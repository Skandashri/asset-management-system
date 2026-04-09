# Deactivation (Soft Delete) Demonstration

## 📊 Current Database State

### **Demonstration Summary**

This document shows how the **soft delete** pattern works in the OptiAsset system. Instead of permanently deleting records, we use an `is_active` flag to mark them as inactive.

---

## 🔄 What Was Demonstrated

### **1. User Deactivated: Frank Miller**

**Before:**
```
Name: Frank Miller
Email: frank@company.com
Role: Employee
is_active: True ✅
```

**After:**
```
Name: Frank Miller
Email: frank@company.com
Role: Employee
is_active: False ❌
```

**Database Record Still Exists:**
- ✅ Record preserved in database
- ✅ Historical data maintained
- ✅ Can be reactivated anytime
- ❌ Won't appear in API responses by default

---

### **2. Asset Deactivated: iPhone 13 Pro**

**Before:**
```
Asset Tag: IPHONE-13-001
Name: iPhone 13 Pro 256GB
Status: Available
is_active: True ✅
```

**After:**
```
Asset Tag: IPHONE-13-001
Name: iPhone 13 Pro 256GB
Status: Available
is_active: False ❌
```

**Database Record Still Exists:**
- ✅ Record preserved in database
- ✅ Audit trail maintained
- ✅ Can be reactivated anytime
- ❌ Won't appear in active inventory

---

## 📋 Final Database Counts

```
USERS:
├─ Total: 8
├─ Active: 7 ✅
└─ Inactive: 1 ❌ (Frank Miller)

ASSETS:
├─ Total: 13
├─ Active: 12 ✅
└─ Inactive: 1 ❌ (iPhone 13 Pro)

ASSIGNMENTS:
└─ Active Assignments: 5 (all assigned assets)
```

---

## 🔍 How to View in DBeaver

### **View Deactivated User:**

Run this SQL query:
```sql
SELECT 
    id,
    name,
    email,
    role_id,
    is_active,
    created_at
FROM users
WHERE email = 'frank@company.com';
```

**Result:**
| id | name | email | role_id | is_active | created_at |
|----|------|-------|---------|-----------|------------|
| uuid | Frank Miller | frank@company.com | uuid | **False** | timestamp |

---

### **View Deactivated Asset:**

Run this SQL query:
```sql
SELECT 
    id,
    asset_tag,
    name,
    status,
    is_active,
    created_at
FROM assets
WHERE asset_tag = 'IPHONE-13-001';
```

**Result:**
| id | asset_tag | name | status | is_active | created_at |
|----|-----------|------|--------|-----------|------------|
| uuid | IPHONE-13-001 | iPhone 13 Pro 256GB | Available | **False** | timestamp |

---

### **Compare Active vs Inactive Users:**

```sql
-- See all users with their active status
SELECT 
    name,
    email,
    is_active,
    CASE 
        WHEN is_active = TRUE THEN '✅ Active'
        ELSE '❌ Inactive'
    END as status_label
FROM users
ORDER BY is_active DESC, name;
```

**Result:**
| name | email | is_active | status_label |
|------|-------|-----------|--------------|
| Alice Johnson | alice@company.com | true | ✅ Active |
| Bob Smith | bob@company.com | true | ✅ Active |
| ... | ... | ... | ... |
| Frank Miller | frank@company.com | false | ❌ Inactive |

---

### **Compare Active vs Inactive Assets:**

```sql
-- See all assets with their active status
SELECT 
    asset_tag,
    name,
    status,
    is_active,
    CASE 
        WHEN is_active = TRUE THEN '✅ Active'
        ELSE '❌ Inactive'
    END as status_label
FROM assets
ORDER BY is_active DESC, asset_tag;
```

**Result:**
| asset_tag | name | status | is_active | status_label |
|-----------|------|--------|-----------|--------------|
| CHAIR-HERMAN-001 | Herman Miller Aeron Chair | Available | true | ✅ Active |
| DESK-STAND-001 | Standing Desk Electric 48" | Available | true | ✅ Active |
| ... | ... | ... | ... | ... |
| IPHONE-13-001 | iPhone 13 Pro 256GB | Available | false | ❌ Inactive |

---

## 💡 Why Use Soft Delete?

### **Advantages:**

1. **Data Integrity**
   - Foreign key relationships remain intact
   - No broken references in assignments table
   - Historical audit trails preserved

2. **Audit Trail**
   - Track when items were deactivated
   - Know who deactivated them (if you add tracking fields)
   - Maintain compliance with record-keeping requirements

3. **Reversibility**
   - Easy to reactivate by setting `is_active = TRUE`
   - No data loss from accidental deletions
   - Business continuity

4. **Reporting**
   - Show "inactive" items in reports
   - Analyze deactivation patterns
   - Track lifecycle of assets/users

---

## 🚀 API Behavior

### **Default Behavior: Filter Out Inactive**

When you call the API endpoints, they automatically filter out inactive records:

```http
GET /api/users/
# Returns only active users (is_active = true)
# Frank Miller NOT included

GET /api/assets/
# Returns only active assets (is_active = true)
# iPhone 13 Pro NOT included
```

### **Include Inactive (if needed)**

Some endpoints support including inactive records:

```http
GET /api/users/?include_inactive=true
# Returns ALL users (active + inactive)

GET /api/assets/?include_inactive=true
# Returns ALL assets (active + inactive)
```

---

## 🧪 Reactivation Example

### **Reactivate User:**

```python
from app.database import SessionLocal
from app.models import User

db = SessionLocal()

frank = db.query(User).filter(User.email == "frank@company.com").first()
frank.is_active = True
db.commit()

print(f"✅ {frank.name} reactivated!")
```

### **Reactivate Asset:**

```python
iphone = db.query(Asset).filter(Asset.asset_tag == "IPHONE-13-001").first()
iphone.is_active = True
db.commit()

print(f"✅ {iphone.name} reactivated!")
```

---

## 📊 Visual Comparison

### **Before Deactivation:**
```
┌──────────────────────────────────────┐
│ USERS TABLE                          │
├──────────────────────────────────────┤
│ Alice Johnson       ✅ Active        │
│ Bob Smith          ✅ Active         │
│ Carol Williams     ✅ Active         │
│ David Brown        ✅ Active         │
│ Eve Davis          ✅ Active         │
│ Frank Miller       ✅ Active         │
└──────────────────────────────────────┘
Total: 6 Active Users
```

### **After Deactivation:**
```
┌──────────────────────────────────────┐
│ USERS TABLE                          │
├──────────────────────────────────────┤
│ Alice Johnson       ✅ Active        │
│ Bob Smith          ✅ Active         │
│ Carol Williams     ✅ Active         │
│ David Brown        ✅ Active         │
│ Eve Davis          ✅ Active         │
├──────────────────────────────────────┤
│ Frank Miller       ❌ Inactive       │ ← Hidden by default
└──────────────────────────────────────┘
Total: 5 Active + 1 Inactive User
```

---

## 🎯 Key Takeaways

1. **Soft delete preserves data** instead of permanently removing it
2. **`is_active` flag** controls visibility in queries
3. **API filters automatically** exclude inactive records by default
4. **Historical integrity** maintained for auditing
5. **Easy reactivation** by flipping the flag back to TRUE

---

## 📝 Related Files

| File | Purpose |
|------|---------|
| `demonstrate_deactivation.py` | Script that performed this demo |
| `app/models.py` | Defines `is_active` field on models |
| `app/routers/users.py` | API endpoint with soft delete logic |
| `app/routers/assets.py` | API endpoint with soft delete logic |

---

## 🧪 Try It Yourself

### **Via API (Swagger UI):**

1. Go to http://localhost:8000/docs
2. Find `PATCH /api/users/{user_id}/deactivate`
3. Get user ID: `GET /api/users/` → copy Frank's UUID
4. Execute deactivate endpoint
5. Verify: `GET /api/users/` → Frank no longer appears!

### **Via DBeaver:**

1. Query users table
2. Find Frank Miller
3. Edit `is_active` cell → change to `false`
4. Save changes (Ctrl+S)
5. Refresh to see the change!

---

*Last Updated: March 7, 2026*  
*Demonstration completed successfully!*
