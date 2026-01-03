# Cybersecurity Incident Response Expert System

**Milestone 1 - COMPLETED ✅**  
**Milestone 2 - COMPLETED ✅**  
**Milestone 3 - COMPLETED ✅**

## Project Overview

An automated incident response expert system that analyzes security alerts using if-then rules and provides actionable recommendations for handling Brute Force and DDoS attacks.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python run.py
```

This will create the SQLite database with all required tables.

### 3. Create Admin User

```bash
python create_admin.py
```

This creates the default admin account:

- **Username:** admin
- **Password:** Admin@123

### 4. Seed Security Rules

```bash
python seed_rules.py
```

This creates 11 predefined rules (5 Brute Force + 6 DDoS)

### 5. Run the Application

```bash
python run.py
```

Access the application at: http://127.0.0.1:5000

## Milestone 1 Deliverables ✅

### RBAC Implementation

- ✅ **Admin Role** - Manage user accounts, view summary reports, manage all system data
- ✅ **Security Analyst Role** - Add/edit attack types, create/edit decision rules, analyze alerts
- ✅ **IT Operator Role (Viewer)** - Review alerts, view incident history, read-only access

### Database Schema

- ✅ **users** - Security team members with roles (admin/analyst/viewer)
- ✅ **attack_types** - Brute Force and DDoS attack definitions
- ✅ **rules** - If-then cybersecurity rules with JSON conditions
- ✅ **alerts** - Incoming security alerts with raw data
- ✅ **incidents** - Processed incidents with recommendations
- ✅ **incident_history** - Audit trail of actions taken

### Authentication System

- ✅ Login/Logout functionality
- ✅ Session-based authentication
- ✅ Password hashing with Werkzeug
- ✅ Role-based user system (admin, analyst, viewer)
- ✅ Last login tracking

### User Management

- ✅ CRUD operations for users
- ✅ Role assignment
- ✅ Password strength validation
- ✅ Active/Inactive status

### Dashboard

- ✅ Security dashboard with placeholder statistics
- ✅ Quick action buttons
- ✅ User profile display
- ✅ Navigation menu

## Milestone 2 Deliverables ✅

### Attack Type Management

- ✅ CRUD operations for attack types (Security Analyst access)
- ✅ Brute Force and DDoS attack type definitions
- ✅ Severity level assignment (1-10)
- ✅ Active/Inactive status management

### Rule Management System

- ✅ **11 Security Rules Created:**
  - 5 Brute Force attack rules (failed logins, account lockouts, rate limiting)
  - 6 DDoS attack rules (traffic spikes, request floods, protocol patterns)
- ✅ JSON-based flexible rule conditions
- ✅ JSON-based action definitions
- ✅ Priority system (high/medium/low)
- ✅ Severity scoring (1-10)
- ✅ Rule CRUD interface for analysts
- ✅ Rule validation service

## Milestone 3 Deliverables ✅

### Inference Engine

- ✅ **Core Analysis Engine** (`inference_engine.py`):
  - `analyze_alert()` - Main orchestrator for alert processing
  - `match_rules()` - Pattern matching with 70% condition threshold
  - `evaluate_conditions()` - Supports numeric (>=, <=, >, <, ==), boolean, string, list comparisons
  - `prioritize_actions()` - Combines actions by priority (high=3, medium=2, low=1)
  - `calculate_confidence()` - Multi-factor scoring:
    - Base confidence: 40 points
    - Match score: up to 30 points
    - Priority bonus: up to 20 points
    - Severity factor: up to 10 points
  - `generate_explanation()` - Human-readable analysis with matched rules and rationale

### Alert Management System

- ✅ **Alert Service** (`alert_service.py`):

  - CRUD operations for alerts
  - Status management (new/processed/ignored)
  - Alert filtering capabilities

- ✅ **Alert Forms** (`alert_forms.py`):

  - IP address validation
  - JSON raw_data validation
  - Severity selection

- ✅ **Alert Routes** (`alert_routes.py`):

  - List all alerts with status filtering
  - View alert details with analysis results
  - Submit new alerts (manual testing)
  - Automatic analysis on submission
  - Re-analyze existing alerts (admin/analyst only)

- ✅ **Alert Templates:**
  - `alerts/index.html` - Filterable list with status tabs, severity badges
  - `alerts/detail.html` - Alert info + incident analysis with confidence visualization
  - `alerts/create.html` - Submission form with sample JSON for Brute Force & DDoS

### Incident Processing

- ✅ Automatic incident creation on alert submission
- ✅ Confidence scoring (0-100)
- ✅ Recommended actions generation
- ✅ Detailed explanation of analysis
- ✅ Attack type identification
- ✅ Matched rules tracking

## Project Structure

```
MID-TERM/
├── app/
│   ├── models/          # All 6 database models
│   │   ├── user.py
│   │   ├── attack_type.py
│   │   ├── rule.py
│   │   ├── alert.py
│   │   ├── incident.py
│   │   └── incident_history.py
│   ├── forms/           # WTForms for all entities
│   │   ├── auth_forms.py
│   │   ├── user_forms.py
│   │   ├── attack_type_forms.py
│   │   ├── rule_forms.py
│   │   └── alert_forms.py
│   ├── routes/          # Blueprints for all modules
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── user_routes.py
│   │   ├── attack_type_routes.py
│   │   ├── rule_routes.py
│   │   └── alert_routes.py
│   ├── services/        # Business logic layer
│   │   ├── user_service.py
│   │   ├── attack_type_service.py
│   │   ├── rule_service.py
│   │   ├── alert_service.py
│   │   └── inference_engine.py  # Core reasoning engine
│   └── templates/       # HTML templates
│       ├── auth/
│       ├── dashboard/
│       ├── users/
│       ├── attack_types/
│       ├── rules/
│       └── alerts/
├── instance/            # SQLite database (auto-created)
├── config.py           # Database configuration
├── create_admin.py     # Admin user creation script
├── seed_rules.py       # Security rules seeding script
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

## Default Login Credentials

**Username:** admin  
**Password:** Admin@123

⚠️ **Change the password after first login!**

## Features Implemented

### Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing (pbkdf2:sha256)
- ✅ Session-based authentication
- ✅ Active/Inactive user status

### Database Models

All 6 tables with proper relationships:

1. User (with role field)
2. AttackType (Brute Force, DDoS)
3. Rule (JSON conditions & actions)
4. Alert (JSON raw data storage)
5. Incident (with confidence scoring)
6. IncidentHistory (audit trail)

## Next Steps (Milestone 4)

- [ ] Enhance dashboard with real-time statistics
- [ ] Add Chart.js visualizations (attack distribution, timeline)
- [ ] Build incident history interface for all users
- [ ] Implement incident status workflow (new → analyzing → pending → resolved)
- [ ] Add search and filter functionality
- [ ] Create reporting features

## Database Schema

### users

- id, username, email, full_name, **role**, is_active, password_hash, created_at, updated_at, **last_login**

### attack_types

- id, name, description, severity_level, is_active

### rules

- id, name, attack_type_id, **conditions (JSON)**, **actions (JSON)**, priority, severity_score, is_active

### alerts

- id, timestamp, source_ip, destination_ip, alert_type, severity, **raw_data (JSON)**, status

### incidents

- id, alert_id, attack_type_id, **matched_rules (JSON)**, **recommended_actions (JSON)**, confidence_score, explanation, status, assigned_to

### incident_history

- id, incident_id, action_taken, notes, performed_by, timestamp

## Testing

Run the application and verify:

1. **Authentication:**
   - Login with admin credentials (admin/Admin@123)
   - Role-based access control working
2. **User Management (Admin only):**

   - Create users with different roles
   - Edit user details
   - View user list

3. **Attack Types (Analyst/Admin):**

   - Create/edit attack types
   - View attack type list
   - Manage severity levels

4. **Rules (Analyst/Admin):**

   - Create security rules with JSON conditions
   - Edit existing rules
   - View all 11 seeded rules
   - Test rule priority system

5. **Alerts (All roles):**

   - Submit new alert with sample JSON
   - View automatic analysis results
   - Check confidence score and recommendations
   - Filter alerts by status
   - Re-analyze alerts (Admin/Analyst)

6. **Inference Engine:**
   - Submit Brute Force alert → Verify rule matching
   - Submit DDoS alert → Verify rule matching
   - Check confidence scoring accuracy
   - Verify explanation generation

## Notes

- SQLite database automatically created on first run
- All tables include proper foreign key relationships
- JSON fields allow flexible rule storage
- Session-based authentication (no external auth library needed)
- Bootstrap 5 responsive UI

---

**Status:** Milestone 3 Complete ✅  
**Current Milestone:** Dashboard & Alert Management (Milestone 4)  
**Last Updated:** December 29, 2025

## Key Features Summary

- ✅ **11 Security Rules** - 5 Brute Force + 6 DDoS attack patterns
- ✅ **Pattern Matching** - 70% threshold with priority-based rule matching
- ✅ **Confidence Scoring** - Multi-factor algorithm (0-100 scale)
- ✅ **Automatic Analysis** - Instant alert processing with incident creation
- ✅ **RBAC System** - Three-tier access control (Admin, Analyst, Viewer)
- ✅ **JSON Flexibility** - Dynamic rule conditions and alert data storage
- ✅ **Action Recommendations** - Priority-based action selection and combination
