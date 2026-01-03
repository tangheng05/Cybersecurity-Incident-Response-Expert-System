# Cybersecurity Incident Response Expert System

## Project Milestones & Timeline

**Project Name:** Cybersecurity Incident Response Expert System  
**Date Created:** December 29, 2025  
**Project Type:** Expert System with If-Then Rules Engine  
**Focus:** Brute Force & DDoS Attack Detection and Response

---

## User Roles - RBAC

## Admin: Manage user accounts and view summary

reports.
Staff (Security Analyst): Add or edit attack types and
create decision rules using the Dashboard.
End User (IT Operator): Review alerts, receive
recommended responses, and check incident history

## 📋 Project Overview

### **Objective**

Build an automated incident response expert system that analyzes security alerts using if-then rules and provides actionable recommendations to security teams for handling Brute Force and DDoS attacks.

### **In Scope**

- ✅ Knowledge Base with cybersecurity rules
- ✅ Inference Engine for alert analysis and action suggestion
- ✅ Dashboard for monitoring alerts and responses
- ✅ Focus on 2 attack types: **Brute Force** and **DDoS**

### **Out of Scope**

- ❌ Image recognition for attack detection
- ❌ IoT device integration

### **Technology Stack**

- **Backend:** Flask (Python), Flask-WTF, Werkzeug
- **Database:** SQLite with JSON for flexible rule storage
- **ORM:** SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Architecture:** Client-Server with Inference Engine

---

## 🎯 Project Milestones

### **Milestone 1: Project Setup & Database Design** ⏱️ Week 1

#### **Goals**

- Set up development environment
- Design database schema
- Create project structure
- Implement basic authentication system

#### **Deliverables**

- [x] Flask application skeleton with proper folder structure
- [x] SQLite database schema for:
  - Users (security team members)
  - Attack Types (Brute Force, DDoS)
  - Rules (if-then cybersecurity rules)
  - Alerts (incoming security alerts)
  - Incidents (processed incidents with responses)
  - Incident History (audit trail)
- [x] User authentication system (login/logout)
- [x] Password hashing with Werkzeug
- [x] Database models with SQLAlchemy ORM

#### **Tasks**

1. Initialize Flask project structure
2. Install dependencies (Flask, Flask-WTF, SQLAlchemy, etc.)
3. Create database models:
   - User model (username, password_hash, role, email)
   - AttackType model (name, description, severity_level)
   - Rule model (condition, action, priority, attack_type_id)
   - Alert model (timestamp, source_ip, alert_type, severity, raw_data)
   - Incident model (alert_id, attack_type, status, recommended_action)
   - IncidentHistory model (incident_id, action_taken, timestamp)
4. Set up SQLAlchemy database connection
5. Create user registration and login forms with Flask-WTF
6. Implement secure password hashing
7. Create basic login/logout routes

#### **Success Criteria**

- ✅ Database tables created successfully
- ✅ Users can register and login securely
- ✅ Passwords are properly hashed
- ✅ Application runs without errors

---

### **Milestone 2: Knowledge Base Development** ⏱️ Week 2

#### **Goals**

- Build comprehensive rule set for Brute Force and DDoS attacks
- Implement CRUD operations for rules management
- Create rule storage with JSON flexibility
- Define attack patterns and thresholds

#### **Deliverables**

- [x] Knowledge Base with if-then rules for:
  - **Brute Force Attacks:**
    - Multiple failed login attempts from same IP
    - Multiple failed attempts across different accounts
    - Login attempts outside business hours
    - Geographic anomalies
  - **DDoS Attacks:**
    - Traffic volume thresholds
    - Request rate patterns
    - Source IP distribution
    - Protocol-specific indicators
- [x] Rules management interface (Create, Read, Update, Delete)
- [x] Attack Types management interface (CRUD for Security Analysts)
- [x] Rule priority system
- [x] Rule validation logic
- [x] JSON storage for flexible rule conditions
- [x] RBAC implementation (admin, analyst, viewer roles)

#### **Tasks**

1. Design rule structure schema (JSON format)
   ```json
   {
     "rule_id": 1,
     "name": "Brute Force - Multiple Failed Logins",
     "attack_type": "brute_force",
     "conditions": {
       "failed_attempts": ">= 5",
       "time_window": "5 minutes",
       "same_ip": true
     },
     "actions": ["block_ip", "alert_admin", "log_incident"],
     "priority": "high",
     "severity": 8
   }
   ```
2. Create rule templates for common attack patterns
3. Build rules management UI (admin only)
4. Implement rule CRUD operations
5. Create rule validation service
6. Populate initial rule set (minimum 10 rules total)
7. Test rule retrieval and filtering

#### **Success Criteria**

- ✅ At least 5 rules defined for Brute Force attacks
- ✅ At least 5 rules defined for DDoS attacks
- ✅ Rules can be added, edited, and deleted
- ✅ Rules stored with JSON conditions for flexibility
- ✅ Rule priority system functional

---

### **Milestone 3: Inference Engine Implementation** ⏱️ Week 3

#### **Goals**

- Build core reasoning engine
- Implement pattern matching algorithm
- Create alert analysis logic
- Develop recommendation system

#### **Deliverables**

- [x] Inference Engine service that:
  - Analyzes incoming alerts
  - Matches alerts against rule conditions (70% threshold)
  - Evaluates multiple matching rules by priority
  - Generates recommended actions
  - Provides explanation for decisions
- [x] Alert processing pipeline
- [x] Rule evaluation algorithm (numeric, boolean, string comparisons)
- [x] Confidence scoring system (0-100 based on 4 factors)
- [x] Action recommendation logic with priority-based selection
- [x] Alert management interface (list, detail, create)
- [x] Automatic incident creation on alert submission
- [x] Alert filtering by status (new/processed/ignored)

#### **Tasks**

1. Create `InferenceEngine` class with core methods:
   - `analyze_alert(alert_data)` - Main analysis function
   - `match_rules(alert, rules)` - Pattern matching
   - `evaluate_conditions(alert, rule)` - Condition checking
   - `prioritize_actions(matched_rules)` - Action selection
   - `generate_explanation(matched_rules)` - Decision explanation
2. Implement condition evaluation logic:
   - Numeric comparisons (>=, <=, ==, !=)
   - Time window calculations
   - IP address matching
   - Rate calculations
3. Build alert preprocessing:
   - Parse raw alert data
   - Normalize data formats
   - Extract key metrics
4. Create confidence scoring based on:
   - Number of matching rules
   - Rule priority levels
   - Alert severity
5. Implement action recommendation engine
6. Generate human-readable explanations
7. Create unit tests for inference engine

#### **Success Criteria**

- ✅ Engine correctly identifies Brute Force attacks
- ✅ Engine correctly identifies DDoS attacks
- ✅ Multiple rules can match and be prioritized
- ✅ Recommendations are accurate and actionable
- ✅ Explanations are clear and understandable
- ✅ Processing time < 1 second per alert

---

### **Milestone 4: Dashboard & Alert Management** ⏱️ Week 4

#### **Goals**

- Create interactive security dashboard
- Implement alert monitoring interface
- Build incident response tracking
- Develop reporting features

#### **Deliverables**

- [ ] Security Dashboard with:
  - Real-time alert feed
  - Incident statistics (charts/graphs)
  - Active incidents list
  - Recent responses summary
- [ ] Alert Management Interface:
  - View all alerts (with filtering)
  - Alert details page
  - Manual alert submission (for testing)
  - Alert status tracking
- [ ] Incident Response Interface:
  - View recommended actions
  - Mark actions as taken
  - Add notes to incidents
  - Close/resolve incidents
- [ ] Reporting features:
  - Incident history log
  - Attack type distribution
  - Response time metrics

#### **Tasks**

1. Design dashboard layout (wireframes)
2. Create dashboard route and template
3. Build real-time alert display:
   - Auto-refresh or WebSocket updates
   - Color-coded by severity
   - Sortable and filterable
4. Implement statistics visualizations:
   - Chart.js or similar library
   - Attack type pie chart
   - Timeline of incidents
   - Severity distribution
5. Create alert submission form (manual testing)
6. Build incident detail pages:
   - Show matched rules
   - Display recommendations
   - Show explanation
   - Action buttons
7. Implement incident status workflow:
   - New → Analyzing → Pending Action → Resolved
8. Create incident history table
9. Add search and filter functionality
10. Style with CSS3 (responsive design)

#### **Success Criteria**

- ✅ Dashboard displays real-time alert information
- ✅ Users can view all incidents and their statuses
- ✅ Visualizations are clear and informative
- ✅ Interface is responsive and user-friendly
- ✅ Manual alert submission works correctly
- ✅ Incident workflow is intuitive

---

### **Milestone 5: Testing, Documentation & Deployment** ⏱️ Week 5

#### **Goals**

- Comprehensive system testing
- Performance optimization
- Complete documentation
- Prepare for deployment

#### **Deliverables**

- [ ] Test Suite:
  - Unit tests for all models
  - Service layer tests
  - Inference engine tests
  - Integration tests
  - End-to-end workflow tests
- [ ] Documentation:
  - User manual
  - Admin guide
  - API documentation
  - System architecture diagram
  - Rule creation guide
- [ ] Performance optimization
- [ ] Security audit
- [ ] Deployment package

#### **Tasks**

1. Write unit tests (pytest):
   - Model tests (User, Alert, Rule, Incident)
   - Service tests (InferenceEngine, AlertService)
   - Form validation tests
   - Authentication tests
2. Create test scenarios:
   - Brute Force attack simulation
   - DDoS attack simulation
   - Multiple concurrent alerts
   - Edge cases and error handling
3. Performance testing:
   - Load testing with multiple alerts
   - Database query optimization
   - Caching strategy
4. Security review:
   - SQL injection prevention
   - XSS protection
   - CSRF token validation
   - Password security
   - Input sanitization
5. Write documentation:
   - README.md with setup instructions
   - User guide with screenshots
   - Rule creation tutorial
   - System architecture document
6. Create sample data and demo scenarios
7. Code cleanup and refactoring
8. Deployment preparation:
   - Environment configuration
   - Production settings
   - Backup strategy

#### **Success Criteria**

- ✅ All tests passing (>80% code coverage)
- ✅ No critical security vulnerabilities
- ✅ System handles 100+ alerts without performance degradation
- ✅ Complete documentation available
- ✅ Application ready for deployment
- ✅ Demo scenarios prepared

---

## 📊 Timeline Summary

| Milestone                   | Duration    | Start Date | End Date | Status         |
| --------------------------- | ----------- | ---------- | -------- | -------------- |
| 1: Project Setup & Database | 1 week      | Week 1     | Week 1   | ✅ Completed   |
| 2: Knowledge Base           | 1 week      | Week 2     | Week 2   | ✅ Completed   |
| 3: Inference Engine         | 1 week      | Week 3     | Week 3   | ✅ Completed   |
| 4: Dashboard & Alerts       | 1 week      | Week 4     | Week 4   | 🟡 In Progress |
| 5: Testing & Deployment     | 1 week      | Week 5     | Week 5   | ⚪ Not Started |
| **Total**                   | **5 weeks** | -          | -        | -              |

**Legend:**

- ✅ Completed
- 🟢 On Track
- 🟡 In Progress
- 🟠 At Risk
- 🔴 Delayed
- ⚪ Not Started

---

## 🗄️ Database Schema Design

### **Tables Overview**

#### **1. users**

```sql
- id (PK)
- username (unique)
- email (unique)
- password_hash
- role (admin/analyst/viewer)
- is_active
- created_at
- last_login
```

#### **2. attack_types**

```sql
- id (PK)
- name (brute_force/ddos)
- description
- severity_level (1-10)
- is_active
```

#### **3. rules**

```sql
- id (PK)
- name
- attack_type_id (FK)
- conditions (JSON)
- actions (JSON)
- priority (high/medium/low)
- severity_score (1-10)
- is_active
- created_at
- updated_at
```

#### **4. alerts**

```sql
- id (PK)
- timestamp
- source_ip
- destination_ip
- alert_type
- severity
- raw_data (JSON)
- status (new/processed/ignored)
- created_at
```

#### **5. incidents**

```sql
- id (PK)
- alert_id (FK)
- attack_type_id (FK)
- matched_rules (JSON array of rule IDs)
- recommended_actions (JSON)
- confidence_score (0-100)
- explanation (TEXT)
- status (new/analyzing/pending/resolved)
- assigned_to (FK to users)
- created_at
- updated_at
- resolved_at
```

#### **6. incident_history**

```sql
- id (PK)
- incident_id (FK)
- action_taken
- notes
- performed_by (FK to users)
- timestamp
```

---

## 🎯 Key Features by Milestone

### **Milestone 1 Features**

- User registration and authentication
- Secure password management
- Database initialization
- Basic routing structure

### **Milestone 2 Features**

- Rule management interface
- Pre-defined attack rules
- JSON-based flexible rule storage
- Rule validation

### **Milestone 3 Features**

- Alert analysis engine
- Pattern matching algorithm
- Action recommendation
- Decision explanation generator

### **Milestone 4 Features**

- Interactive dashboard
- Alert monitoring
- Incident tracking
- Reporting and analytics

### **Milestone 5 Features**

- Comprehensive testing
- Performance optimization
- Full documentation
- Deployment readiness

---

## 🔧 Technical Requirements

### **Development Environment**

- Python 3.8+
- Flask 2.3+
- SQLite 3
- Modern web browser (Chrome, Firefox, Edge)

### **Dependencies**

```txt
Flask==2.3.3
Flask-WTF==1.1.1
Flask-SQLAlchemy==3.1.1
WTForms==3.1.2
Werkzeug==2.3.7
email-validator==2.1.0.post1
pytest==7.4.0 (for testing)
```

### **Frontend Libraries**

- Bootstrap 5 (CSS framework)
- Chart.js (data visualization)
- jQuery (optional, for AJAX)

---

## 📈 Success Metrics

### **Functional Metrics**

- ✅ 100% of defined rules working correctly
- ✅ <1 second alert processing time
- ✅ >95% accurate attack detection
- ✅ Zero critical security vulnerabilities

### **Quality Metrics**

- ✅ >80% code test coverage
- ✅ All user workflows functional
- ✅ Responsive design on desktop and tablet
- ✅ Clear documentation for all features

### **User Experience Metrics**

- ✅ Intuitive dashboard navigation
- ✅ <3 clicks to view incident details
- ✅ Clear action recommendations
- ✅ Comprehensive incident explanations

---

## 🚨 Risk Management

### **Technical Risks**

| Risk                         | Impact | Mitigation                                          |
| ---------------------------- | ------ | --------------------------------------------------- |
| Inference engine complexity  | High   | Start with simple rules, iterate                    |
| Performance with many alerts | Medium | Implement caching, optimize queries                 |
| Rule conflicts               | Medium | Clear priority system, testing                      |
| Database scalability         | Low    | SQLite sufficient for demo, document migration path |

### **Project Risks**

| Risk               | Impact | Mitigation                      |
| ------------------ | ------ | ------------------------------- |
| Scope creep        | High   | Strict focus on 2 attack types  |
| Timeline delays    | Medium | Weekly checkpoints, buffer time |
| Testing coverage   | Medium | Test-driven approach from start |
| Documentation gaps | Low    | Document as you build           |

---

## 📝 Deliverable Checklist

### **Code Deliverables**

- [ ] Complete Flask application
- [ ] Database with sample data
- [ ] All models and relationships
- [ ] Inference engine implementation
- [ ] Dashboard interface
- [ ] Test suite

### **Documentation Deliverables**

- [ ] README.md
- [ ] User Manual
- [ ] System Architecture Document
- [ ] Rule Creation Guide
- [ ] API Documentation (if applicable)
- [ ] Deployment Guide

### **Presentation Deliverables**

- [ ] Demo scenarios prepared
- [ ] Brute Force attack simulation
- [ ] DDoS attack simulation
- [ ] Dashboard walkthrough
- [ ] Rule management demo
- [ ] Presentation slides

---

## 🎓 Learning Objectives Alignment

### **Expert Systems Concepts**

- ✅ Knowledge representation (rules)
- ✅ Inference engine design
- ✅ Forward chaining reasoning
- ✅ Explanation generation
- ✅ Conflict resolution (rule priority)

### **Software Engineering**

- ✅ MVC architecture
- ✅ Database design
- ✅ RESTful routing
- ✅ Security best practices
- ✅ Testing methodologies

### **Cybersecurity Domain**

- ✅ Attack pattern recognition
- ✅ Incident response workflows
- ✅ Threat analysis
- ✅ Security monitoring

---

## 📞 Project Contacts & Resources

### **Team Roles** (Update as needed)

- **Project Lead:** [Name]
- **Backend Developer:** [Name]
- **Frontend Developer:** [Name]
- **Database Designer:** [Name]
- **QA/Tester:** [Name]

### **Resources**

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Brute Force Attack Patterns](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks)
- [DDoS Mitigation Techniques](https://www.cloudflare.com/learning/ddos/ddos-mitigation/)

---

**Last Updated:** December 29, 2025  
**Status:** Milestone 3 - Completed ✅ | Milestone 4 - In Progress 🟡  
**Next Milestone:** Dashboard enhancements, Incident tracking, Reporting features

---

**End of Milestones Document**
