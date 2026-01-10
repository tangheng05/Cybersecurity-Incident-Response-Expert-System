# Cybersecurity Incident Response Expert System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)


> An automated incident response expert system that analyzes security alerts using if-then rules and provides actionable recommendations for handling Brute Force and DDoS attacks.



## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Quick Start](#-quick-start)
- [Running Tests](#-running-tests)
- [User Guide](#-user-guide)
- [Complete Feature List](#-complete-feature-list)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Security Features](#-security-features)
- [Inference Engine](#-inference-engine)
- [Technologies Used](#-technologies-used)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🎯 Project Overview

Built with Flask, SQLAlchemy, and a custom inference engine, this system provides:

- **Real-time threat detection** with pattern matching
- **Automated incident response** with confidence scoring
- **Role-based access control** for security teams
- **Comprehensive audit trails** for compliance

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Cybersecurity-Incident-Response-Expert-System.git
cd Cybersecurity-Incident-Response-Expert-System
```

2. **Create virtual environment** (recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize database**

```bash
python run.py
# Press Ctrl+C after database is created
```

5. **Create admin user**

```bash
python create_admin.py
```

6. **Seed security rules**

```bash
python seed_rules.py
```

7. **Run the application**

```bash
python run.py
```

8. **Access the system**

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

### 🔑 Default Credentials

| Username | Password    |
| -------- | ----------- |
| `admin`  | `Admin@123` |

> ⚠️ **Important:** Change the default password after your first login!

## 🧪 Running Tests

Run the complete test suite:

```bash
pytest
```

Run specific test files:

```bash
# Test models
pytest app/tests/test_models.py

# Test services
pytest app/tests/test_services.py

# Test attack simulations
pytest app/tests/test_attack_simulations.py
```

Run with verbose output and detailed information:

```bash
pytest -v
pytest -v --tb=long  # With full traceback
```

View test coverage:

```bash
pytest --cov=app --cov-report=html
```

## 📚 User Guide

### 👨‍💼 For Admins

- **User Management** - Create analysts and viewers
- **Full System Access** - All CRUD operations
- **Monitor All Activity** - Dashboard with real-time stats

### 🔍 For Analysts (Security Staff)

- **Manage Attack Types** - Create/edit attack definitions
- **Create Rules** - Define detection patterns with JSON
- **Analyze Alerts** - Submit and re-analyze security alerts
- **Track Incidents** - Update status, add notes, assign tasks

### 👁️ For Viewers (IT Operators)

- **View Alerts** - Monitor incoming security alerts
- **Read Incident Details** - Access analysis results
- **Review History** - Check incident audit trail

## 📊 Complete Feature List

### ✅ Milestone 1 - Project Setup & Database

- User authentication (login/logout)
- Password hashing with Werkzeug
- RBAC implementation (admin, analyst, viewer)
- 6 database tables with relationships
- User management CRUD
- Dashboard interface

### ✅ Milestone 2 - Knowledge Base

- Attack type management (Brute Force, DDoS)
- Rule management system (CRUD operations)
- 11 predefined security rules
- JSON-based flexible rule conditions
- Priority system (high/medium/low)
- Severity scoring (1-10)

### ✅ Milestone 3 - Inference Engine

- Core reasoning engine
- Pattern matching (70% threshold)
- Confidence scoring (0-100)
- Action prioritization
- Explanation generation
- Alert management interface
- Automatic incident creation

### ✅ Milestone 4 - Dashboard & Incident Management

- Real-time statistics dashboard
- Chart.js visualizations (pie & bar charts)
- Recent alerts feed
- Incident management routes
- Status workflow (new → analyzing → pending → resolved)
- Action tracking with history
- Incident assignment system

### ✅ Milestone 5 - Testing & Deployment

- Pytest configuration
- Model tests (6 models)
- Service layer tests
- Inference engine tests
- Attack simulation tests (Brute Force & DDoS)
- Edge case testing
- Complete documentation

## 🏗️ Project Structure

```
Cybersecurity-Incident-Response-Expert-System/
├── app/
│   ├── __init__.py
│   ├── models/              # Database models (6 tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── attack_type.py
│   │   ├── rule.py
│   │   ├── alert.py
│   │   ├── incident.py
│   │   └── incident_history.py
│   ├── forms/               # WTForms validation
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── user_forms.py
│   │   ├── attack_type_forms.py
│   │   ├── rule_forms.py
│   │   └── alert_forms.py
│   ├── routes/              # Flask blueprints
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── user_routes.py
│   │   ├── attack_type_routes.py
│   │   ├── rule_routes.py
│   │   ├── alert_routes.py
│   │   ├── incident_routes.py
│   │   └── role_routes.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── attack_type_service.py
│   │   ├── rule_service.py
│   │   ├── alert_service.py
│   │   └── inference_engine.py
│   ├── templates/           # Jinja2 templates
│   │   ├── layouts/
│   │   │   └── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   ├── users/           # 6 templates
│   │   ├── attack_types/    # 5 templates
│   │   ├── rules/           # 5 templates
│   │   ├── alerts/          # 3 templates
│   │   ├── incidents/       # 2 templates
│   │   └── roles/           # 2 templates
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   ├── tests/               # Pytest suite
│   │   ├── conftest.py
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_attack_simulations.py
│   └── utils/
├── instance/                # SQLite database (auto-created)
│   └── cybersecurity.db
├── .venv/                   # Virtual environment
├── config.py               # Configuration
├── extensions.py           # Flask extensions
├── create_admin.py         # Admin creation script
├── seed_rules.py           # Rules seeding script
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
├── run.py                  # Entry point
└── README.md              # This file
```

## 🗄️ Database Schema

<details>
<summary>Click to expand database tables</summary>

### users

```sql
id, username, email, full_name, role, is_active,
password_hash, created_at, updated_at, last_login
```

### attack_types

```sql
id, name, description, severity_level, is_active
```

### rules

```sql
id, name, attack_type_id, conditions (JSON),
actions (JSON), priority, severity_score, is_active
```

### alerts

```sql
id, timestamp, source_ip, destination_ip, alert_type,
severity, raw_data (JSON), status, created_at
```

### incidents

```sql
id, alert_id, attack_type_id, matched_rules (JSON),
recommended_actions (JSON), confidence_score, explanation,
status, assigned_to, created_at, updated_at, resolved_at
```

### incident_history

```sql
id, incident_id, action_taken, notes,
performed_by, timestamp
```

</details>

## 🔒 Security Features

- **Password Hashing** - pbkdf2:sha256 with Werkzeug
- **CSRF Protection** - All forms protected
- **Session Security** - Secure session management
- **Input Validation** - Server-side validation on all inputs
- **SQL Injection Prevention** - SQLAlchemy ORM
- **RBAC** - Three-tier access control

## 🎯 Inference Engine

The heart of the system. Analyzes alerts using:

| Component                  | Description                                 |
| -------------------------- | ------------------------------------------- |
| **Pattern Matching**       | 70% condition threshold for rule activation |
| **Confidence Scoring**     | Multi-factor algorithm (0-100)              |
| **Action Prioritization**  | High → Medium → Low                         |
| **Explanation Generation** | Human-readable analysis                     |

### Confidence Score Calculation

```
Base confidence:    40 points
Match score:        up to 30 points
Priority bonus:     up to 20 points
Severity factor:    up to 10 points
─────────────────────────────────
Total:              0-100 points
```

## 📝 Sample Usage

### Submitting a Brute Force Alert

<details>
<summary>Click to expand example</summary>

**Request:**

```json
{
  "failed_attempts": 10,
  "time_window": 120,
  "source_ip": "192.168.1.100",
  "target_username": "admin"
}
```

**Expected Result:**

```json
{
  "confidence": 85,
  "attack_type": "Brute Force",
  "actions": ["block_ip", "alert_security_team", "log_incident"],
  "explanation": "Detected brute force attack based on 10 failed login attempts..."
}
```

</details>

## 🔧 Configuration

Edit `config.py` to customize:

- Database URI
- Secret key
- Debug mode
- Other Flask settings

## 📖 Additional Documentation

- **PROJECT_MILESTONES.md** - Detailed milestone tracking
- **CODEBASE_STRUCTURE.md** - Complete technical documentation

## 🐛 Troubleshooting

<details>
<summary><b>Database Issues</b></summary>

```bash
# Delete and recreate database
rm instance/cybersecurity.db      # Linux/Mac
del instance\cybersecurity.db     # Windows

# Recreate everything
python run.py
python create_admin.py
python seed_rules.py
```

</details>

<details>
<summary><b>Import Errors</b></summary>

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# If still failing, recreate virtual environment
deactivate
rm -rf .venv      # Linux/Mac
rmdir /s .venv    # Windows
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Test Failures</b></summary>

```bash
# Run with verbose output
pytest -v --tb=long

# Run specific test file
pytest app/tests/test_models.py -v

# Check test coverage
pytest --cov=app --cov-report=html
```

</details>

<details>
<summary><b>Port Already in Use</b></summary>

```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

</details>

## 🎓 Technologies Used

| Category           | Technologies                   |
| ------------------ | ------------------------------ |
| **Backend**        | Flask 2.3.3, Python 3.8+       |
| **Database**       | SQLite, SQLAlchemy 3.1.1       |
| **Forms**          | Flask-WTF 1.1.1, WTForms 3.1.2 |
| **Authentication** | Werkzeug 2.3.7 (pbkdf2:sha256) |
| **Frontend**       | Bootstrap 5, Chart.js          |
| **Testing**        | Pytest 7.4.0                   |

## 📊 Test Coverage

- **Model Tests:** 6 models fully tested
- **Service Tests:** All services with edge cases
- **Integration Tests:** Brute Force & DDoS simulations
- **Edge Cases:** Empty data, inactive rules, multiple matches

## ✨ Key Achievements

- ✅ **11 Security Rules** - 5 Brute Force + 6 DDoS detection patterns
- ✅ **Sub-second Processing** - Alert analysis < 1 second
- ✅ **70% Match Threshold** - Pattern matching accuracy
- ✅ **Multi-factor Scoring** - Comprehensive confidence calculation
- ✅ **Complete Audit Trail** - Full incident history tracking
- ✅ **Real-time Dashboard** - Live charts with Chart.js
- ✅ **Comprehensive Tests** - Full pytest coverage
- ✅ **RBAC Implementation** - Three-tier access control

## 📊 Test Coverage

| Test Category         | Coverage                                     |
| --------------------- | -------------------------------------------- |
| **Model Tests**       | 6 models fully tested                        |
| **Service Tests**     | All services with edge cases                 |
| **Integration Tests** | Brute Force & DDoS simulations               |
| **Edge Cases**        | Empty data, inactive rules, multiple matches |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or issues, please:

- Open an issue on GitHub
- Refer to the documentation in `CODEBASE_STRUCTURE.md`
- Check the `PROJECT_MILESTONES.md` for detailed feature tracking

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap for responsive UI components
- Chart.js for visualization capabilities

---

<div align="center">

**Project Status:** ✅ Complete & Production Ready  
**Version:** 1.0.0  
**Last Updated:** January 10, 2026

Made with ❤️ for cybersecurity incident response

[⬆ Back to Top](#cybersecurity-incident-response-expert-system)

</div>
