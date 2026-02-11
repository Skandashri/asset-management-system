-- ============================================================
-- DATABASE: AssetTrack Pro
-- INDUSTRIAL GRADE POSTGRESQL DUMP
-- Designed for 1000+ Employees & Dedicated HR Department
-- ============================================================

-- Drop Tables Safely
DROP TABLE IF EXISTS asset_status_logs;
DROP TABLE IF EXISTS asset_assignments;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS hr_staff;
DROP TABLE IF EXISTS departments;

-- ============================================================
-- 1. Departments Table
-- ============================================================

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_location VARCHAR(150),
    department_status VARCHAR(50) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_departments_name ON departments(department_name);

-- ============================================================
-- 2. Employees Table (Designed for 1000+ Employees)
-- ============================================================

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    employee_first_name VARCHAR(100) NOT NULL,
    employee_last_name VARCHAR(100),
    employee_email VARCHAR(150) UNIQUE NOT NULL,
    employee_phone VARCHAR(20),
    employee_address TEXT,
    employee_role VARCHAR(100),
    manager_employee_id INTEGER,
    department_id INTEGER,  -- Referencing departments.department_id
    employee_status VARCHAR(50) DEFAULT 'Active',
    date_of_joining DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employees_department_id ON employees(department_id);
CREATE INDEX idx_employees_status ON employees(employee_status);
CREATE INDEX idx_employees_code ON employees(employee_code);

-- ============================================================
-- 3. HR Staff Table (Dedicated HR Department)
-- ============================================================

CREATE TABLE hr_staff (
    hr_staff_id SERIAL PRIMARY KEY,
    hr_employee_code VARCHAR(50) UNIQUE NOT NULL,
    hr_name VARCHAR(150) NOT NULL,
    hr_email VARCHAR(150) UNIQUE NOT NULL,
    hr_phone VARCHAR(20),
    hr_designation VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hr_staff_code ON hr_staff(hr_employee_code);

-- ============================================================
-- 4. Assets Table
-- ============================================================

CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    asset_code VARCHAR(100) UNIQUE NOT NULL,
    asset_name VARCHAR(150) NOT NULL,
    asset_category VARCHAR(100),
    asset_serial_number VARCHAR(150),
    asset_purchase_date DATE,
    asset_warranty_expiry_date DATE,
    asset_vendor_name VARCHAR(150),
    asset_value NUMERIC(12,2),
    asset_condition VARCHAR(50),
    asset_status VARCHAR(50) DEFAULT 'Available',
    asset_location VARCHAR(150),
    created_by_hr_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assets_status ON assets(asset_status);
CREATE INDEX idx_assets_code ON assets(asset_code);

-- ============================================================
-- 5. Asset Assignments Table
-- ============================================================

CREATE TABLE asset_assignments (
    assignment_id SERIAL PRIMARY KEY,
    asset_id INTEGER,
    employee_id INTEGER,
    assigned_by_hr_id INTEGER,
    return_approved_by_hr_id INTEGER,
    assignment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_return_date DATE,
    actual_return_date DATE,
    assignment_status VARCHAR(50) DEFAULT 'Assigned',
    remarks TEXT,
    assignment_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_assignments_asset_id ON asset_assignments(asset_id);
CREATE INDEX idx_asset_assignments_employee_id ON asset_assignments(employee_id);

-- ============================================================
-- 6. Asset Status Logs (Full Audit Tracking)
-- ============================================================

CREATE TABLE asset_status_logs (
    log_id SERIAL PRIMARY KEY,
    asset_id INTEGER,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by_hr_id INTEGER,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE INDEX idx_asset_status_logs_asset_id ON asset_status_logs(asset_id);

-- ============================================================
-- Dummy Industrial Sample Data
-- ============================================================

INSERT INTO departments (department_name, department_location)
VALUES
('HR', 'Head Office'),
('IT', 'Bangalore'),
('Finance', 'Mumbai'),
('Operations', 'Chennai');

INSERT INTO hr_staff (hr_employee_code, hr_name, hr_email, hr_designation)
VALUES
('HR001', 'Anita Sharma', 'anita.hr@company.com', 'Senior HR Manager'),
('HR002', 'Rahul Verma', 'rahul.hr@company.com', 'HR Executive');

INSERT INTO employees (employee_code, employee_first_name, employee_last_name, employee_email, department_id, employee_role, date_of_joining)
VALUES
('EMP001', 'Rohit', 'Kumar', 'rohit.kumar@company.com', 2, 'Software Engineer', '2022-05-10'),
('EMP002', 'Sneha', 'Reddy', 'sneha.reddy@company.com', 3, 'Financial Analyst', '2021-03-15');

INSERT INTO assets (asset_code, asset_name, asset_category, asset_serial_number, asset_purchase_date, asset_value, asset_condition, asset_location, created_by_hr_id)
VALUES
('AST001', 'Dell Laptop', 'Electronics', 'DL123456', '2023-01-10', 75000.00, 'New', 'Bangalore Office', 1),
('AST002', 'Office Chair', 'Furniture', 'CH789456', '2022-07-20', 8000.00, 'Good', 'Mumbai Office', 2);

-- ============================================================
-- END OF INDUSTRIAL DATABASE DUMP
-- ============================================================