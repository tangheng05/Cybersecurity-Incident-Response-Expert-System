from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    session,
)

from app.forms.user_forms import UserCreateForm, UserEditForm, ConfirmDeleteForm
from app.services.user_service import UserService
from app.utils.decorators import admin_required

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("/")
@admin_required
def index():
    users = UserService.get_all()
    return render_template("users/index.html", users=users)


@user_bp.route("/<int:user_id>")
@admin_required
def detail(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    return render_template("users/detail.html", user=user)


@user_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "role": form.role.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data
        user = UserService.create(data, password)
        flash(f"User '{user.username}' was created successfully.", "success")
        return redirect(url_for("users.index"))

    return render_template("users/create.html", form=form)


@user_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)

    form = UserEditForm(original_user=user, obj=user)

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "role": form.role.data,
            "is_active": form.is_active.data,
        }
        password = form.password.data or None
        UserService.update(user, data, password)
        
        # Update session if the edited user is the currently logged-in user
        if session.get('user_id') == user_id:
            session['user_role'] = user.role
            session['username'] = user.username
            flash(f"Your profile was updated successfully. Your new role is '{user.role}'.", "success")
            
            # If user is no longer active or no longer admin, redirect to dashboard
            if not user.is_active:
                session.clear()
                flash("Your account has been deactivated. Please contact an administrator.", "warning")
                return redirect(url_for('auth.login'))
        else:
            flash(f"User '{user.username}' was updated successfully.", "success")
        
        return redirect(url_for("users.detail", user_id=user.id))

    return render_template("users/edit.html", form=form, user=user)


@user_bp.route("/<int:user_id>/delete", methods=["GET"])
@admin_required
def delete_confirm(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)
    form = ConfirmDeleteForm()
    return render_template("users/delete_confirm.html", user=user, form=form)


@user_bp.route("/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete(user_id: int):
    user = UserService.get_by_id(user_id)
    if user is None:
        abort(404)

    UserService.delete(user)
    flash(f"User was deleted successfully.", "success")
    return redirect(url_for("users.index"))

