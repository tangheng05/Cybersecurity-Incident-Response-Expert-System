# Deployment Guide for Ubuntu Server

This guide will help you deploy the Cybersecurity Incident Response Expert System to your Ubuntu server with all necessary data.

## Prerequisites

On your Ubuntu server, ensure you have:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

## Option 1: Deploy with Default Seed Data (Recommended for Fresh Install)

### Step 1: Clone/Upload Your Application

```bash
# Upload your application to the server
# Or clone from git repository
cd /var/www  # or your preferred location
# git clone <your-repo-url>
cd Cybersecurity-Incident-Response-Expert-System
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

```bash
# Create instance directory
mkdir -p instance

# Initialize database tables
python3 -c "from app import create_app; app = create_app(); app.app_context().push(); from extensions import db; db.create_all()"
```

### Step 5: Seed Database with Default Data

```bash
# Add default attack types and security rules
python3 scripts/seed_data.py

# Create admin user
python3 scripts/create_admin.py
```

### Step 6: Run the Application

```bash
# For testing
python3 main.py

# For production (install gunicorn first)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

---

## Option 2: Migrate Existing Data from Local to Server

If you want to transfer your existing attack types and rules from your local machine to the server:

### Step 1: Export Data Locally (On Your Windows Machine)

```powershell
# In your local project directory with activated venv
python scripts/export_data.py
```

This creates JSON files in the `database_exports/` folder with timestamp:

- `attack_types_YYYYMMDD_HHMMSS.json`
- `rules_YYYYMMDD_HHMMSS.json`

### Step 2: Transfer Files to Server

```bash
# From your local machine, upload the exported files
scp database_exports/*.json user@your-server:/path/to/project/database_exports/
```

Or use SFTP/FileZilla to upload the files.

### Step 3: Import Data on Server

```bash
# On your Ubuntu server
cd /path/to/project
source venv/bin/activate

# Import the data
python3 scripts/import_data.py database_exports/attack_types_20260110_120000.json database_exports/rules_20260110_120000.json
```

Replace the filenames with your actual exported file names.

---

## Production Deployment with Nginx (Optional but Recommended)

### Step 1: Install Nginx

```bash
sudo apt install nginx -y
```

### Step 2: Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/cybersecurity-app
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your server IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/Cybersecurity-Incident-Response-Expert-System/app/static;
    }
}
```

### Step 3: Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/cybersecurity-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Create Systemd Service

```bash
sudo nano /etc/systemd/system/cybersecurity-app.service
```

Add this configuration:

```ini
[Unit]
Description=Cybersecurity Incident Response Expert System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/Cybersecurity-Incident-Response-Expert-System
Environment="PATH=/var/www/Cybersecurity-Incident-Response-Expert-System/venv/bin"
ExecStart=/var/www/Cybersecurity-Incident-Response-Expert-System/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app

[Install]
WantedBy=multi-user.target
```

### Step 5: Start the Service

```bash
sudo systemctl daemon-reload
sudo systemctl start cybersecurity-app
sudo systemctl enable cybersecurity-app
sudo systemctl status cybersecurity-app
```

---

## Troubleshooting

### Database Issues

```bash
# Check if database exists
ls -la instance/

# Reset database (WARNING: This deletes all data)
rm instance/cybersecurity.db
python3 -c "from app import create_app; app = create_app(); app.app_context().push(); from extensions import db; db.create_all()"
python3 scripts/seed_data.py
```

### Permission Issues

```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/Cybersecurity-Incident-Response-Expert-System
sudo chmod -R 755 /var/www/Cybersecurity-Incident-Response-Expert-System
sudo chmod 664 instance/cybersecurity.db
```

### View Application Logs

```bash
# If using systemd
sudo journalctl -u cybersecurity-app -f

# If running manually
tail -f /var/log/nginx/error.log
```

---

## Quick Reference Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Seed default data
python3 scripts/seed_data.py

# Create admin user
python3 scripts/create_admin.py

# Export data (run locally before migration)
python3 scripts/export_data.py

# Import data (run on server after uploading JSON files)
python3 scripts/import_data.py database_exports/attack_types_*.json database_exports/rules_*.json

# Restart service
sudo systemctl restart cybersecurity-app

# Check service status
sudo systemctl status cybersecurity-app
```

---

## Security Recommendations

1. **Change Default Admin Password**: If you used `create_admin.py --default`, change the password immediately
2. **Set Strong SECRET_KEY**: Set environment variable `SECRET_KEY` with a strong random value
3. **Enable HTTPS**: Use Let's Encrypt for free SSL certificates
4. **Set Up Firewall**: Configure UFW to only allow necessary ports
5. **Regular Backups**: Backup `instance/cybersecurity.db` regularly

```bash
# Example backup
cp instance/cybersecurity.db instance/backups/cybersecurity_$(date +%Y%m%d_%H%M%S).db
```
