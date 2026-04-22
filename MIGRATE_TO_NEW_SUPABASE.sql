-- ==========================================
-- COMPLETE DATABASE SETUP WITH REAL DATA
-- Run this in Supabase SQL Editor
-- ==========================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (in correct order)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS asset_reports CASCADE;
DROP TABLE IF EXISTS asset_status_logs CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS assets CASCADE;
DROP TABLE IF EXISTS asset_categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- ==========================================
-- CREATE TABLES
-- ==========================================

-- Roles table
CREATE TABLE roles (
    id VARCHAR PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    permissions TEXT NOT NULL
);

-- Asset categories table
CREATE TABLE asset_categories (
    id VARCHAR PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    total_quantity INTEGER DEFAULT 0 NOT NULL,
    available_quantity INTEGER DEFAULT 0 NOT NULL
);

-- Users table
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    role_id VARCHAR NOT NULL REFERENCES roles(id),
    secondary_role_id VARCHAR REFERENCES roles(id),
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    department VARCHAR,
    contact VARCHAR,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Assets table
CREATE TABLE assets (
    id VARCHAR PRIMARY KEY,
    asset_tag VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    category_id VARCHAR REFERENCES asset_categories(id),
    purchase_date DATE,
    cost DOUBLE PRECISION,
    image_url VARCHAR,
    document_url VARCHAR,
    vendor VARCHAR,
    location VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'Available',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Assignments table
CREATE TABLE assignments (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    asset_id VARCHAR NOT NULL REFERENCES assets(id),
    assigned_date TIMESTAMP NOT NULL DEFAULT NOW(),
    return_date TIMESTAMP
);

-- Asset status logs table
CREATE TABLE asset_status_logs (
    id VARCHAR PRIMARY KEY,
    asset_id VARCHAR NOT NULL REFERENCES assets(id),
    old_status VARCHAR,
    new_status VARCHAR NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Asset reports table
CREATE TABLE asset_reports (
    id VARCHAR PRIMARY KEY,
    asset_id VARCHAR NOT NULL REFERENCES assets(id),
    reported_by_id VARCHAR NOT NULL REFERENCES users(id),
    report_type VARCHAR NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR DEFAULT 'Medium',
    status VARCHAR DEFAULT 'Pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMP,
    admin_notes TEXT
);

-- Requests table
CREATE TABLE requests (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    asset_id VARCHAR REFERENCES assets(id),
    item_name VARCHAR NOT NULL,
    item_type VARCHAR NOT NULL,
    notes TEXT,
    status VARCHAR NOT NULL DEFAULT 'Pending',
    admin_notes TEXT,
    requested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT request_status_check CHECK (status IN ('Pending', 'Approved', 'Rejected'))
);

-- Audit logs table
CREATE TABLE audit_logs (
    id VARCHAR PRIMARY KEY,
    action VARCHAR NOT NULL,
    performed_by_id VARCHAR REFERENCES users(id),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ==========================================
-- CREATE INDEXES
-- ==========================================

CREATE INDEX ix_roles_id ON roles(id);
CREATE UNIQUE INDEX ix_roles_name ON roles(name);

CREATE INDEX ix_asset_categories_id ON asset_categories(id);
CREATE UNIQUE INDEX ix_asset_categories_name ON asset_categories(name);

CREATE INDEX ix_users_id ON users(id);
CREATE UNIQUE INDEX ix_users_email ON users(email);

CREATE INDEX ix_assets_id ON assets(id);
CREATE UNIQUE INDEX ix_assets_asset_tag ON assets(asset_tag);

CREATE INDEX ix_assignments_id ON assignments(id);
CREATE INDEX ix_assignments_user_id ON assignments(user_id);
CREATE INDEX ix_assignments_asset_id ON assignments(asset_id);

CREATE INDEX ix_asset_status_logs_id ON asset_status_logs(id);
CREATE INDEX ix_asset_status_logs_asset_id ON asset_status_logs(asset_id);

CREATE INDEX ix_asset_reports_id ON asset_reports(id);
CREATE INDEX ix_asset_reports_asset_id ON asset_reports(asset_id);
CREATE INDEX ix_asset_reports_reported_by_id ON asset_reports(reported_by_id);

CREATE INDEX ix_requests_id ON requests(id);
CREATE INDEX ix_requests_user_id ON requests(user_id);
CREATE INDEX ix_requests_asset_id ON requests(asset_id);

CREATE INDEX ix_audit_logs_id ON audit_logs(id);
CREATE INDEX ix_audit_logs_performed_by_id ON audit_logs(performed_by_id);

-- ==========================================
-- INSERT REAL DATA
-- ==========================================

-- Insert Roles
INSERT INTO roles (id, name, permissions) VALUES
('bea322a4-011e-4e06-95bb-d6534250e8b8', 'Super Admin', '["all"]'),
('3282c72b-c4f0-40d5-86b6-1fa5d86ed5ed', 'Admin', '["view:roles", "manage:assignments", "view:users", "manage:users", "view:assignments", "view:assets", "view:reports", "view:dashboard", "manage:roles", "manage:reports", "manage:assets"]'),
('31ce2068-6d35-4d92-b0c3-764f032f3f9e', 'Employee', '["view:assets", "view:assignments", "view:dashboard", "create:reports", "view:my_reports"]');

-- Insert Users (with real passwords from your production DB)
INSERT INTO users (id, role_id, secondary_role_id, name, email, hashed_password, department, contact, is_active, created_at) VALUES
('2ee122ba-0acb-4ed8-9338-fa87c1cabef8', 'bea322a4-011e-4e06-95bb-d6534250e8b8', NULL, 'Super Administrator', 'superadmin@optiasset.com', '$2b$12$T86ya9ry.HeJTDGYBCkGGxu5PKhNZHVlF8zDIs3/b6Fc7aRtf9GQ.S', NULL, NULL, true, '2026-04-22 03:20:34.336031'),
('939c9bfc-ffb2-4d56-ae30-23ebbce4e2ca', '3282c72b-c4f0-40d5-86b6-1fa5d86ed5ed', NULL, 'Admin User', 'admin@optiasset.com', '$2b$12$2kG83OJ2UQjKzoIk8xbd7OJ2xcnK.Tj9K.rbWaNaCyABEKgc3bTRu', NULL, NULL, true, '2026-04-22 03:20:34.336038'),
('bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'Employee User', 'employee@optiasset.com', '$2b$12$VISlHoNLFye2RfkR76pNXOppZIQfs3zGoufymAaG/6.u8mQWHMtOG', NULL, NULL, true, '2026-04-22 07:06:58.600134'),
('aba3617f-4314-4140-874f-12f85cc09557', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'skanda', 'skandashri@optiasset.com', '$2b$12$A8M3e65aZ8JbTmEmMTzQyOwe1T.Mxmww3U0JpSZ0p7EFezOzJWgl6', NULL, NULL, true, '2026-04-22 12:35:10.034542'),
('a8bb319d-ee45-4ad3-944a-1c29dfe3b961', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'john', 'john@optiasset.com', '$2b$12$NHO99TlxLnn2TwbMIcybau8jcsHDw0JgOwAv0OXQfjRVZ5rjLkJm6', 'tech', '55666', true, '2026-04-22 13:29:57.924155'),
('01c685bf-1fa6-4659-96e4-d262f91fa560', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'Alice Johnson', 'alice@company.com', '$2b$12$8wU3YJyYQbnqrP3n8zHDj.1MW6cmq1cxPW/5/eRxlOHvA9AQUoSm.', NULL, NULL, true, '2026-04-22 03:20:34.336042'),
('207ec37f-40ea-4caf-8c6f-3277acaaaf18', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'Bob Smith', 'bob@company.com', '$2b$12$u0gNRtXTR4WuMKclG8p56OFx7XwrFVT6Z4s17w7SH4BtrY386/dfe', NULL, NULL, true, '2026-04-22 03:20:34.336045'),
('ba57235f-eed2-4ebe-870b-3280ad499be4', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'Carol Williams', 'carol@company.com', '$2b$12$7qVkFS2m8fB3OV3pEG7gxO9tJtXzlGmgONRs.KYlexDlWUBQJyyye', NULL, NULL, true, '2026-04-22 03:20:34.336048'),
('a184f757-e245-4fff-a7f4-a695b15a2448', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'David Brown', 'david@company.com', '$2b$12$8J2EnKf31.u6N2qpv4f1qOutg3ZxNVuwxJbrrf4rmp4e2l9bbxiWy', NULL, NULL, true, '2026-04-22 03:20:34.336051'),
('d0327810-3f89-47d8-ae08-6d80ddf339bb', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'Eve Davis', 'eve@company.com', '$2b$12$DsFeyoQ1Uz39JWxE3x8XOOBdbbfPWLFdPvXpcCWdw147Bulzvo2m', NULL, NULL, false, '2026-04-22 03:20:34.336053'),
('2582acb7-66fa-4f02-99b8-97e3c8b0179e', '31ce2068-6d35-4d92-b0c3-764f032f3f9e', NULL, 'Frank Miller', 'frank@company.com', '$2b$12$f8AV0E5N7XpSE3qgoKVhhe2jOEX3za0rvtyyQ3qF/IxEQOYY.vrpm', NULL, NULL, true, '2026-04-22 03:20:34.336055');

-- Insert Assets
INSERT INTO assets (id, asset_tag, name, category_id, purchase_date, cost, image_url, document_url, vendor, location, status, is_active, created_at) VALUES
('42495a36-dc40-4109-8250-4eb69aaea287', 'IPHONE-13-001', 'iPhone 13 Pro 256GB', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Available', true, '2026-04-22 03:20:34.361342'),
('146ddfef-c187-4d33-9aa6-0e5db01e698f', 'MONITOR-DELL-001', 'Dell UltraSharp 27" U2720Q', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361322'),
('46a0f4bd-2ba3-43fa-bf09-d0f136338f69', 'LAPTOP-HP-001', 'HP EliteBook 840 G8', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361312'),
('7de319e5-bdd7-480c-8c2f-371b39c64405', 'KEYBOARD-LOGI-001', 'Logitech MX Keys Keyboard', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361329'),
('86464c0a-d9c3-4653-b490-8174276b3d27', 'LAPTOP-LEN-002', 'Lenovo ThinkPad X1 Carbon', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361319'),
('f639fe37-fa1a-4614-a382-7b736cead51f', 'MONITOR-LG-002', 'LG 27" 4K UHD Monitor', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361325'),
('dd2597d8-4986-4950-a916-7c5019547c76', 'DESK-STAND-001', 'Standing Desk Electric 48"', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361337'),
('a8aeb81b-0b2b-47e8-984c-6b92933ec0aa', 'IPAD-PRO-001', 'iPad Pro 12.9" M1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361339'),
('a3c45364-c2a0-416f-9310-f84d7b68e265', 'A101', 'macbook', NULL, NULL, 122, NULL, NULL, 'me', 'hassan', 'Assigned', true, '2026-04-22 12:36:29.56295'),
('d4dd71d2-c389-492f-af20-80e0febc4b42', 'HEADSET-SONY-001', 'Sony WH-1000XM4 Headphones', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361347'),
('ceba4785-26e2-411b-89a5-cdc4d6e38688', 'WEBCAM-LOGI-001', 'Logitech Brio 4K Webcam', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 03:20:34.361344'),
('a1baadd0-7c1b-4066-aa67-7e407c754e8b', 'A0011', 'macbook pro max', NULL, NULL, 450, NULL, NULL, 'sam', 'hassan', 'Available', true, '2026-04-22 16:20:45.760915'),
('310d07e9-93a0-4d05-836a-9a0b41f1ed37', 'TAG-e1a540', 'Test Asset', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Assigned', true, '2026-04-22 05:30:53.294129'),
('bed45e21-e0bc-48a1-b04f-33582db863e9', 'CHAIR-HERMAN-001', 'Herman Miller Aeron Chair', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Available', false, '2026-04-22 03:20:34.361334'),
('1fa5c546-a6a4-4568-abca-4ce6f317c15c', 'MOUSE-LOGI-001', 'Logitech MX Master 3 Mouse', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Available', false, '2026-04-22 03:20:34.361331');

-- Insert Assignments
INSERT INTO assignments (id, user_id, asset_id, assigned_date, return_date) VALUES
('34380a98-8a7a-414d-875b-98a3d913eadf', '01c685bf-1fa6-4659-96e4-d262f91fa560', '46a0f4bd-2ba3-43fa-bf09-d0f136338f69', '2026-03-23 03:20:34.375327', NULL),
('9851cd7a-9c49-46c4-a2fc-a98d3ae677e9', '207ec37f-40ea-4caf-8c6f-3277acaaaf18', '86464c0a-d9c3-4653-b490-8174276b3d27', '2026-03-28 03:20:34.376486', NULL),
('27d9e74e-359c-4104-ac00-4dc9c8426a4d', 'ba57235f-eed2-4ebe-870b-3280ad499be4', '146ddfef-c187-4d33-9aa6-0e5db01e698f', '2026-04-02 03:20:34.377482', NULL),
('df12bc35-c761-4abf-afc5-d06f3a9e56a0', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'dd2597d8-4986-4950-a916-7c5019547c76', '2026-04-22 13:03:27.164011', NULL),
('5cb09859-f4fd-4edb-8dab-4cc3df39b476', '207ec37f-40ea-4caf-8c6f-3277acaaaf18', 'a8aeb81b-0b2b-47e8-984c-6b92933ec0aa', '2026-04-22 14:47:12.731272', NULL),
('7ca305ad-49a0-4d0a-80d0-d8825595908a', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'a3c45364-c2a0-416f-9310-f84d7b68e265', '2026-04-22 14:47:47.363619', NULL),
('8b3cebf4-93f4-4323-8c14-2b65f46185bf', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'd4dd71d2-c389-492f-af20-80e0febc4b42', '2026-04-22 14:50:43.731268', NULL),
('382d5dc1-e3ff-44b3-bc67-abeec8908059', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'ceba4785-26e2-411b-89a5-cdc4d6e38688', '2026-04-22 15:06:39.056172', NULL);

-- Insert Asset Status Logs
INSERT INTO asset_status_logs (id, asset_id, old_status, new_status, changed_at) VALUES
('f7cdea86-fd6f-4806-8370-45116fa79f97', '46a0f4bd-2ba3-43fa-bf09-d0f136338f69', 'Available', 'Assigned', '2026-03-23 03:20:34.375327'),
('aeb13b7c-505b-4b72-b8fc-e6bc88116172', '86464c0a-d9c3-4653-b490-8174276b3d27', 'Available', 'Assigned', '2026-03-28 03:20:34.376486'),
('fef1e0a9-27a6-409e-b805-3da2f141a484', '146ddfef-c187-4d33-9aa6-0e5db01e698f', 'Available', 'Assigned', '2026-04-02 03:20:34.377482'),
('4bccc6e8-dbf4-41f4-b364-3e258b0b0a8c', 'dd2597d8-4986-4950-a916-7c5019547c76', 'Available', 'Assigned', '2026-04-22 13:03:27.158356'),
('9e0e93db-b73a-4cf8-8698-d6c9e86c294e', 'a8aeb81b-0b2b-47e8-984c-6b92933ec0aa', 'Available', 'Assigned', '2026-04-22 14:47:12.727533'),
('09a80ed8-6a4e-4e8a-8a00-7c9bc73e4575', 'a3c45364-c2a0-416f-9310-f84d7b68e265', 'Available', 'Assigned', '2026-04-22 14:47:47.362248'),
('2df3b3b6-6366-4cea-be16-1d133a6f9067', 'd4dd71d2-c389-492f-af20-80e0febc4b42', 'Available', 'Assigned', '2026-04-22 14:50:43.730277'),
('4379a155-1545-4685-a38d-5c0560cea42c', 'ceba4785-26e2-411b-89a5-cdc4d6e38688', 'Available', 'Assigned', '2026-04-22 15:06:39.05488');

-- Insert Asset Reports
INSERT INTO asset_reports (id, asset_id, reported_by_id, report_type, description, severity, status, created_at, resolved_at, admin_notes) VALUES
('b372ece7-5d83-4c49-a16e-1a03d41d848a', 'dd2597d8-4986-4950-a916-7c5019547c76', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'Not working', 'bad', 'Medium', 'Under Review', '2026-04-22 13:26:55.337422', NULL, 'it is looking'),
('dc9f8c5b-335d-42df-9dd7-35b006305976', 'ceba4785-26e2-411b-89a5-cdc4d6e38688', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'Not working', 'bad', 'Medium', 'Under Review', '2026-04-22 15:48:43.818501', NULL, 'kklp;m;m;mmnnkm');

-- Insert Requests
INSERT INTO requests (id, user_id, asset_id, item_name, item_type, notes, status, admin_notes, requested_at) VALUES
('5353a916-a3ec-4bd6-9059-f1a086cc3e94', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', NULL, 'Test Laptop M3', 'Laptop', 'Needed for development', 'Approved', 'Approved for new project - Q2 2024', '2026-04-22 13:22:20.5166'),
('986512ae-a217-4755-a0b7-13775b513da5', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', 'a8aeb81b-0b2b-47e8-984c-6b92933ec0aa', 'mouse', 'Equipment', 'my old mouse is not woking good', 'Approved', NULL, '2026-04-22 12:59:09.782708'),
('a731e304-e8ed-471a-9ba6-aee8dc7c6ba2', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', NULL, 'skanda', 'Laptop', NULL, 'Rejected', 'it is costly', '2026-04-22 12:57:45.684546'),
('dc197443-2b89-4e17-aaa9-2c60d067e5ef', 'bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7', '310d07e9-93a0-4d05-836a-9a0b41f1ed37', 'usb cable', 'Accessory', '', 'Approved', NULL, '2026-04-22 16:48:19.403947');
