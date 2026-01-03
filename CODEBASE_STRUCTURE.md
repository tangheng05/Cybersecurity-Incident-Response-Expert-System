# Codebase Structure Documentation

**Project:** Cybersecurity Incident Response Expert System  
**Date:** December 29, 2025  
**Architecture:** MVC Pattern with Service Layer + Inference Engine  
**Status:** Milestones 1, 2, 3 Completed ✅

---

## 📁 Project Structure

```
MID-TERM/
├── run.py                      # Application entry point
├── config.py                   # Configuration settings
├── extensions.py               # Flask extensions initialization
├── requirements.txt            # Python dependencies
├── create_admin.py             # Admin user creation script
├── seed_rules.py               # Security rules seeding script
├── instance/                   # Instance folder (database storage)
│   └── cybersecurity.db        # SQLite database (auto-generated)
├── app/
│   ├── __init__.py             # Application factory
│   ├── models/                 # Database models (6 tables)
│   │   ├── __init__.py
│   │   ├── user.py             # User model with roles
│   │   ├── attack_type.py      # Attack type definitions
│   │   ├── rule.py             # Security rules with JSON
│   │   ├── alert.py            # Alert model
│   │   ├── incident.py         # Incident with analysis results
│   │   └── incident_history.py # Audit trail
│   ├── forms/                  # WTForms form definitions
│   │   ├── __init__.py
│   │   ├── auth_forms.py       # Login form
│   │   ├── user_forms.py       # User management forms
│   │   ├── attack_type_forms.py # Attack type forms
│   │   ├── rule_forms.py       # Rule management forms
│   │   └── alert_forms.py      # Alert submission form (NEW)
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py     # User CRUD operations
│   │   ├── attack_type_service.py # Attack type service
│   │   ├── rule_service.py     # Rule service
│   │   ├── alert_service.py    # Alert CRUD operations (NEW)
│   │   └── inference_engine.py # Core reasoning engine (NEW)
│   ├── routes/                 # Route handlers/controllers
│   │   ├── __init__.py
│   │   ├── auth_routes.py      # Login/logout
│   │   ├── dashboard_routes.py # Dashboard
│   │   ├── user_routes.py      # User management
│   │   ├── attack_type_routes.py # Attack type CRUD
│   │   ├── rule_routes.py      # Rule CRUD
│   │   └── alert_routes.py     # Alert management (NEW)
│   ├── templates/              # HTML templates
│   │   ├── layouts/
│   │   │   └── base.html       # Base with navigation
│   │   ├── auth/
│   │   │   └── login.html      # Login page
│   │   ├── dashboard/
│   │   │   └── index.html      # Dashboard
│   │   ├── users/              # User templates (6 files)
│   │   ├── attack_types/       # Attack type templates (5 files)
│   │   ├── rules/              # Rule templates (5 files)
│   │   └── alerts/             # Alert templates (NEW)
│   │       ├── index.html      # Alert list with filters
│   │       ├── detail.html     # Alert + analysis results
│   │       └── create.html     # Alert submission form
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   └── style.css       # Custom styles
│   │   ├── js/
│   │   │   └── main.js         # Client-side JavaScript
│   │   └── images/             # Image assets
│   └── tests/                  # Unit tests (placeholder)
└── migrations/                 # Database migrations (placeholder)
```

---

## 🏗️ Architecture Overview

### **Layer Separation**

1. **Models** (`app/models/`) - Data layer, 6 database tables with relationships
2. **Forms** (`app/forms/`) - Validation and user input handling with custom validators
3. **Services** (`app/services/`) - Business logic, CRUD operations, **Inference Engine**
4. **Routes** (`app/routes/`) - HTTP endpoints, blueprints, RBAC enforcement
5. **Templates** (`app/templates/`) - Presentation layer with Bootstrap 5

### **Core Components**

- **Inference Engine** (`app/services/inference_engine.py`) - Pattern matching, confidence scoring, recommendation generation
- **RBAC System** - Role-based access control (admin, analyst, viewer)
- **JSON Storage** - Flexible rule conditions and alert data
- **Alert Processing** - Automatic analysis and incident creation

---

## 📄 File Details

### **Root Configuration Files**

#### `run.py`

- Application entry point
- Imports and runs the Flask app
- Runs with `debug=True` for development

#### `config.py`

- **Class:** `Config`
- **Settings:**
  - `SECRET_KEY`: Environment variable or default dev key
  - `SQLALCHEMY_DATABASE_URI`: SQLite database in instance folder
  - `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled for performance

#### `extensions.py`

- Initializes Flask extensions:
  - `db`: SQLAlchemy database instance
  - `csrf`: CSRF protection instance

#### `requirements.txt`

- Flask==2.3.3
- Flask-WTF==1.1.1
- WTForms==3.1.2
- email-validator==2.1.0.post1
- Werkzeug==2.3.7
- Flask-SQLAlchemy==3.1.1

#### `create_admin.py`

- Creates default admin user (admin/Admin@123)
- Run once during initial setup

#### `seed_rules.py`

- Creates 11 security rules:
  - 5 Brute Force attack rules
  - 6 DDoS attack rules
- Populates attack_types table
- Run after database initialization

---

### **Application Factory** (`app/__init__.py`)

#### `create_app(config_class=Config)`

- Creates and configures Flask application
- Initializes extensions (db, csrf)
- Registers blueprints:
  - auth_bp (authentication)
  - dashboard_bp (dashboard)
  - user_bp (user management)
  - attack_type_bp (attack types)
  - rule_bp (rules)
  - alert_bp (alerts - NEW)
- Creates instance folder if not exists
- Creates database tables on startup
- Sets up root route redirect to dashboard

---

### **Models Layer** (`app/models/`)

#### `User` Model (`user.py`)

**Table:** `users`

**Fields:**

- `id`: Integer, primary key
- `username`: String(80), unique, not null
- `email`: String(120), unique, not null
- `full_name`: String(120), not null
- `role`: String(20), default 'viewer' (admin/analyst/viewer)
- `is_active`: Boolean, default True
- `password_hash`: String(255), not null
- `created_at`: DateTime, default UTC now
- `updated_at`: DateTime, auto-updates on change
- `last_login`: DateTime, nullable

**Methods:**

- `set_password(password)`: Hashes and stores password
- `check_password(password)`: Verifies password against hash
- `__repr__()`: String representation

---

#### `AttackType` Model (`attack_type.py`)

**Table:** `attack_types`

**Fields:**

- `id`: Integer, primary key
- `name`: String(100), unique, not null (e.g., "Brute Force", "DDoS")
- `description`: Text, not null
- `severity_level`: Integer (1-10)
- `is_active`: Boolean, default True

**Relationships:**

- `rules`: One-to-many with Rule model
- `incidents`: One-to-many with Incident model

---

#### `Rule` Model (`rule.py`)

**Table:** `rules`

**Fields:**

- `id`: Integer, primary key
- `name`: String(200), not null
- `attack_type_id`: Integer, foreign key to attack_types
- `conditions`: JSON (flexible rule conditions)
- `actions`: JSON (recommended actions array)
- `priority`: String(20) (high/medium/low)
- `severity_score`: Integer (1-10)
- `is_active`: Boolean, default True
- `created_at`: DateTime
- `updated_at`: DateTime

**Relationships:**

- `attack_type`: Many-to-one with AttackType

**JSON Structure Examples:**

```python
# conditions
{
    "failed_attempts": {"operator": ">=", "value": 5},
    "time_window": 300,  # seconds
    "source_ip": {"type": "same"}
}

# actions
["block_ip", "alert_security_team", "log_incident", "enable_rate_limiting"]
```

---

#### `Alert` Model (`alert.py`)

**Table:** `alerts`

**Fields:**

- `id`: Integer, primary key
- `timestamp`: DateTime, default UTC now
- `source_ip`: String(45) (supports IPv4/IPv6)
- `destination_ip`: String(45)
- `alert_type`: String(100)
- `severity`: String(20) (low/medium/high/critical)
- `raw_data`: JSON (flexible alert data)
- `status`: String(20) (new/processed/ignored)
- `created_at`: DateTime

**Relationships:**

- `incident`: One-to-one with Incident model

---

#### `Incident` Model (`incident.py`)

**Table:** `incidents`

**Fields:**

- `id`: Integer, primary key
- `alert_id`: Integer, foreign key to alerts, unique
- `attack_type_id`: Integer, foreign key to attack_types
- `matched_rules`: JSON (array of matched rule IDs)
- `recommended_actions`: JSON (array of action strings)
- `confidence_score`: Integer (0-100)
- `explanation`: Text (human-readable analysis)
- `status`: String(20) (new/analyzing/pending/resolved)
- `assigned_to`: Integer, foreign key to users, nullable
- `created_at`: DateTime
- `updated_at`: DateTime
- `resolved_at`: DateTime, nullable

**Relationships:**

- `alert`: One-to-one with Alert
- `attack_type`: Many-to-one with AttackType
- `assigned_user`: Many-to-one with User
- `history_entries`: One-to-many with IncidentHistory

---

#### `IncidentHistory` Model (`incident_history.py`)

**Table:** `incident_history`

**Fields:**

- `id`: Integer, primary key
- `incident_id`: Integer, foreign key to incidents
- `action_taken`: String(200)
- `notes`: Text, nullable
- `performed_by`: Integer, foreign key to users
- `timestamp`: DateTime, default UTC now

**Relationships:**

- `incident`: Many-to-one with Incident
- `user`: Many-to-one with User

---

### **Forms Layer** (`app/forms/`)

#### `LoginForm` (`auth_forms.py`)

**Purpose:** User authentication

**Fields:**

- `username`: StringField (required)
- `password`: PasswordField (required)
- `submit`: SubmitField

---

#### `UserCreateForm` (`user_forms.py`)

**Purpose:** Create new user with required password

**Fields:**

- `username`: StringField (3-80 chars, required)
- `email`: StringField (email validation, required)
- `full_name`: StringField (1-120 chars, required)
- `role`: SelectField (admin/analyst/viewer)
- `is_active`: BooleanField (default True)
- `password`: PasswordField (required, strong validation)
- `confirm_password`: PasswordField (must match password)
- `submit`: SubmitField

**Validators:**

- `validate_username()`: Check uniqueness
- `validate_email()`: Check uniqueness
- `strong_password()`: Custom validator (8+ chars, upper, lower, digit, special)

#### `UserEditForm` (`user_forms.py`)

**Purpose:** Edit existing user with optional password update

**Fields:** Same as CreateForm except password is optional

**Special:**

- `__init__()`: Takes `original_user` to exclude from uniqueness checks
- `validate_username()`: Excludes current user ID
- `validate_email()`: Excludes current user ID

---

#### `AttackTypeForm` (`attack_type_forms.py`)

**Purpose:** Create/edit attack type definitions

**Fields:**

- `name`: StringField (required, unique)
- `description`: TextAreaField (required)
- `severity_level`: SelectField (1-10)
- `is_active`: BooleanField
- `submit`: SubmitField

---

#### `RuleForm` (`rule_forms.py`)

**Purpose:** Create/edit security rules with JSON conditions

**Fields:**

- `name`: StringField (required)
- `attack_type_id`: SelectField (populated from attack_types)
- `conditions`: TextAreaField (JSON format, validated)
- `actions`: TextAreaField (JSON array, validated)
- `priority`: SelectField (high/medium/low)
- `severity_score`: SelectField (1-10)
- `is_active`: BooleanField
- `submit`: SubmitField

**Custom Validators:**

- `validate_conditions()`: Ensures valid JSON format
- `validate_actions()`: Ensures valid JSON array

---

#### `AlertForm` (`alert_forms.py`) **NEW**

**Purpose:** Submit security alerts for analysis

**Fields:**

- `source_ip`: StringField (required, IP address validation)
- `destination_ip`: StringField (optional, IP address validation)
- `alert_type`: StringField (required)
- `severity`: SelectField (low/medium/high/critical)
- `raw_data`: TextAreaField (JSON format, validated)
- `submit`: SubmitField

**Custom Validators:**

- `validate_raw_data()`: Ensures valid JSON format for alert data

#### `ConfirmDeleteForm` (`user_forms.py`, `attack_type_forms.py`, `rule_forms.py`)

**Purpose:** Simple confirmation for delete action

**Fields:**

- `submit`: SubmitField ("Confirm Delete")

- `__init__()`: Takes `original_user` to exclude from uniqueness checks
- `validate_username()`: Excludes current user ID
- `validate_email()`: Excludes current user ID

#### `ConfirmDeleteForm` (`user_forms.py`)

**Purpose:** Simple confirmation for delete action

**Fields:**

- `submit`: SubmitField ("Confirm Delete")

---

### **Services Layer** (`app/services/`)

#### `UserService` (`user_service.py`)

**Pattern:** Static methods for user operations

**Methods:**

- `get_all()`: Returns all users ordered by ID descending
- `get_by_id(user_id)`: Returns single user or None
- `create(data, password)`: Creates user with hashed password
- `update(user, data, password=None)`: Updates user, optionally changes password
- `delete(user)`: Deletes user from database

---

#### `AttackTypeService` (`attack_type_service.py`)

**Pattern:** Static methods for attack type operations

**Methods:**

- `get_all()`: Returns all attack types
- `get_active()`: Returns only active attack types
- `get_by_id(attack_type_id)`: Returns single attack type or None
- `create(data)`: Creates new attack type
- `update(attack_type, data)`: Updates attack type
- `delete(attack_type)`: Deletes attack type

---

#### `RuleService` (`rule_service.py`)

**Pattern:** Static methods for rule operations

**Methods:**

- `get_all()`: Returns all rules with relationships
- `get_by_attack_type(attack_type_id)`: Filters rules by attack type
- `get_active()`: Returns only active rules
- `get_by_id(rule_id)`: Returns single rule or None
- `create(data)`: Creates new rule with JSON validation
- `update(rule, data)`: Updates rule
- `delete(rule)`: Deletes rule

---

#### `AlertService` (`alert_service.py`) **NEW**

**Pattern:** Static methods for alert operations

**Methods:**

- `get_all(status=None)`: Returns all alerts, optionally filtered by status
- `get_by_id(alert_id)`: Returns single alert with incident data or None
- `create(data)`: Creates new alert with JSON raw_data
- `update_status(alert, status)`: Updates alert status (new/processed/ignored)
- `delete(alert)`: Deletes alert

**Status Values:**

- `new`: Alert just submitted, awaiting analysis
- `processed`: Alert analyzed, incident created
- `ignored`: Alert dismissed by analyst

---

#### `InferenceEngine` (`inference_engine.py`) **NEW - CORE REASONING ENGINE**

**Purpose:** Analyzes security alerts and generates actionable recommendations

**Main Method:**

```python
analyze_alert(alert: Alert) -> dict
```

Returns:

```python
{
    'matched_rules': [Rule objects],
    'recommended_actions': ['action1', 'action2'],
    'confidence_score': 85,  # 0-100
    'explanation': 'Detailed analysis text',
    'attack_type_id': 1
}
```

**Core Methods:**

1. **`analyze_alert(alert)`**

   - Main orchestrator for alert analysis
   - Retrieves active rules
   - Calls match_rules()
   - Generates recommendations
   - Returns comprehensive analysis dict

2. **`match_rules(alert, rules)`**

   - Pattern matching algorithm
   - Evaluates each rule's conditions against alert
   - Requires 70% condition match threshold
   - Returns sorted list by priority (high=3, medium=2, low=1)

3. **`evaluate_conditions(alert_data, conditions)`**

   - Evaluates individual rule conditions
   - Supports operators:
     - Numeric: `>=`, `<=`, `>`, `<`, `==`
     - Boolean: direct comparison
     - String: exact match or substring
     - List: `in` operator
   - Returns (matched_count, total_count)

4. **`prioritize_actions(matched_rules)`**

   - Combines actions from all matched rules
   - Priority mapping:
     - `high`: weight 3
     - `medium`: weight 2
     - `low`: weight 1
   - Returns deduplicated, prioritized action list

5. **`calculate_confidence(matched_rules, alert)`**

   - Multi-factor confidence scoring (0-100)
   - **Base confidence:** 40 points
   - **Match score:** (matched_rules / total_active_rules) \* 30
   - **Priority bonus:** Average priority weight \* 10
   - **Severity factor:** (alert_severity / 10) \* 10
   - Total capped at 100

6. **`generate_explanation(matched_rules, alert, confidence)`**
   - Creates human-readable analysis
   - Includes:
     - Matched rule names
     - Attack type identification
     - Confidence score
     - Alert details (IP, severity, type)
     - Recommendation summary

**Pattern Matching Logic:**

- Iterates through all active rules
- Evaluates each rule's JSON conditions against alert raw_data
- Requires >= 70% of conditions to match
- Matched rules sorted by priority for action selection

**Example Usage:**

```python
from app.services.inference_engine import InferenceEngine
from app.models import Alert

# Get alert
alert = Alert.query.get(1)

# Analyze
engine = InferenceEngine()
results = engine.analyze_alert(alert)

# Create incident with results
incident = Incident(
    alert_id=alert.id,
    attack_type_id=results['attack_type_id'],
    matched_rules=[r.id for r in results['matched_rules']],
    recommended_actions=results['recommended_actions'],
    confidence_score=results['confidence_score'],
    explanation=results['explanation'],
    status='new'
)
```

---

### **Routes Layer** (`app/routes/`)

#### `auth_routes.py`

**Blueprint:** `auth` (no prefix)

**Routes:**

| Method   | Path      | Function   | Description           | RBAC          |
| -------- | --------- | ---------- | --------------------- | ------------- |
| GET/POST | `/login`  | `login()`  | User login            | Public        |
| GET      | `/logout` | `logout()` | User logout, redirect | Authenticated |

**Features:**

- Session-based authentication
- Password verification with Werkzeug
- Last login timestamp update
- Flash messages for errors

---

#### `dashboard_routes.py`

**Blueprint:** `dashboard` (no prefix)

**Routes:**

| Method | Path | Function  | Description    | RBAC          |
| ------ | ---- | --------- | -------------- | ------------- |
| GET    | `/`  | `index()` | Dashboard home | Authenticated |

**Features:**

- Displays user info and role
- Quick action buttons
- Statistics placeholders
- RBAC-based menu items

---

#### `user_routes.py`

**Blueprint:** `users` (prefix: `/users`)

**Routes:**

| Method   | Path                 | Function                  | Description              | RBAC  |
| -------- | -------------------- | ------------------------- | ------------------------ | ----- |
| GET      | `/users/`            | `index()`                 | List all users           | Admin |
| GET      | `/users/<id>`        | `detail(user_id)`         | View user details        | Admin |
| GET/POST | `/users/create`      | `create()`                | Create new user          | Admin |
| GET/POST | `/users/<id>/edit`   | `edit(user_id)`           | Edit user                | Admin |
| GET      | `/users/<id>/delete` | `delete_confirm(user_id)` | Show delete confirmation | Admin |
| POST     | `/users/<id>/delete` | `delete(user_id)`         | Execute deletion         | Admin |

**Features:**

- Flash messages for user feedback
- 404 abort on user not found
- Form validation with error display
- Redirect after successful operations
- RBAC check: admin only

---

#### `attack_type_routes.py`

**Blueprint:** `attack_types` (prefix: `/attack-types`)

**Routes:**

| Method   | Path                        | Function                         | Description              | RBAC           |
| -------- | --------------------------- | -------------------------------- | ------------------------ | -------------- |
| GET      | `/attack-types/`            | `index()`                        | List all attack types    | Analyst, Admin |
| GET      | `/attack-types/<id>`        | `detail(attack_type_id)`         | View attack type details | Analyst, Admin |
| GET/POST | `/attack-types/create`      | `create()`                       | Create new attack type   | Analyst, Admin |
| GET/POST | `/attack-types/<id>/edit`   | `edit(attack_type_id)`           | Edit attack type         | Analyst, Admin |
| GET      | `/attack-types/<id>/delete` | `delete_confirm(attack_type_id)` | Show delete confirmation | Admin          |
| POST     | `/attack-types/<id>/delete` | `delete(attack_type_id)`         | Execute deletion         | Admin          |

**Features:**

- RBAC: Analysts can create/edit, only Admins can delete
- Severity level selection (1-10)
- Active/Inactive toggle
- Related rules count display

---

#### `rule_routes.py`

**Blueprint:** `rules` (prefix: `/rules`)

**Routes:**

| Method   | Path                 | Function                  | Description              | RBAC           |
| -------- | -------------------- | ------------------------- | ------------------------ | -------------- |
| GET      | `/rules/`            | `index()`                 | List all rules           | All roles      |
| GET      | `/rules/<id>`        | `detail(rule_id)`         | View rule details        | All roles      |
| GET/POST | `/rules/create`      | `create()`                | Create new rule          | Analyst, Admin |
| GET/POST | `/rules/<id>/edit`   | `edit(rule_id)`           | Edit rule                | Analyst, Admin |
| GET      | `/rules/<id>/delete` | `delete_confirm(rule_id)` | Show delete confirmation | Admin          |
| POST     | `/rules/<id>/delete` | `delete(rule_id)`         | Execute deletion         | Admin          |

**Features:**

- JSON condition editor with validation
- JSON action editor with validation
- Priority and severity selection
- Attack type association
- RBAC: Viewers can read, Analysts can create/edit, Admins can delete

---

#### `alert_routes.py` **NEW**

**Blueprint:** `alerts` (prefix: `/alerts`)

**Routes:**

| Method   | Path                   | Function            | Description                    | RBAC           |
| -------- | ---------------------- | ------------------- | ------------------------------ | -------------- |
| GET      | `/alerts/`             | `index()`           | List all alerts with filtering | All roles      |
| GET      | `/alerts/<id>`         | `detail(alert_id)`  | View alert + analysis results  | All roles      |
| GET/POST | `/alerts/create`       | `create()`          | Submit new alert               | All roles      |
| POST     | `/alerts/<id>/analyze` | `analyze(alert_id)` | Re-analyze existing alert      | Analyst, Admin |

**Features:**

- **index():**

  - Displays all alerts in table
  - Filter by status (new/processed/ignored) via query param `?status=new`
  - Color-coded severity badges (low=success, medium=warning, high=danger, critical=dark)
  - Status tabs for quick filtering

- **detail():**

  - Shows alert information (IP, type, severity, timestamp)
  - Displays raw_data JSON formatted
  - Shows linked incident with:
    - Attack type identified
    - Matched rules list
    - Recommended actions
    - Confidence score (0-100) with progress bar
    - Detailed explanation
  - "Re-analyze" button for Analysts/Admins

- **create():**

  - Alert submission form
  - Sample JSON templates for Brute Force and DDoS
  - Validates IP addresses
  - Validates JSON raw_data format
  - **On successful submission:**
    1. Creates alert record
    2. Runs InferenceEngine.analyze_alert()
    3. Creates incident with analysis results
    4. Sets alert status to 'processed'
    5. Redirects to alert detail page

- **analyze():**
  - RBAC: Analyst or Admin only
  - Re-runs inference engine on existing alert
  - Updates or creates new incident
  - Flash success message
  - Redirects to detail page

**Workflow:**

```
User submits alert → create() → InferenceEngine analyzes
                               → Incident created with results
                               → Redirect to detail()
                               → User sees analysis + recommendations
```

---

### **Templates Layer** (`app/templates/`)

#### Base Layout (`layouts/base.html`)

- Bootstrap 5 framework
- Responsive navbar with role-based menu items:
  - **All users:** Dashboard, Alerts
  - **Analysts/Admins:** Attack Types, Rules
  - **Admins only:** Users
- Flash message display with dismissible alerts
- Content block for child templates
- User info and logout button
- Links to custom CSS and JS

---

#### Authentication Templates (`auth/`)

**`login.html`**

- Bootstrap styled login form
- Username and password fields
- CSRF protection
- Flash messages for errors
- Redirect to dashboard on success

---

#### Dashboard Templates (`dashboard/`)

**`index.html`**

- Welcome message with user's full name and role
- Quick action cards:
  - View Alerts
  - Manage Rules (Analyst/Admin)
  - Manage Attack Types (Analyst/Admin)
  - Manage Users (Admin)
- Statistics placeholders (for Milestone 4)

---

#### User Templates (`users/`)

**`index.html`**

- Displays users in Bootstrap table
- Shows: ID, Username, Full Name, Email, Role, Status badge, Created date
- Action buttons: Edit (✏️), Delete (🗑️)
- "No users found" message when empty
- Create User button

**`detail.html`**

- Definition list showing all user fields
- Role and status displayed as Bootstrap badges
- Last login timestamp
- Edit button and back to list link

**`create.html`**

- Page title: "Create User"
- Includes `_form.html` partial
- Form submits via POST

**`edit.html`**

- Page title: "Edit User"
- Includes `_form.html` partial
- Shows current values
- Form submits via POST

**`delete_confirm.html`**

- Warning card with user details
- Lists username, full name, email, role
- Confirm Delete button (danger style)
- Cancel link back to index

**`_form.html`** (Partial)

- Reusable form fields for create/edit
- Fields: username, email, full_name, role, is_active, password, confirm_password
- Error display for each field
- Submit and Cancel buttons
- Bootstrap form styling

---

#### Attack Type Templates (`attack_types/`)

**`index.html`**

- Table with: ID, Name, Severity Level, Status, Actions
- Severity displayed as colored badges
- Create Attack Type button (Analyst/Admin)
- Edit/Delete actions

**`detail.html`**

- Attack type information
- Related rules count
- Edit button (Analyst/Admin)
- Delete button (Admin only)

**`create.html`**, **`edit.html`**, **`delete_confirm.html`**, **`_form.html`**

- Similar structure to user templates
- Severity level dropdown (1-10)
- Description textarea

---

#### Rule Templates (`rules/`)

**`index.html`**

- Table with: ID, Name, Attack Type, Priority, Severity, Status
- Priority badges (high=danger, medium=warning, low=info)
- Filter by attack type
- Create Rule button (Analyst/Admin)

**`detail.html`**

- Rule information with all fields
- JSON conditions displayed formatted
- JSON actions displayed as list
- Attack type link
- Edit button (Analyst/Admin)
- Delete button (Admin only)

**`create.html`**, **`edit.html`**

- Form with JSON editors for conditions and actions
- Attack type dropdown
- Priority and severity dropdowns
- JSON validation on submit

**`delete_confirm.html`**, **`_form.html`**

- Standard delete confirmation
- JSON syntax highlighting

---

#### Alert Templates (`alerts/`) **NEW**

**`index.html`**

- **Status Filter Tabs:**

  - All Alerts
  - New (badge count)
  - Processed (badge count)
  - Ignored (badge count)

- **Alert Table:**

  - Columns: ID, Source IP, Alert Type, Severity, Status, Timestamp, Actions
  - **Severity Badges:**
    - Low: success (green)
    - Medium: warning (yellow)
    - High: danger (red)
    - Critical: dark (black)
  - **Status Badges:**
    - New: primary (blue)
    - Processed: success (green)
    - Ignored: secondary (gray)
  - Action: View Details button

- **Create Alert Button** (all roles)

**`detail.html`**

- **Two-Column Layout:**

  **Left Column - Alert Information:**

  - Source IP
  - Destination IP (if present)
  - Alert Type
  - Severity (badge)
  - Status (badge)
  - Timestamp
  - Raw Data (JSON formatted with syntax highlighting)

  **Right Column - Incident Analysis:**

  - Attack Type Identified (badge with icon)
  - **Confidence Score:**
    - Progress bar (0-100%)
    - Color-coded:
      - 0-40: danger (red)
      - 41-70: warning (yellow)
      - 71-100: success (green)
  - **Matched Rules:**
    - List of rule names with links
    - Priority badges
  - **Recommended Actions:**
    - Ordered list
    - Icon for each action
  - **Detailed Explanation:**
    - Multi-paragraph analysis
    - Human-readable reasoning

- **Actions:**
  - Re-analyze button (Analyst/Admin only)
  - Back to Alerts List

**`create.html`**

- **Alert Submission Form:**

  - Source IP (required, validated)
  - Destination IP (optional)
  - Alert Type
  - Severity dropdown
  - Raw Data (JSON textarea)

- **Sample JSON Templates:**

  - **Brute Force Attack:**
    ```json
    {
      "failed_attempts": 7,
      "time_window": 300,
      "target_account": "admin",
      "authentication_method": "password"
    }
    ```
  - **DDoS Attack:**
    ```json
    {
      "request_count": 15000,
      "time_window": 60,
      "protocol": "HTTP",
      "target_service": "web_server"
    }
    ```

- **Copy-to-form Buttons** for samples
- JSON validation on submit
- Submit button → Triggers automatic analysis

---

### **Static Assets** (`app/static/`)

#### `css/style.css`

- Body background: #f5f5f5 (light gray)
- Container max-width: 960px
- Table vertical alignment: middle

#### `js/main.js`

- Real-time password strength validation
- Checks for: 8+ chars, uppercase, lowercase, digit, special char
- Updates help text with ✅ when strong
- Color-coded feedback (green/red)

---

## 🔑 Key Features

### **Security**

- ✅ Password hashing with Werkzeug (pbkdf2:sha256)
- ✅ CSRF protection on all forms
- ✅ Strong password requirements enforced
- ✅ Server-side validation for all inputs
- ✅ Role-Based Access Control (RBAC) with 3 roles
- ✅ Session-based authentication

### **RBAC Implementation**

- ✅ **Admin Role:**
  - Manage all users (CRUD)
  - Delete attack types and rules
  - Full system access
- ✅ **Analyst Role (Security Analyst):**
  - Create/edit attack types
  - Create/edit security rules
  - Submit and analyze alerts
  - Re-analyze existing alerts
- ✅ **Viewer Role (IT Operator):**
  - View alerts and incidents
  - View incident history
  - Read-only access to rules and attack types

### **Validation**

- ✅ Email format validation
- ✅ IP address validation (IPv4/IPv6)
- ✅ Username uniqueness check
- ✅ Email uniqueness check
- ✅ JSON format validation for rules and alerts
- ✅ Password strength requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character

### **Expert System Features**

- ✅ **11 Security Rules:**
  - 5 Brute Force attack patterns
  - 6 DDoS attack patterns
- ✅ **Inference Engine:**
  - Pattern matching with 70% threshold
  - Multi-factor confidence scoring (0-100)
  - Priority-based action selection
  - Human-readable explanation generation
- ✅ **Alert Processing:**
  - Automatic analysis on submission
  - Incident creation with recommendations
  - Status tracking (new/processed/ignored)
  - Re-analysis capability
- ✅ **JSON Flexibility:**
  - Dynamic rule conditions
  - Flexible alert data structure
  - Extensible action definitions

### **User Experience**

- ✅ Bootstrap 5 responsive design
- ✅ Flash messages for feedback
- ✅ Real-time password validation
- ✅ Confirmation pages for deletions
- ✅ Status badges (color-coded)
- ✅ Severity indicators
- ✅ Filterable alert lists
- ✅ Sample JSON templates
- ✅ Clean, modern UI

### **Code Quality**

- ✅ MVC architecture with service layer
- ✅ DRY principle (reusable form partials)
- ✅ Type hints in service methods
- ✅ Application factory pattern
- ✅ Blueprint organization
- ✅ Separation of concerns
- ✅ Dedicated inference engine module

---

## 🚀 Application Flows

### **Alert Analysis Workflow**

1. **User submits alert** → `POST /alerts/create`
2. **AlertForm validates** input:
   - IP address format
   - JSON raw_data structure
   - Required fields
3. **AlertService.create()** saves alert to database
4. **InferenceEngine.analyze_alert()** runs automatically:
   - a. Retrieves all active rules
   - b. Matches rules against alert data (70% threshold)
   - c. Prioritizes matched rules (high=3, medium=2, low=1)
   - d. Combines actions from matched rules
   - e. Calculates confidence score (0-100)
   - f. Generates human-readable explanation
5. **Incident created** with analysis results:
   - Attack type identified
   - Matched rule IDs
   - Recommended actions
   - Confidence score
   - Detailed explanation
6. **Alert status updated** to 'processed'
7. **Redirect to detail page** → User sees analysis
8. **User can re-analyze** (Analyst/Admin only)

### **Pattern Matching Algorithm**

```python
For each active rule:
    matched_conditions = 0
    total_conditions = len(rule.conditions)

    For each condition in rule.conditions:
        if condition matches alert.raw_data:
            matched_conditions += 1

    match_percentage = matched_conditions / total_conditions

    if match_percentage >= 0.70:  # 70% threshold
        Add rule to matched_rules

Sort matched_rules by priority (high > medium > low)
Return matched_rules
```

### **Confidence Scoring Formula**

```python
base_confidence = 40

match_score = (num_matched_rules / total_active_rules) * 30

priority_weights = {'high': 3, 'medium': 2, 'low': 1}
avg_priority = average([priority_weights[r.priority] for r in matched_rules])
priority_bonus = avg_priority * 10

severity_map = {'low': 2.5, 'medium': 5, 'high': 7.5, 'critical': 10}
severity_factor = severity_map[alert.severity]

confidence = base_confidence + match_score + priority_bonus + severity_factor
confidence = min(confidence, 100)  # Cap at 100
```

### **Create User Flow**

1. User clicks "Create" → `GET /users/create`
2. `create()` renders form via `UserCreateForm`
3. User fills form and submits → `POST /users/create`
4. Form validates (client-side JS + server-side)
5. If valid: `UserService.create()` → Flash message → Redirect to index
6. If invalid: Re-render form with error messages

### **Edit User Flow**

1. User clicks Edit (✏️) → `GET /users/<id>/edit`
2. `edit()` loads user, renders form with current data
3. User modifies and submits → `POST /users/<id>/edit`
4. Form validates (excluding current user from uniqueness checks)
5. If valid: `UserService.update()` → Flash message → Redirect to detail
6. If invalid: Re-render with errors

### **Delete User Flow**

1. User clicks Delete (🗑️) → `GET /users/<id>/delete`
2. `delete_confirm()` renders confirmation page
3. User confirms → `POST /users/<id>/delete`
4. `UserService.delete()` → Flash message → Redirect to index

### **Rule Creation Flow**

1. Analyst navigates to Rules → Create Rule
2. Fills form with:
   - Rule name
   - Attack type selection
   - JSON conditions (validated)
   - JSON actions (validated)
   - Priority level
   - Severity score
3. Form validates JSON format
4. `RuleService.create()` saves rule
5. Rule becomes active for pattern matching
6. Redirect to rules list

### **Login Flow**

1. User accesses `/login`
2. Enters username and password
3. `LoginForm` validates
4. `User.check_password()` verifies hash
5. If valid:
   - Session created with user_id and role
   - Last login timestamp updated
   - Redirect to dashboard
6. If invalid:
   - Flash error message
   - Re-render login form

---

## 🗄️ Database Schema

### **users** Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    role VARCHAR(20) DEFAULT 'viewer' NOT NULL,
    is_active BOOLEAN DEFAULT 1 NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_login DATETIME
);
```

### **attack_types** Table

```sql
CREATE TABLE attack_types (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    severity_level INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 1 NOT NULL
);
```

### **rules** Table

```sql
CREATE TABLE rules (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    attack_type_id INTEGER NOT NULL,
    conditions JSON NOT NULL,
    actions JSON NOT NULL,
    priority VARCHAR(20) NOT NULL,
    severity_score INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 1 NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (attack_type_id) REFERENCES attack_types(id)
);
```

### **alerts** Table

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    source_ip VARCHAR(45) NOT NULL,
    destination_ip VARCHAR(45),
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    raw_data JSON NOT NULL,
    status VARCHAR(20) DEFAULT 'new' NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### **incidents** Table

```sql
CREATE TABLE incidents (
    id INTEGER PRIMARY KEY,
    alert_id INTEGER UNIQUE NOT NULL,
    attack_type_id INTEGER NOT NULL,
    matched_rules JSON NOT NULL,
    recommended_actions JSON NOT NULL,
    confidence_score INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new' NOT NULL,
    assigned_to INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    resolved_at DATETIME,
    FOREIGN KEY (alert_id) REFERENCES alerts(id),
    FOREIGN KEY (attack_type_id) REFERENCES attack_types(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```

### **incident_history** Table

```sql
CREATE TABLE incident_history (
    id INTEGER PRIMARY KEY,
    incident_id INTEGER NOT NULL,
    action_taken VARCHAR(200) NOT NULL,
    notes TEXT,
    performed_by INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (incident_id) REFERENCES incidents(id),
    FOREIGN KEY (performed_by) REFERENCES users(id)
);
```

### **Relationships**

```
users (1) ──────────┬─── (∞) incidents [assigned_to]
                    └─── (∞) incident_history [performed_by]

attack_types (1) ───┬─── (∞) rules
                    └─── (∞) incidents

alerts (1) ───────────── (1) incidents [unique constraint]

rules ─────────────────── (stored in incidents.matched_rules as JSON)

incidents (1) ──────────── (∞) incident_history
```

---

## 📦 Dependencies

| Package          | Version     | Purpose                     |
| ---------------- | ----------- | --------------------------- |
| Flask            | 2.3.3       | Web framework               |
| Flask-WTF        | 1.1.1       | Form handling & CSRF        |
| WTForms          | 3.1.2       | Form validation             |
| email-validator  | 2.1.0.post1 | Email validation            |
| Werkzeug         | 2.3.7       | Password hashing, utilities |
| Flask-SQLAlchemy | 3.1.1       | ORM for database            |

---

## 🔧 Configuration

### **Environment Variables**

- `SECRET_KEY`: Flask secret key (optional, has default)
- `DATABASE_URL`: Database URI (optional, defaults to SQLite)

### **Default Settings**

- Database: SQLite at `instance/users.db`
- Debug mode: Enabled in development
- CSRF protection: Enabled globally
- SQLAlchemy track modifications: Disabled

---

## 🎯 Future Enhancements (Placeholder Directories)

- `app/tests/`: Unit and integration tests
- `migrations/`: Database migration scripts
- `app/templates/roles/`: Role management (if needed)
- `app/utils/`: Utility functions

---

## 📝 Notes

- Application uses SQLite for simplicity (can be changed in config)
- Password is never stored in plain text
- All forms include CSRF tokens
- Edit form allows optional password changes
- Database tables are created automatically on first run
- Root URL `/` redirects to dashboard
- Inference Engine runs automatically on alert submission
- 70% condition match threshold ensures high-quality pattern matching
- Confidence scoring ranges from 0-100 with multi-factor calculation
- JSON storage allows flexible rule conditions without schema changes
- RBAC enforced at route level with role checks

---

## 🎯 Completed Milestones Summary

### **Milestone 1: Database & Authentication** ✅

- 6 database tables with proper relationships
- Session-based authentication system
- User management with RBAC
- Password hashing and validation
- Dashboard interface

### **Milestone 2: Knowledge Base** ✅

- 11 security rules (5 Brute Force + 6 DDoS)
- Attack type management interface
- Rule management with JSON conditions/actions
- Priority and severity systems
- RBAC implementation for analysts

### **Milestone 3: Inference Engine** ✅

- Complete reasoning engine with 6 core methods
- Pattern matching algorithm (70% threshold)
- Multi-factor confidence scoring (0-100)
- Action prioritization and combination
- Human-readable explanation generation
- Alert management interface
- Automatic incident creation
- Alert filtering and status tracking
- Re-analysis capability

---

## 🚀 Next Steps (Milestone 4)

### **Dashboard Enhancements**

- [ ] Real-time statistics display
- [ ] Chart.js visualizations:
  - Attack type distribution (pie chart)
  - Incident timeline (line chart)
  - Severity distribution (bar chart)
- [ ] Recent alerts feed
- [ ] Active incidents counter

### **Incident History Interface**

- [ ] Incident list with search/filter
- [ ] Incident detail pages
- [ ] Action tracking
- [ ] Status workflow (new → analyzing → pending → resolved)
- [ ] Notes and comments
- [ ] Assignment to users

### **Reporting Features**

- [ ] Incident history log (all users)
- [ ] Response time metrics
- [ ] Attack pattern analysis
- [ ] Export functionality

---

**End of Documentation**
