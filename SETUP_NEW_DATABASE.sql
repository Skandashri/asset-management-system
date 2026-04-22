-- Complete Supabase Database Setup with Initial Data
-- Run this entire script in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (in correct order)
DROP TABLE IF EXISTS asset_status_logs CASCADE;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS asset_reports CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS assets CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS asset_categories CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- Create roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create asset_categories table
CREATE TABLE asset_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    secondary_role_id INTEGER REFERENCES roles(id),
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create assets table
CREATE TABLE assets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    asset_tag VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    category_id INTEGER REFERENCES asset_categories(id),
    status VARCHAR(50) DEFAULT 'Available',
    purchase_date DATE,
    purchase_cost DECIMAL(10,2),
    location VARCHAR(255),
    description TEXT,
    specifications JSONB,
    warranty_expiry DATE,
    assigned_to UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create assignments table
CREATE TABLE assignments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    user_id UUID REFERENCES users(id),
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_return_date DATE,
    actual_return_date DATE,
    condition_at_assignment TEXT,
    condition_at_return TEXT,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create asset_reports table
CREATE TABLE asset_reports (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    user_id UUID REFERENCES users(id),
    issue_type VARCHAR(100),
    description TEXT NOT NULL,
    priority VARCHAR(50) DEFAULT 'Medium',
    status VARCHAR(50) DEFAULT 'Open',
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create requests table
CREATE TABLE requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    asset_id UUID REFERENCES assets(id),
    request_type VARCHAR(50),
    description TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    approved_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create asset_status_logs table
CREATE TABLE asset_status_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_assigned_to ON assets(assigned_to);
CREATE INDEX idx_assignments_asset_id ON assignments(asset_id);
CREATE INDEX idx_assignments_user_id ON assignments(user_id);
CREATE INDEX idx_asset_reports_status ON asset_reports(status);
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_asset_status_logs_asset_id ON asset_status_logs(asset_id);

-- ============================================
-- INSERT INITIAL DATA
-- ============================================

-- Insert roles
INSERT INTO roles (name, description) VALUES
('Admin', 'Full system access'),
('Manager', 'Can approve requests and view reports'),
('Employee', 'Standard user - can request assets'),
('IT Staff', 'Technical staff managing assets');

-- Insert asset categories
INSERT INTO asset_categories (name, description) VALUES
('Laptops', 'Laptop computers and notebooks'),
('Monitors', 'Display monitors'),
('Phones', 'Mobile phones and tablets'),
('Accessories', 'Keyboards, mice, and other accessories'),
('Furniture', 'Desks, chairs, and office furniture'),
('Networking', 'Routers, switches, and network equipment');

-- Insert default admin user
-- Password: admin123 (hashed with bcrypt)
-- IMPORTANT: Change this password after first login!
INSERT INTO users (email, hashed_password, full_name, role_id, department, is_active) VALUES
('admin@company.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILp92S.0i', 'System Administrator', 1, 'IT', true),
('manager@company.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILp92S.0i', 'Department Manager', 2, 'Operations', true),
('employee@company.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILp92S.0i', 'John Employee', 3, 'Engineering', true);

-- Insert sample assets
INSERT INTO assets (id, name, asset_tag, category, category_id, status, location, description) VALUES
(uuid_generate_v4(), 'MacBook Pro 14"', 'LAPTOP-APPLE-001', 'Laptops', 1, 'Available', 'IT Storage', 'MacBook Pro 14-inch M2 Pro'),
(uuid_generate_v4(), 'Dell UltraSharp 27"', 'MONITOR-DELL-001', 'Monitors', 2, 'Available', 'IT Storage', 'Dell UltraSharp 27" 4K Monitor'),
(uuid_generate_v4(), 'iPhone 15 Pro', 'PHONE-APPLE-001', 'Phones', 3, 'Available', 'IT Storage', 'iPhone 15 Pro 256GB'),
(uuid_generate_v4(), 'HP EliteBook 840', 'LAPTOP-HP-001', 'Laptops', 1, 'Available', 'IT Storage', 'HP EliteBook 840 G9'),
(uuid_generate_v4(), 'Logitech MX Keys', 'KEYBOARD-LOGI-001', 'Accessories', 4, 'Available', 'IT Storage', 'Logitech MX Keys Wireless Keyboard'),
(uuid_generate_v4(), 'Standing Desk Electric', 'DESK-STAND-001', 'Furniture', 5, 'Available', 'IT Storage', 'Electric Standing Desk 48"');
