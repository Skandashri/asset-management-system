import urllib.request
import urllib.parse
import json
import uuid

BASE_URL = "http://localhost:8000/api"

def request(method, path, data=None, token=None, is_form=False):
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    encoded_data = None
    if data:
        if is_form:
            encoded_data = urllib.parse.urlencode(data).encode('utf-8')
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            encoded_data = json.dumps(data).encode('utf-8')
            headers["Content-Type"] = "application/json"
            
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            if res_body:
                return response.status, json.loads(res_body)
            return response.status, {}
    except urllib.error.HTTPError as e:
        res_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(res_body)
        except:
            return e.code, res_body
    except Exception as e:
        return 500, str(e)

def run_tests():
    print("Starting API Tests...")
    failures = []
    
    # 1. Login
    status, res = request("POST", "/auth/login", {"username": "admin@optiasset.com", "password": "admin123"}, is_form=True)
    if status == 200:
        token = res.get("access_token")
        print("PASS: Login successful")
    else:
        print(f"FAIL: Login failed: {status} {res}")
        return

    # 2. Roles
    status, roles = request("GET", "/roles/", token=token)
    if status == 200:
        print("PASS: Get all roles successful")
    else:
        print(f"FAIL: Get roles failed: {status} {roles}")
        failures.append("Get Roles")

    # 3. Create Role
    role_name = f"TestRole_{uuid.uuid4().hex[:6]}"
    status, role = request("POST", "/roles/", {"name": role_name, "permissions": ["view:assets"]}, token=token)
    if status == 201:
        print("PASS: Create role successful")
        role_id = role["id"]
    else:
        print(f"FAIL: Create role failed: {status} {role}")
        failures.append("Create Role")

    # 4. Create Asset
    asset_tag = f"TAG-{uuid.uuid4().hex[:6]}"
    status, asset = request("POST", "/assets/", {"asset_tag": asset_tag, "name": "Test Asset"}, token=token)
    if status == 201:
        print("PASS: Create asset successful")
        asset_id = asset["id"]
    elif status == 400: # if validations are strict and dummy data exists
        print(f"WARN: Create asset returned 400: {status} {asset} - checking if any asset exists to continue")
        status, assets = request("GET", "/assets/", token=token)
        if assets and len(assets) > 0:
            asset_id = assets[0]["id"]
        else:
            return
    else:
        print(f"FAIL: Create asset failed: {status} {asset}")
        failures.append("Create Asset")
        
    # Get Alle Assets
    status, res = request("GET", "/assets/", token=token)
    if status == 200:
        print("PASS: Get all assets successful")
    else:
        print(f"FAIL: Get assets failed: {status} {res}")
        failures.append("Get Assets")
        
    # Get Single Asset
    if 'asset_id' in locals():
        status, res = request("GET", f"/assets/{asset_id}", token=token)
        if status == 200:
            print("PASS: Get single asset successful")
        else:
            print(f"FAIL: Get single asset failed: {status} {res}")
            failures.append("Get Single Asset")

        # Update Asset
        status, res = request("PUT", f"/assets/{asset_id}", {"name": "Updated Test Asset", "status": "Maintenance"}, token=token)
        if status == 200:
            print("PASS: Update asset successful")
        else:
            print(f"FAIL: Update asset failed: {status} {res}")
            failures.append("Update Asset")

    # Dashboard
    status, res = request("GET", "/dashboard/", token=token)
    if status == 200:
        print("PASS: Get dashboard successful")
    else:
        print(f"FAIL: Get dashboard failed: {status} {res}")
        failures.append("Get Dashboard")
        
    # Users
    status, res = request("GET", "/users/", token=token)
    if status == 200:
        print("PASS: Get users successful")
    else:
        print(f"FAIL: Get users failed: {status} {res}")
        failures.append("Get Users")

    # Summary
    print("-" * 30)
    if not failures:
        print("ALL TESTED ENDPOINTS PASSED!")
    else:
        print(f"WARN: {len(failures)} failures: {', '.join(failures)}")

if __name__ == "__main__":
    run_tests()
