1. departments (department_id, department_name, department_location, department_status, created_at)

2. employees (employee_id, employee_code, employee_first_name, employee_last_name, employee_email, employee_phone, employee_address, employee_role, manager_employee_id, department_id, employee_status, date_of_joining, created_at, last_updated_at)

3. hr_staff (hr_staff_id, hr_employee_code, hr_name, hr_email, hr_phone, hr_designation, created_at)

4. assets (asset_id, asset_code, asset_name, asset_category, asset_serial_number, asset_purchase_date, asset_warranty_expiry_date, asset_vendor_name, asset_value, asset_condition, asset_status, asset_location, created_by_hr_id, created_at, last_updated_at)

5. asset_assignments (assignment_id, asset_id, employee_id, assigned_by_hr_id, return_approved_by_hr_id, assignment_date, expected_return_date, actual_return_date, assignment_status, remarks, assignment_updated_at)

6. asset_status_logs (log_id, asset_id, previous_status, new_status, changed_by_hr_id, change_timestamp, notes)