--
-- PostgreSQL database dump
--

DROP TABLE IF EXISTS public.asset_reports CASCADE;
DROP TABLE IF EXISTS public.asset_status_logs CASCADE;
DROP TABLE IF EXISTS public.assignments CASCADE;
DROP TABLE IF EXISTS public.assets CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.roles CASCADE;

-- Dumped from database version 15.16
-- Dumped by pg_dump version 15.16

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: asset_reports; Type: TABLE; Schema: public; Owner: -
--

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


--
-- Name: asset_status_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asset_status_logs (
    id character varying NOT NULL,
    asset_id character varying NOT NULL,
    old_status character varying,
    new_status character varying NOT NULL,
    changed_at timestamp without time zone NOT NULL
);


--
-- Name: assets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assets (
    id character varying NOT NULL,
    asset_tag character varying NOT NULL,
    name character varying NOT NULL,
    status character varying NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assignments (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    asset_id character varying NOT NULL,
    assigned_date timestamp without time zone NOT NULL,
    return_date timestamp without time zone
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id character varying NOT NULL,
    name character varying NOT NULL,
    permissions text NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id character varying NOT NULL,
    role_id character varying,
    name character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    secondary_role_id text
);


--
-- Data for Name: asset_reports; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: asset_status_logs; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.asset_status_logs VALUES ('075a3e86-7b65-4589-878d-5445ccfe6fc8', '162df5f9-94b7-46d6-80df-4636f3ed15cb', 'Available', 'Assigned', '2026-03-10 07:03:11.193647');
INSERT INTO public.asset_status_logs VALUES ('f85ff8e4-a154-4b0e-8979-2beb3022549c', 'a83529cd-14a4-4226-ba7d-f0764474d811', 'Available', 'Assigned', '2026-03-15 07:03:11.197567');
INSERT INTO public.asset_status_logs VALUES ('dd021119-e628-42f7-bbe1-62d0cde6a6bf', '364af830-06df-47b9-a47e-f031fe7f53b6', 'Available', 'Assigned', '2026-03-20 07:03:11.200651');
INSERT INTO public.asset_status_logs VALUES ('834ad737-70f3-4373-a98e-0501876b04ca', '863f6f2b-0bd1-4cec-9c83-afc6d4168341', 'Available', 'Assigned', '2026-03-25 07:03:11.202772');
INSERT INTO public.asset_status_logs VALUES ('2dcb7284-d893-4a6f-8fcc-89141e7e0e22', '736a8411-b740-412a-8bfd-371de8cf0809', 'Available', 'Assigned', '2026-03-30 07:03:11.206846');


--
-- Data for Name: assets; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.assets VALUES ('42b158f2-c557-486d-903a-98bfb968eaff', 'MONITOR-DELL-001', 'Dell UltraSharp 27" U2720Q', 'Available', true, '2026-04-09 07:03:11.16108');
INSERT INTO public.assets VALUES ('f5389ed8-523f-45af-8575-35504d7f4fc9', 'MONITOR-LG-002', 'LG 27" 4K UHD Monitor', 'Available', true, '2026-04-09 07:03:11.161086');
INSERT INTO public.assets VALUES ('8563e4a4-9b0c-4e13-b085-4ef779f9cba2', 'KEYBOARD-LOGI-001', 'Logitech MX Keys Keyboard', 'Available', true, '2026-04-09 07:03:11.161091');
INSERT INTO public.assets VALUES ('5ba6d325-721b-400a-9e2c-c2f44b9ead77', 'MOUSE-LOGI-001', 'Logitech MX Master 3 Mouse', 'Available', true, '2026-04-09 07:03:11.161097');
INSERT INTO public.assets VALUES ('5c8a3abf-2e4f-4dd8-acec-b61c38f2f3d6', 'CHAIR-HERMAN-001', 'Herman Miller Aeron Chair', 'Available', true, '2026-04-09 07:03:11.161102');
INSERT INTO public.assets VALUES ('84ffeb2a-d5cd-4c8d-a152-c5a18daafa5b', 'DESK-STAND-001', 'Standing Desk Electric 48"', 'Available', true, '2026-04-09 07:03:11.161107');
INSERT INTO public.assets VALUES ('32e0ed2c-f823-48c5-a91f-8f9822ecb771', 'IPAD-PRO-001', 'iPad Pro 12.9" M1', 'Available', true, '2026-04-09 07:03:11.161112');
INSERT INTO public.assets VALUES ('f98c3d41-e021-4757-ad02-6ca55aa5c792', 'IPHONE-13-001', 'iPhone 13 Pro 256GB', 'Available', true, '2026-04-09 07:03:11.161116');
INSERT INTO public.assets VALUES ('39e1e7aa-6858-483d-a99c-cb4057f29d6c', 'WEBCAM-LOGI-001', 'Logitech Brio 4K Webcam', 'Available', true, '2026-04-09 07:03:11.161121');
INSERT INTO public.assets VALUES ('3ffbd45f-9e57-40e1-9716-a253e2a756c9', 'HEADSET-SONY-001', 'Sony WH-1000XM4 Headphones', 'Available', true, '2026-04-09 07:03:11.16114');
INSERT INTO public.assets VALUES ('162df5f9-94b7-46d6-80df-4636f3ed15cb', 'TAG-0b978a', 'Test Asset', 'Assigned', true, '2026-04-09 06:29:45.446199');
INSERT INTO public.assets VALUES ('364af830-06df-47b9-a47e-f031fe7f53b6', 'TAG-47bdae', 'Test Asset', 'Assigned', true, '2026-04-09 06:31:53.040744');
INSERT INTO public.assets VALUES ('736a8411-b740-412a-8bfd-371de8cf0809', 'LAPTOP-LEN-002', 'Lenovo ThinkPad X1 Carbon', 'Assigned', true, '2026-04-09 07:03:11.161071');
INSERT INTO public.assets VALUES ('863f6f2b-0bd1-4cec-9c83-afc6d4168341', 'LAPTOP-HP-001', 'HP EliteBook 840 G8', 'Assigned', true, '2026-04-09 07:03:11.161051');
INSERT INTO public.assets VALUES ('a83529cd-14a4-4226-ba7d-f0764474d811', 'TAG-9bae76', 'Test Asset', 'Assigned', true, '2026-04-09 06:31:06.861057');


--
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.assignments VALUES ('68b4715b-d32b-4374-8c2f-bb0063c54575', '505d4dc9-8103-439c-a9bf-2c6234621673', '162df5f9-94b7-46d6-80df-4636f3ed15cb', '2026-03-10 07:03:11.193647', NULL);
INSERT INTO public.assignments VALUES ('d4867d82-12fa-4969-a7c1-c89ed940b42d', 'ecc65ca4-8af8-4c9f-b79e-308baa94673e', 'a83529cd-14a4-4226-ba7d-f0764474d811', '2026-03-15 07:03:11.197567', NULL);
INSERT INTO public.assignments VALUES ('a5a76eaf-b098-4087-be02-628aa91e01bb', 'f0a25257-a8d0-49b3-bdad-0ff532b1916e', '364af830-06df-47b9-a47e-f031fe7f53b6', '2026-03-20 07:03:11.200651', NULL);
INSERT INTO public.assignments VALUES ('7c629472-21b2-4e14-8015-050fdd20512f', 'c585ad4e-6b40-4cd4-8205-5c3595246aaa', '863f6f2b-0bd1-4cec-9c83-afc6d4168341', '2026-03-25 07:03:11.202772', NULL);
INSERT INTO public.assignments VALUES ('0617d7aa-0cf7-4c9a-b3f8-6f7753f055ac', '13ce59d9-5072-4272-be48-26d6f2cd1b8f', '736a8411-b740-412a-8bfd-371de8cf0809', '2026-03-30 07:03:11.206846', NULL);


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.roles VALUES ('cd196ab1-baf2-4aee-a57b-af358aad22ac', 'Super Admin', '["all"]');
INSERT INTO public.roles VALUES ('72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Employee', '["view:assets", "view:assignments", "view:dashboard", "create:reports", "view:my_reports"]');
INSERT INTO public.roles VALUES ('18ac1d71-abcd-4e7c-a134-a60c31cc97fc', 'Admin', '["all"]');
INSERT INTO public.roles VALUES ('d012d22a-18e7-49d6-9ac6-8b29b995ccb1', 'TestRole_574daa', '["view:assets"]');
INSERT INTO public.roles VALUES ('98d0ccd1-2c6a-4312-a9b9-5d007a10419b', 'TestRole_74cff5', '["view:assets"]');
INSERT INTO public.roles VALUES ('e2e20a01-7be7-41fb-adb5-05a7d98cc3dd', 'TestRole_aff6ac', '["view:assets"]');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users VALUES ('ecc65ca4-8af8-4c9f-b79e-308baa94673e', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Alice Johnson', 'alice@company.com', '$2b$12$0qbsCkQWu..1H35XxvSnjuhR1dFS7jMyD9FoieDxnO3XNTVonuDyq', true, '2026-04-09 07:03:11.102905', NULL);
INSERT INTO public.users VALUES ('f0a25257-a8d0-49b3-bdad-0ff532b1916e', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Bob Smith', 'bob@company.com', '$2b$12$mb1t4DS.eg7ccVWLRjPVfuzgXB3CzJsByOUGY6kdzHfeKgVdOI1he', true, '2026-04-09 07:03:11.102923', NULL);
INSERT INTO public.users VALUES ('c585ad4e-6b40-4cd4-8205-5c3595246aaa', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Carol Williams', 'carol@company.com', '$2b$12$ZILS9oEqnHT5NwF/BX/6BeBKGpc.pzT3SiAyOZ0T/24U7dbd91v5K', true, '2026-04-09 07:03:11.102932', NULL);
INSERT INTO public.users VALUES ('13ce59d9-5072-4272-be48-26d6f2cd1b8f', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'David Brown', 'david@company.com', '$2b$12$lials/nA3BeDSJ2Y6BMGFuQCCz6EWCasfGCF581OJ8ZaiGNTwK4a6', true, '2026-04-09 07:03:11.102938', NULL);
INSERT INTO public.users VALUES ('30a01867-1030-451e-a0c0-1674774726c0', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Eve Davis', 'eve@company.com', '$2b$12$JukVsMBH1zOqdAT32hnkxuC1kiVpiMZC1OYmQqKyzVvwGHDfBg/XW', true, '2026-04-09 07:03:11.102944', NULL);
INSERT INTO public.users VALUES ('1205b215-ca28-4142-9bdd-b263d6dea9a2', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Frank Miller', 'frank@company.com', '$2b$12$EfPy7i18FkZINW9hUYu6kumbKFxlcAMEKGvh.2LrHM3mKezOW6Go.', true, '2026-04-09 07:03:11.10295', NULL);
INSERT INTO public.users VALUES ('7db1d6bd-677c-47ba-b389-6e63268909ab', '18ac1d71-abcd-4e7c-a134-a60c31cc97fc', 'Admin User', 'admin@optiasset.com', '$2b$12$MJ36jlPErmTh4P98YkaCAuXDdIdBlSdhtLENpnrnSulG5.J9AJKlG', true, '2026-04-03 14:37:33.335697', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c');
INSERT INTO public.users VALUES ('505d4dc9-8103-439c-a9bf-2c6234621673', '18ac1d71-abcd-4e7c-a134-a60c31cc97fc', 'Employee User', 'employee@optiasset.com', '$2b$12$LWojdLGFPdUnRHxppfWFv.clpcnoupGVGQ4VJbZbc8C0eSPrzFiwO', true, '2026-04-03 14:37:33.335706', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c');
INSERT INTO public.users VALUES ('88322707-34cf-47e7-9cf1-a2d81a64f6d9', '72bf2cb1-12c8-4aa6-8425-4be3678aa50c', 'Super Administrator', 'superadmin@optiasset.com', '$2b$12$lV.KksY5p5oGQnHnQDuDEO1SIjfz4juNlPJnulA2xsYj5sRblGRQG', true, '2026-04-03 14:37:33.335679', 'cd196ab1-baf2-4aee-a57b-af358aad22ac');


--
-- Name: asset_reports asset_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asset_reports
    ADD CONSTRAINT asset_reports_pkey PRIMARY KEY (id);


--
-- Name: asset_status_logs asset_status_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asset_status_logs
    ADD CONSTRAINT asset_status_logs_pkey PRIMARY KEY (id);


--
-- Name: assets assets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_pkey PRIMARY KEY (id);


--
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_asset_reports_asset_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asset_reports_asset_id ON public.asset_reports USING btree (asset_id);


--
-- Name: ix_asset_reports_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asset_reports_id ON public.asset_reports USING btree (id);


--
-- Name: ix_asset_reports_reported_by_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asset_reports_reported_by_id ON public.asset_reports USING btree (reported_by_id);


--
-- Name: ix_asset_status_logs_asset_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asset_status_logs_asset_id ON public.asset_status_logs USING btree (asset_id);


--
-- Name: ix_asset_status_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asset_status_logs_id ON public.asset_status_logs USING btree (id);


--
-- Name: ix_assets_asset_tag; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_assets_asset_tag ON public.assets USING btree (asset_tag);


--
-- Name: ix_assets_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assets_id ON public.assets USING btree (id);


--
-- Name: ix_assignments_asset_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assignments_asset_id ON public.assignments USING btree (asset_id);


--
-- Name: ix_assignments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assignments_id ON public.assignments USING btree (id);


--
-- Name: ix_assignments_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assignments_user_id ON public.assignments USING btree (user_id);


--
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: asset_reports asset_reports_asset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asset_reports
    ADD CONSTRAINT asset_reports_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);


--
-- Name: asset_reports asset_reports_reported_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asset_reports
    ADD CONSTRAINT asset_reports_reported_by_id_fkey FOREIGN KEY (reported_by_id) REFERENCES public.users(id);


--
-- Name: asset_status_logs asset_status_logs_asset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asset_status_logs
    ADD CONSTRAINT asset_status_logs_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);


--
-- Name: assignments assignments_asset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);


--
-- Name: assignments assignments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- PostgreSQL database dump complete
--



