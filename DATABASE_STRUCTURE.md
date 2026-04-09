# Database Structure & Location - OptiAsset Management System

## 📍 Database Location

### Physical Location
```
Type: PostgreSQL 15 (Docker Container)
Host: localhost
Port: 5433
Database: asset_management
Username: postgres
Password: password
```

### Docker Configuration
Located in: `docker-compose.yml`
```yaml
services:
  db:
    image: postgres:15
    ports:
      - "5433:5432"
    environment:
      POSTGRES_DB: asset_management
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
```

---

## 🗄️ Database Tables (Actual Current State)

### Current Database Contents (Live Data)

**As of:** March 7, 2026

#### 📋 TABLE: roles (2 records)
| ID | Name | Permissions |
|----|------|-------------|
| 211c4bbd-097c-47bb-8f8d-8f5690e5bf9f | Admin | ["all"] |
| f1f81eda-231a-4fc0-9768-5185f63c5eea | Employee | ["view:my_gear", "view:assets"] |

#### 👥 TABLE: users (2 records)
| ID | Name | Email | Role ID | Is Active | Created |
|----|------|-------|---------|-----------|---------|
| ef892efa-910f-4f8e-891f-55cdf701f030 | OptiAsset Admin | admin@optiasset.com | 211c4bbd... (Admin) | True | 2026-03-07 11:08:27 |
| 5e81929e-3cff-4e3e-a580-6be58e06ccca | John Employee | employee@optiasset.com | f1f81eda... (Employee) | True | 2026-03-07 11:51:39 |

#### 💼 TABLE: assets (1 record)
| ID | Asset Tag | Name | Status | Is Active | Created |
|----|-----------|------|--------|-----------|---------|
| 15b5988d-2ab5-48d5-80f8-3aa315cc539f | TEST-001 | Test Laptop | Available | True | 2026-03-07 12:40:31 |

#### 📦 TABLE: assignments (0 records)
*No assignments yet*

#### 📝 TABLE: asset_status_logs (0 records)
*No status changes logged yet*

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────────────┐
│       roles         │
├─────────────────────┤
│ id (PK) UUID        │
│ name VARCHAR        │
│ permissions TEXT[]  │
└─────────────────────┘
         ▲
         │ role_id (FK)
         │
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK) UUID        │
│ role_id (FK) UUID   │──┐
│ name VARCHAR        │  │
│ email VARCHAR       │  │
│ hashed_password     │  │
│ is_active BOOLEAN   │  │
│ created_at TIMESTAMP│  │
└─────────────────────┘  │
                         │
         ┌───────────────┘
         │ user_id (FK)
         │
┌─────────────────────┐
│   assignments       │
├─────────────────────┤
│ id (PK) UUID        │
│ user_id (FK) UUID   │
│ asset_id (FK) UUID  │
│ assigned_date TIMESTAMP
│ return_date TIMESTAMP
└─────────────────────┘
         ▲
         │ asset_id (FK)
         │
┌─────────────────────┐
│       assets        │
├─────────────────────┤
│ id (PK) UUID        │
│ asset_tag VARCHAR   │
│ name VARCHAR        │
│ status VARCHAR      │
│ is_active BOOLEAN   │
│ created_at TIMESTAMP│
└─────────────────────┘
         │
         │ asset_id (FK)
         ▼
┌─────────────────────┐
│ asset_status_logs   │
├─────────────────────┤
│ id (PK) UUID        │
│ asset_id (FK) UUID  │
│ old_status VARCHAR  │
│ new_status VARCHAR  │
│ changed_at TIMESTAMP│
└─────────────────────┘
```

---

## 🔧 How to Access Your Database

### Method 1: Python Script (Easiest) ✅ ALREADY CREATED

Run this to see all data:
```bash
cd "c:\Users\SKANDASHRI S N\tessacloud\asset-management-system"
python view_database.py
```

**Output shows:** All tables with their current data

---

### Method 2: pgAdmin (GUI Tool)

1. **Download:** https://www.pgadmin.org/download/
2. **Install and open pgAdmin**
3. **Right-click "Servers" → Create → Server**
4. **Connection tab:**
   ```
   Host name/address: localhost
   Port: 5433
   Maintenance database: asset_management
   Username: postgres
   Password: password
   ```
5. **Click "Save"**
6. **Browse your database visually!**

---

### Method 3: Command Line (psql via Docker)

```bash
# Connect to your database
docker exec -it <container-name> psql -U postgres -d asset_management

# Or directly via psql if installed:
psql -h localhost -p 5433 -U postgres -d asset_management
```

---

### Method 4: Direct SQL Queries (Advanced)

Create a query script:

```python
# query_database.py
from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Example: Get all users with their roles
query = text("""
    SELECT 
        u.id,
        u.name,
        u.email,
        r.name as role_name,
        r.permissions
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
""")

result = db.execute(query).fetchall()
for row in result:
    print(dict(row))
```

---

## 📋 Table Schemas (Detailed)

### 1. roles
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    permissions TEXT[] DEFAULT '{}',
    -- No created_at in current model
);

-- Indexes
CREATE INDEX ix_roles_id ON roles;
CREATE INDEX ix_roles_name ON roles;
```

**Purpose:** Defines user roles with permission arrays  
**Current Records:** 2 (Admin, Employee)

---

### 2. users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID REFERENCES roles(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX ix_users_id ON users;
CREATE INDEX ix_users_email ON users;
CREATE INDEX ix_users_role_id ON users;
```

**Purpose:** System users with authentication  
**Current Records:** 2 (1 Admin, 1 Employee)

---

### 3. assets
```sql
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_tag VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Available',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX ix_assets_id ON assets;
CREATE INDEX ix_assets_asset_tag ON assets;
CREATE INDEX ix_assets_status ON assets;
```

**Purpose:** Company inventory tracking  
**Current Records:** 1 (Test Laptop)

---

### 4. assignments
```sql
CREATE TABLE assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP
);

-- Indexes
CREATE INDEX ix_assignments_id ON assignments;
CREATE INDEX ix_assignments_user_id ON assignments;
CREATE INDEX ix_assignments_asset_id ON assignments;
```

**Purpose:** Tracks asset-to-user assignments  
**Current Records:** 0

---

### 5. asset_status_logs
```sql
CREATE TABLE asset_status_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX ix_status_logs_id ON status_logs;
CREATE INDEX ix_status_logs_asset_id ON status_logs;
```

**Purpose:** Audit trail for asset status changes  
**Current Records:** 0

---

## 🎯 Database Relationships

### One-to-Many Relationships:
1. **roles → users**: One role can have many users
2. **users → assignments**: One user can have many assignments
3. **assets → assignments**: One asset can have many assignment records
4. **assets → status_logs**: One asset can have many status log entries

### Cascade Rules:
- **ON DELETE CASCADE**: When a user/asset is deleted, related assignments are also deleted
- **Soft Delete Preferred**: Set `is_active = FALSE` instead of hard delete

---

## 📊 Current Database Statistics

```
Total Roles:              2
Total Users:              2
  - Active Users:         2
  - Inactive Users:       0
Total Assets:             1
  - Available Assets:     1
  - Assigned Assets:      0
  - In Maintenance:       0
Total Assignments:        0
Total Status Logs:        0
```

---

## 🔍 How to View Specific Data

### View User's Role:
```python
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
user = db.query(User).filter(User.email == "admin@optiasset.com").first()
print(f"User: {user.name}")
print(f"Role: {user.role.name}")
print(f"Permissions: {user.role.permissions}")
```

### View Asset Status:
```python
from app.models import Asset

asset = db.query(Asset).filter(Asset.asset_tag == "TEST-001").first()
print(f"Asset: {asset.name}")
print(f"Status: {asset.status}")
print(f"Is Active: {asset.is_active}")
```

---

## 🛠️ Database Maintenance Commands

### Backup Database:
```bash
docker exec <container-name> pg_dump -U postgres asset_management > backup.sql
```

### Restore Database:
```bash
docker exec -i <container-name> psql -U postgres -d asset_management < backup.sql
```

### Reset Database (WARNING: Deletes all data):
```bash
# Stop containers
docker-compose down

# Remove volumes
docker volume rm asset-management-system_postgres_data

# Start fresh
docker-compose up -d db

# Run migration
python migrate_rbac.py
```

---

## 📁 Related Files

| File | Purpose | Location |
|------|---------|----------|
| `models.py` | SQLAlchemy models | `/app/models.py` |
| `database.py` | DB connection | `/app/database.py` |
| `migrate_rbac.py` | Creates roles/users | Root directory |
| `view_database.py` | View all data | Root directory |
| `docker-compose.yml` | DB container config | Root directory |
| `.env` | DB credentials | Root directory |

---

## 🚀 Quick Reference

**To see your database right now:**
```bash
cd "c:\Users\SKANDASHRI S N\tessacloud\asset-management-system"
python view_database.py
```

**Your test accounts:**
- Admin: admin@optiasset.com / admin123
- Employee: employee@optiasset.com / employee123

**Your test asset:**
- Asset Tag: TEST-001
- Name: Test Laptop
- Status: Available

---

*Last Updated: March 7, 2026*  
*Database Version: PostgreSQL 15*  
*ORM: SQLAlchemy 2.0*
