# Quick API Testing Cheat Sheet

## 🚀 Quick Start (5 Minutes)

### Step 1: Open Swagger UI
```
http://localhost:8000/docs
```

### Step 2: Authenticate as Admin
1. Click **[Authorize]** button (top right)
2. Enter:
   - **username:** `admin@optiasset.com`
   - **password:** `admin123`
3. Click **[Authorize]** → **[Close]**

### Step 3: Test These 5 Endpoints (Minimum Viable Demo)

#### 1️⃣ Create Asset
```
POST /api/assets/
Try it out → 
{
  "asset_tag": "TEST-001",
  "name": "Test Laptop"
}
→ Execute → 201 Created ✅
```

#### 2️⃣ Get All Assets
```
GET /api/assets/
Try it out → Execute → 200 OK ✅
```

#### 3️⃣ Create User
```
POST /api/users/
Try it out →
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "test123"
}
→ Execute → 201 Created ✅
```

#### 4️⃣ Assign Asset
```
POST /api/assignments/
Try it out →
{
  "user_id": "<paste-user-id-from-step-3>",
  "asset_id": "<paste-asset-id-from-step-1>"
}
→ Execute → 201 Created ✅
```

#### 5️⃣ Get Dashboard Stats
```
GET /api/dashboard/
Try it out → Execute → 200 OK ✅
```

---

## 🎯 Screenshot-Worthy Tests

For your submission screenshot, test these endpoints and capture the green **200 OK**:

### Recommended Sequence:

1. **Authentication** - Show you're logged in
   ```
   POST /api/auth/login
   Response shows: access_token, role: "Admin"
   ```

2. **Create Asset** - Show creation works
   ```
   POST /api/assets/
   Request: {"asset_tag": "DEMO-001", "name": "Demo Laptop"}
   Response: 201 Created with full asset object
   ```

3. **Get All Assets** - Show retrieval works
   ```
   GET /api/assets/
   Response: Array of assets [ {...}, {...} ]
   ```

4. **Dashboard** - Show analytics work
   ```
   GET /api/dashboard/
   Response: {"total_assets": X, "total_users": Y, ...}
   ```

---

## 🔐 Test Accounts Reference

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| **Admin** | admin@optiasset.com | admin123 | `["all"]` (Full Access) |
| **Employee** | employee@optiasset.com | employee123 | `["view:my_gear", "view:assets"]` (Limited) |

---

## ✅ Must-Pass Tests for Submission

### Authentication (Required)
- [x] Admin login → 200 OK
- [x] Employee login → 200 OK
- [x] Invalid credentials → 401 Unauthorized

### CRUD Operations (Pick 3-4)
- [x] Create asset → 201 Created
- [x] Get all assets → 200 OK
- [x] Update asset → 200 OK
- [x] Create user → 201 Created
- [x] Assign asset → 201 Created
- [x] Get dashboard → 200 OK

### RBAC (Required)
- [x] Employee tries to create asset → 403 Forbidden ❌
- [x] Employee views assets → 200 OK ✅

---

## 💡 Pro Tips

### For Impressive Screenshots:

1. **Expand the endpoint fully** to show documentation
2. **Show both request and response** bodies
3. **Highlight the green 200 OK** badge
4. **Show the lock icon** 🔒 (proves authentication)
5. **Include endpoint path** in screenshot (e.g., `GET /api/assets/`)

### Example Screenshot Composition:

```
┌─────────────────────────────────────────┐
│ Swagger UI                      [🔒]   │
│                                         │
│ ▼ Assets                                │
│   POST /api/assets/                     │
│   ┌─────────────────────────────────┐  │
│   │ Try it out                      │  │
│   │                                 │  │
│   │ Request body:                   │  │
│   │ {                               │  │
│   │   "asset_tag": "TEST-001",     │  │
│   │   "name": "Test Laptop"        │  │
│   │ }                               │  │
│   │                                 │  │
│   │ Response: 201 Created ✅        │  │
│   │ {                               │  │
│   │   "id": "...",                 │  │
│   │   "asset_tag": "TEST-001",     │  │
│   │   "status": "Available"        │  │
│   │ }                               │  │
│   └─────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🚨 Common Mistakes to Avoid

❌ **Don't** test without authenticating first  
✅ **Do** click [Authorize] and get token

❌ **Don't** use invalid UUIDs  
✅ **Do** copy-paste IDs from previous responses

❌ **Don't** test on inactive resources  
✅ **Do** check `is_active: true`

❌ **Don't** forget to click [Try it out]  
✅ **Do** enable edit mode before executing

❌ **Don't** test duplicate creation  
✅ **Do** use unique asset_tag values

---

## 📊 Full Test Coverage Map

| Category | Endpoints | Min Tests | Priority |
|----------|-----------|-----------|----------|
| Auth | 1 | 2 | 🔴 High |
| Assets | 7 | 4 | 🔴 High |
| Users | 6 | 3 | 🟡 Medium |
| Assignments | 4 | 2 | 🟡 Medium |
| Dashboard | 1 | 1 | 🟢 Low |
| Roles | 2 | 1 | 🟢 Low |
| RBAC | N/A | 2 | 🔴 High |

**Minimum Total:** 15 tests for full coverage  
**Quick Demo:** 5 tests (Auth + 3 CRUD + Dashboard)

---

## 🎬 Script for Recording/Demo

If you want to record a quick demo video:

```
1. Open Swagger UI (http://localhost:8000/docs)
2. Click Authorize → Login as admin → Show token received
3. Create an asset → Show 201 Created
4. Get all assets → Show array response
5. Create a user → Show 201 Created
6. Assign asset to user → Show 201 Created
7. Get dashboard stats → Show metrics
8. Logout, login as employee
9. Try to create asset → Show 403 Forbidden (RBAC works!)
10. View assets as employee → Show 200 OK
```

Total time: ~3-5 minutes

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| 401 on all requests | Click [Authorize], login, get token |
| Token expired | Re-login (lasts 30 min) |
| 404 Not Found | Resource doesn't exist, create it first |
| 400 Bad Request | Check for duplicates, validate JSON |
| Can't execute | Click [Try it out] button first |
| No green button | Check authorization, verify request format |

---

## 📱 Mobile-Friendly Quick Reference

Save this to your phone:

```
AUTH:
Admin: admin@optiasset.com / admin123
Employee: employee@optiasset.com / employee123

QUICK TESTS:
1. POST /assets/ → Create
2. GET /assets/ → List
3. POST /users/ → Create User
4. POST /assignments/ → Assign
5. GET /dashboard/ → Stats

RBAC TEST:
Employee create asset → 403 Forbidden
```

---

**Good luck with your testing! 🚀**

All examples are ready to copy-paste into Swagger UI.
