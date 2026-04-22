-- Complete Supabase Database Setup
-- Run this ENTIRE script in one go

-- Step 1: Drop all existing tables
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS asset_status_logs CASCADE;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS asset_reports CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS assets CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS asset_categories CASCADE;
DROP TABLE IF EXISTS alembic_version CASCADE;

-- Step 2: Create all tables

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);

CREATE TABLE public.asset_categories (
    id character varying NOT NULL,
    name character varying NOT NULL,
    total_quantity integer NOT NULL,
    available_quantity integer NOT NULL
);

CREATE TABLE public.roles (
    id character varying NOT NULL,
    name character varying NOT NULL,
    permissions text NOT NULL
);

CREATE TABLE public.users (
    id character varying NOT NULL,
    role_id character varying NOT NULL,
    secondary_role_id character varying,
    name character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    department character varying,
    contact character varying,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);

CREATE TABLE public.assets (
    id character varying NOT NULL,
    asset_tag character varying NOT NULL,
    name character varying NOT NULL,
    category_id character varying,
    purchase_date date,
    cost double precision,
    image_url character varying,
    document_url character varying,
    vendor character varying,
    location character varying,
    status character varying NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);

CREATE TABLE public.assignments (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    asset_id character varying NOT NULL,
    assigned_date timestamp without time zone NOT NULL,
    return_date timestamp without time zone
);

CREATE TABLE public.asset_reports (
    id character varying NOT NULL,
    asset_id character varying NOT NULL,
    reported_by_id character varying NOT NULL,
    report_type character varying NOT NULL,
    description text NOT NULL,
    severity character varying,
    status character varying,
    created_at timestamp without time zone NOT NULL,
    resolved_at timestamp without time zone,
    admin_notes text
);

CREATE TABLE public.asset_status_logs (
    id character varying NOT NULL,
    asset_id character varying NOT NULL,
    old_status character varying,
    new_status character varying NOT NULL,
    changed_at timestamp without time zone NOT NULL
);

CREATE TABLE public.requests (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    asset_id character varying,
    item_name character varying NOT NULL,
    item_type character varying NOT NULL,
    notes text,
    status character varying NOT NULL,
    admin_notes text,
    requested_at timestamp without time zone NOT NULL,
    CONSTRAINT request_status_check CHECK (((status)::text = ANY ((ARRAY['Pending'::character varying, 'Approved'::character varying, 'Rejected'::character varying])::text[])))
);

CREATE TABLE public.audit_logs (
    id character varying NOT NULL,
    action character varying NOT NULL,
    performed_by_id character varying,
    "timestamp" timestamp without time zone NOT NULL
);

CREATE TABLE public.notifications (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    title character varying NOT NULL,
    message text NOT NULL,
    notification_type character varying NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    read_at timestamp without time zone,
    action_url character varying,
    notification_data text
);

-- Step 3: Add Primary Keys

ALTER TABLE ONLY public.alembic_version ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
ALTER TABLE ONLY public.asset_categories ADD CONSTRAINT asset_categories_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.roles ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.assets ADD CONSTRAINT assets_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.assignments ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.asset_reports ADD CONSTRAINT asset_reports_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.asset_status_logs ADD CONSTRAINT asset_status_logs_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.requests ADD CONSTRAINT requests_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.audit_logs ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.notifications ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);

-- Step 4: Add Indexes

CREATE INDEX ix_asset_categories_id ON public.asset_categories USING btree (id);
CREATE UNIQUE INDEX ix_asset_categories_name ON public.asset_categories USING btree (name);
CREATE INDEX ix_roles_id ON public.roles USING btree (id);
CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);
CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);
CREATE INDEX ix_users_id ON public.users USING btree (id);
CREATE UNIQUE INDEX ix_assets_asset_tag ON public.assets USING btree (asset_tag);
CREATE INDEX ix_assets_id ON public.assets USING btree (id);
CREATE INDEX ix_assignments_asset_id ON public.assignments USING btree (asset_id);
CREATE INDEX ix_assignments_id ON public.assignments USING btree (id);
CREATE INDEX ix_assignments_user_id ON public.assignments USING btree (user_id);
CREATE INDEX ix_asset_reports_asset_id ON public.asset_reports USING btree (asset_id);
CREATE INDEX ix_asset_reports_id ON public.asset_reports USING btree (id);
CREATE INDEX ix_asset_reports_reported_by_id ON public.asset_reports USING btree (reported_by_id);
CREATE INDEX ix_asset_status_logs_asset_id ON public.asset_status_logs USING btree (asset_id);
CREATE INDEX ix_asset_status_logs_id ON public.asset_status_logs USING btree (id);
CREATE INDEX ix_requests_asset_id ON public.requests USING btree (asset_id);
CREATE INDEX ix_requests_id ON public.requests USING btree (id);
CREATE INDEX ix_requests_user_id ON public.requests USING btree (user_id);
CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);
CREATE INDEX ix_audit_logs_performed_by_id ON public.audit_logs USING btree (performed_by_id);
CREATE INDEX ix_notifications_created_at ON public.notifications USING btree (created_at);
CREATE INDEX ix_notifications_is_read ON public.notifications USING btree (is_read);
CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);

-- Step 5: Add Foreign Keys

ALTER TABLE ONLY public.assets ADD CONSTRAINT assets_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.asset_categories(id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);
ALTER TABLE ONLY public.users ADD CONSTRAINT fk_user_secondary_role FOREIGN KEY (secondary_role_id) REFERENCES public.roles(id);
ALTER TABLE ONLY public.assignments ADD CONSTRAINT assignments_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);
ALTER TABLE ONLY public.assignments ADD CONSTRAINT assignments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.asset_reports ADD CONSTRAINT asset_reports_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);
ALTER TABLE ONLY public.asset_reports ADD CONSTRAINT asset_reports_reported_by_id_fkey FOREIGN KEY (reported_by_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.asset_status_logs ADD CONSTRAINT asset_status_logs_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);
ALTER TABLE ONLY public.requests ADD CONSTRAINT requests_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);
ALTER TABLE ONLY public.requests ADD CONSTRAINT requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.audit_logs ADD CONSTRAINT audit_logs_performed_by_id_fkey FOREIGN KEY (performed_by_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.notifications ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
