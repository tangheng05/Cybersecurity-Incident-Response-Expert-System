## RBAC Implementation Summary

### Role Definitions

The system implements three distinct user roles with specific permissions:

#### 1. **Admin** - System Administrator

**Capabilities:**

- ✅ Manage user accounts (create, edit, delete users)
- ✅ View all summary reports and dashboards
- ✅ Full access to attack types (create, edit, delete)
- ✅ Full access to security rules (create, edit, delete)
- ✅ Delete attack types and rules
- ✅ Access all system features

**Routes Access:**

- `/users/*` - Full CRUD
- `/attack-types/*` - Full CRUD
- `/rules/*` - Full CRUD
- `/dashboard` - Full access

---

#### 2. **Staff (Security Analyst)** - Security Analyst Role

**Capabilities:**

- ✅ Add and edit attack types via dashboard
- ✅ Create and edit decision rules
- ✅ View all attack types and rules
- ✅ Toggle attack type status (active/inactive)
- ✅ View dashboards and reports
- ❌ Cannot delete attack types or rules
- ❌ Cannot manage user accounts

**Routes Access:**

- `/attack-types/` - Read
- `/attack-types/create` - Create
- `/attack-types/<id>/edit` - Edit
- `/attack-types/<id>/toggle-status` - Toggle
- `/rules/*` - Create, Edit, Read
- `/dashboard` - Full access

---

#### 3. **End User (IT Operator)** - Viewer Role

**Capabilities:**

- ✅ Review alerts and incident reports
- ✅ Receive recommended responses
- ✅ Check incident history
- ✅ View attack types (read-only)
- ✅ View security rules (read-only)
- ❌ Cannot create or edit attack types
- ❌ Cannot create or edit rules
- ❌ Cannot manage users

**Routes Access:**

- `/attack-types/` - Read only
- `/attack-types/<id>` - Read only
- `/rules/` - Read only
- `/rules/<id>` - Read only
- `/dashboard` - View only
- `/alerts/*` - Read and review (coming in Milestone 3)
- `/incidents/*` - Read history (coming in Milestone 4)

---

### Implementation Details

#### Route Protection

All routes implement role-based checks:

```python
# Example from attack_type_routes.py
def check_analyst_or_admin():
    """Check if user has analyst or admin role"""
    if 'user_role' not in session or session['user_role'] not in ['admin', 'analyst']:
        flash('Access denied. Only Security Analysts and Admins can manage attack types.', 'danger')
        return False
    return True
```

#### UI Role Indicators

- Navigation bar displays role badges with color coding:
  - Admin: Red badge
  - Analyst: Warning/Yellow badge
  - Viewer: Info/Blue badge

#### Feature Access Matrix

| Feature                      | Admin   | Analyst | Viewer  |
| ---------------------------- | ------- | ------- | ------- |
| User Management              | ✅ Full | ❌ No   | ❌ No   |
| Attack Types (View)          | ✅      | ✅      | ✅      |
| Attack Types (Create/Edit)   | ✅      | ✅      | ❌      |
| Attack Types (Delete)        | ✅      | ❌      | ❌      |
| Security Rules (View)        | ✅      | ✅      | ✅      |
| Security Rules (Create/Edit) | ✅      | ✅      | ❌      |
| Security Rules (Delete)      | ✅      | ❌      | ❌      |
| Alerts (Review)              | ✅      | ✅      | ✅      |
| Incidents (View History)     | ✅      | ✅      | ✅      |
| Dashboard/Reports            | ✅      | ✅      | ✅ View |

---

### Database Schema

The `users` table includes a `role` field:

- Default: `'viewer'`
- Options: `'admin'`, `'analyst'`, `'viewer'`

### Session Management

User role is stored in session:

```python
session['user_role'] = user.role
```

### Current Status

✅ RBAC fully implemented for:

- User management (admin-only)
- Attack type management (admin + analyst)
- Security rules management (admin + analyst)
- Navigation based on roles

⏳ Pending for Milestone 3/4:

- Alert review interface (all roles can view)
- Incident history interface (all roles can view)
