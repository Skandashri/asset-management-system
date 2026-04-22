--
-- PostgreSQL database dump
--



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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: asset_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asset_categories (
    id character varying NOT NULL,
    name character varying NOT NULL,
    total_quantity integer NOT NULL,
    available_quantity integer NOT NULL
);


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
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_logs (
    id character varying NOT NULL,
    action character varying NOT NULL,
    performed_by_id character varying,
    "timestamp" timestamp without time zone NOT NULL
);


--
--

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


--
-- Name: requests; Type: TABLE; Schema: public; Owner: -
--

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


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: asset_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asset_categories (id, name, total_quantity, available_quantity) FROM stdin;
\.


--
-- Data for Name: asset_reports; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asset_reports (id, asset_id, reported_by_id, report_type, description, severity, status, created_at, resolved_at, admin_notes) FROM stdin;
b372ece7-5d83-4c49-a16e-1a03d41d848a	dd2597d8-4986-4950-a916-7c5019547c76	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	Not working	bad	Medium	Under Review	2026-04-22 13:26:55.337422	\N	it is looking 
0b6b52da-9c89-4376-9a4f-eb7217047afa	ceba4785-26e2-411b-89a5-cdc4d6e38688	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	Not working	ll	Medium	Pending	2026-04-22 16:08:56.24648	\N	\N
1b361641-98dc-4027-a9a3-ede4e08b13eb	ceba4785-26e2-411b-89a5-cdc4d6e38688	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	Not working	bad	Medium	Pending	2026-04-22 16:12:48.268105	\N	\N
dc9f8c5b-335d-42df-9dd7-35b006305976	ceba4785-26e2-411b-89a5-cdc4d6e38688	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	Not working	bad	Medium	Under Review	2026-04-22 15:48:43.818501	\N	kklp;m;m;mmnnkm
df4c5099-a9ce-4831-ad9b-d0519e68b950	ceba4785-26e2-411b-89a5-cdc4d6e38688	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	Not working	455	Medium	Under Review	2026-04-22 16:00:46.123884	\N	
\.


--
-- Data for Name: asset_status_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asset_status_logs (id, asset_id, old_status, new_status, changed_at) FROM stdin;
f7cdea86-fd6f-4806-8370-45116fa79f97	46a0f4bd-2ba3-43fa-bf09-d0f136338f69	Available	Assigned	2026-03-23 03:20:34.375327
aeb13b7c-505b-4b72-b8fc-e6bc88116172	86464c0a-d9c3-4653-b490-8174276b3d27	Available	Assigned	2026-03-28 03:20:34.376486
fef1e0a9-27a6-409e-b805-3da2f141a484	146ddfef-c187-4d33-9aa6-0e5db01e698f	Available	Assigned	2026-04-02 03:20:34.377482
cfc70c1f-dc44-4e09-bdd3-b2b948755f08	f639fe37-fa1a-4614-a382-7b736cead51f	Available	Assigned	2026-04-07 03:20:34.37879
667ed84b-366d-485f-a5d0-5def2729940a	7de319e5-bdd7-480c-8c2f-371b39c64405	Available	Assigned	2026-04-12 03:20:34.380032
4bccc6e8-dbf4-41f4-b364-3e258b0b0a8c	dd2597d8-4986-4950-a916-7c5019547c76	Available	Assigned	2026-04-22 13:03:27.158356
9e0e93db-b73a-4cf8-8698-d6c9e86c294e	a8aeb81b-0b2b-47e8-984c-6b92933ec0aa	Available	Assigned	2026-04-22 14:47:12.727533
09a80ed8-6a4e-4e8a-8a00-7c9bc73e4575	a3c45364-c2a0-416f-9310-f84d7b68e265	Available	Assigned	2026-04-22 14:47:47.362248
2df3b3b6-6366-4cea-be16-1d133a6f9067	d4dd71d2-c389-492f-af20-80e0febc4b42	Available	Assigned	2026-04-22 14:50:43.730277
4379a155-1545-4685-a38d-5c0560cea42c	ceba4785-26e2-411b-89a5-cdc4d6e38688	Available	Assigned	2026-04-22 15:06:39.05488
f7090e10-fca1-4f5a-840d-91e2942e777a	310d07e9-93a0-4d05-836a-9a0b41f1ed37	Available	Assigned	2026-04-22 17:43:31.764719
\.


--
-- Data for Name: assets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.assets (id, asset_tag, name, category_id, purchase_date, cost, image_url, document_url, vendor, location, status, is_active, created_at) FROM stdin;
42495a36-dc40-4109-8250-4eb69aaea287	IPHONE-13-001	iPhone 13 Pro 256GB	\N	\N	\N	\N	\N	\N	\N	Available	t	2026-04-22 03:20:34.361342
146ddfef-c187-4d33-9aa6-0e5db01e698f	MONITOR-DELL-001	Dell UltraSharp 27" U2720Q	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361322
46a0f4bd-2ba3-43fa-bf09-d0f136338f69	LAPTOP-HP-001	HP EliteBook 840 G8	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361312
7de319e5-bdd7-480c-8c2f-371b39c64405	KEYBOARD-LOGI-001	Logitech MX Keys Keyboard	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361329
86464c0a-d9c3-4653-b490-8174276b3d27	LAPTOP-LEN-002	Lenovo ThinkPad X1 Carbon	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361319
f639fe37-fa1a-4614-a382-7b736cead51f	MONITOR-LG-002	LG 27" 4K UHD Monitor	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361325
68113f35-f50f-4cf6-b6c3-0606a7d0b6e1	TAG-f7bba2	Updated Test Asset	\N	\N	\N	\N	\N	\N	\N	Maintenance	t	2026-04-22 05:53:11.374947
9c1e6928-114a-4ed3-b20e-21f591543971	TAG-6743d5	Updated Test Asset	\N	\N	\N	\N	\N	\N	\N	Maintenance	t	2026-04-22 06:57:30.953229
9fd70fe6-877c-4285-93f1-9b1ea4f6adbc	TAG-4921e5	Updated Test Asset	\N	\N	\N	\N	\N	\N	\N	Maintenance	t	2026-04-22 07:00:45.507755
04b87bd5-7061-478f-820b-2807c3090373	TAG-bfea90	Updated Test Asset	\N	\N	\N	\N	\N	\N	\N	Maintenance	t	2026-04-22 07:07:17.731548
1fa5c546-a6a4-4568-abca-4ce6f317c15c	MOUSE-LOGI-001	Logitech MX Master 3 Mouse	\N	\N	\N	\N	\N	\N	\N	Available	f	2026-04-22 03:20:34.361331
6597f303-4867-4f31-b041-b0d185208c26	ff	ff	\N	\N	0	\N	\N	ff	ff	Available	f	2026-04-22 12:40:01.923364
dd2597d8-4986-4950-a916-7c5019547c76	DESK-STAND-001	Standing Desk Electric 48"	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361337
a8aeb81b-0b2b-47e8-984c-6b92933ec0aa	IPAD-PRO-001	iPad Pro 12.9" M1	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361339
a3c45364-c2a0-416f-9310-f84d7b68e265	A101	macbook	\N	\N	122	\N	\N	me	hassan	Assigned	t	2026-04-22 12:36:29.56295
d4dd71d2-c389-492f-af20-80e0febc4b42	HEADSET-SONY-001	Sony WH-1000XM4 Headphones	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361347
ceba4785-26e2-411b-89a5-cdc4d6e38688	WEBCAM-LOGI-001	Logitech Brio 4K Webcam	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 03:20:34.361344
bed45e21-e0bc-48a1-b04f-33582db863e9	CHAIR-HERMAN-001	Herman Miller Aeron Chair	\N	\N	\N	\N	\N	\N	\N	Available	f	2026-04-22 03:20:34.361334
2f92f6c0-2633-4df1-975d-6efdb20eaa19	TAG-afcb3c	Updated Test Asset	\N	\N	\N	\N	\N	\N	\N	Available	t	2026-04-22 05:37:56.704304
a1baadd0-7c1b-4066-aa67-7e407c754e8b	A0011	macbook pro max	\N	\N	450	\N	\N	sam	hassan	Available	t	2026-04-22 16:20:45.760915
310d07e9-93a0-4d05-836a-9a0b41f1ed37	TAG-e1a540	Test Asset	\N	\N	\N	\N	\N	\N	\N	Assigned	t	2026-04-22 05:30:53.294129
\.


--
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.assignments (id, user_id, asset_id, assigned_date, return_date) FROM stdin;
34380a98-8a7a-414d-875b-98a3d913eadf	01c685bf-1fa6-4659-96e4-d262f91fa560	46a0f4bd-2ba3-43fa-bf09-d0f136338f69	2026-03-23 03:20:34.375327	\N
9851cd7a-9c49-46c4-a2fc-a98d3ae677e9	207ec37f-40ea-4caf-8c6f-3277acaaaf18	86464c0a-d9c3-4653-b490-8174276b3d27	2026-03-28 03:20:34.376486	\N
27d9e74e-359c-4104-ac00-4dc9c8426a4d	ba57235f-eed2-4ebe-870b-3280ad499be4	146ddfef-c187-4d33-9aa6-0e5db01e698f	2026-04-02 03:20:34.377482	\N
0c45e2d7-ef47-4a8b-b760-3d87addf4dc2	a184f757-e245-4fff-a7f4-a695b15a2448	f639fe37-fa1a-4614-a382-7b736cead51f	2026-04-07 03:20:34.37879	\N
c0f34ee7-509e-452a-8e5c-3ca5428b97e7	d0327810-3f89-47d8-ae08-6d80ddf339bb	7de319e5-bdd7-480c-8c2f-371b39c64405	2026-04-12 03:20:34.380032	\N
df12bc35-c761-4abf-afc5-d06f3a9e56a0	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	dd2597d8-4986-4950-a916-7c5019547c76	2026-04-22 13:03:27.164011	\N
5cb09859-f4fd-4edb-8dab-4cc3df39b476	207ec37f-40ea-4caf-8c6f-3277acaaaf18	a8aeb81b-0b2b-47e8-984c-6b92933ec0aa	2026-04-22 14:47:12.731272	\N
7ca305ad-49a0-4d0a-80d0-d8825595908a	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	a3c45364-c2a0-416f-9310-f84d7b68e265	2026-04-22 14:47:47.363619	\N
8b3cebf4-93f4-4323-8c14-2b65f46185bf	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	d4dd71d2-c389-492f-af20-80e0febc4b42	2026-04-22 14:50:43.731268	\N
382d5dc1-e3ff-44b3-bc67-abeec8908059	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	ceba4785-26e2-411b-89a5-cdc4d6e38688	2026-04-22 15:06:39.056172	\N
511a6037-4db8-491b-9c42-a932f38852e3	207ec37f-40ea-4caf-8c6f-3277acaaaf18	310d07e9-93a0-4d05-836a-9a0b41f1ed37	2026-04-22 17:43:31.767315	\N
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.audit_logs (id, action, performed_by_id, "timestamp") FROM stdin;
\.


--
--

fdb13cb7-934e-4c36-9dc4-b69aa43ee38d	2ee122ba-0acb-4ed8-9338-fa87c1cabef8	New Equipment Request	Employee User requested Test Laptop (Laptop)	request	f	2026-04-22 16:57:52.832058	\N	/admin-requests	{"request_id": "89d42631-5e4f-432a-80c5-e99fe024707d", "user_id": "bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7"}
1d1f24a8-32cc-48d3-bab3-b89765374fe3	939c9bfc-ffb2-4d56-ae30-23ebbce4e2ca	New Equipment Request	Employee User requested Test Laptop (Laptop)	request	f	2026-04-22 16:57:52.85009	\N	/admin-requests	{"request_id": "89d42631-5e4f-432a-80c5-e99fe024707d", "user_id": "bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7"}
896ce7d8-47cd-4e69-b17a-bb81e46886dd	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	Request Submitted	Your request for Test Laptop has been submitted successfully.	request	f	2026-04-22 16:57:52.864319	\N	/my-requests	{"request_id": "89d42631-5e4f-432a-80c5-e99fe024707d"}
\.


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.requests (id, user_id, asset_id, item_name, item_type, notes, status, admin_notes, requested_at) FROM stdin;
a731e304-e8ed-471a-9ba6-aee8dc7c6ba2	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	skanda	Laptop	\N	Rejected	it is costly	2026-04-22 12:57:45.684546
986512ae-a217-4755-a0b7-13775b513da5	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	a8aeb81b-0b2b-47e8-984c-6b92933ec0aa	mouse	Equipment	my old mouse is not woking good	Approved	\N	2026-04-22 12:59:09.782708
5353a916-a3ec-4bd6-9059-f1a086cc3e94	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	Test Laptop M3	Laptop	Needed for development	Approved	Approved for new project - Q2 2024	2026-04-22 13:22:20.5166
de4c5754-fa2f-4138-addb-d246d0fa20a5	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	bed45e21-e0bc-48a1-b04f-33582db863e9	mouse	Equipment	my old mouse is not woking good	Approved	\N	2026-04-22 14:21:06.527277
1ee37c42-2af4-41ed-86d9-4bc3e9bbff8e	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	bed45e21-e0bc-48a1-b04f-33582db863e9	macbook	Laptop	\N	Approved	\N	2026-04-22 14:18:24.644422
b6412de8-69fd-4e6b-bab3-81d1ac680766	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	mouse	Equipment	my old mouse is not woking good	Rejected	out of stock	2026-04-22 14:18:45.246001
537213f2-1817-49c2-a8b8-fbb663b261bc	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	856	Equipment		Pending	\N	2026-04-22 14:24:53.557255
137c1fc0-b68b-4c40-9b41-0c1d93131c7e	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	keyboard	Equipment	damages	Pending	\N	2026-04-22 14:25:58.849674
18883887-556c-451d-85ea-30efd19cd5ff	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	macbook pro 	Laptop	\N	Pending	\N	2026-04-22 14:46:11.108673
52dc193e-d780-4786-b134-644ce7d52f4b	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	kkkk	Accessory	damages	Pending	\N	2026-04-22 15:22:04.071591
23cbd0f7-18d3-4128-a210-fcad4465ae0f	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	\N	mac	Laptop	\N	Pending	\N	2026-04-22 17:40:06.176086
dc197443-2b89-4e17-aaa9-2c60d067e5ef	bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	310d07e9-93a0-4d05-836a-9a0b41f1ed37	usb cable	Accessory		Approved	\N	2026-04-22 16:48:19.403947
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (id, name, permissions) FROM stdin;
bea322a4-011e-4e06-95bb-d6534250e8b8	Super Admin	["all"]
31ce2068-6d35-4d92-b0c3-764f032f3f9e	Employee	["view:assets", "view:assignments", "view:dashboard", "create:reports", "view:my_reports"]
3282c72b-c4f0-40d5-86b6-1fa5d86ed5ed	Admin	["view:roles", "manage:assignments", "view:users", "manage:users", "view:assignments", "view:assets", "view:reports", "view:dashboard", "manage:roles", "manage:reports", "manage:assets"]
1db79e62-8bcc-41e0-94dd-b30971133f28	TestRole_97c728	["view:assets"]
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, role_id, secondary_role_id, name, email, hashed_password, department, contact, is_active, created_at) FROM stdin;
01c685bf-1fa6-4659-96e4-d262f91fa560	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Alice Johnson	alice@company.com	$2b$12$8wU3YJyYQbnqrP3n8zHDj.1MW6cmq1cxPW/5/eRxlOHvA9AQUoSm.	\N	\N	t	2026-04-22 03:20:34.336042
207ec37f-40ea-4caf-8c6f-3277acaaaf18	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Bob Smith	bob@company.com	$2b$12$u0gNRtXTR4WuMKclG8p56OFx7XwrFVT6Z4s17w7SH4BtrY386/dfe	\N	\N	t	2026-04-22 03:20:34.336045
ba57235f-eed2-4ebe-870b-3280ad499be4	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Carol Williams	carol@company.com	$2b$12$7qVkFS2m8fB3OV3pEG7gxO9tJtXzlGmgONRs.KYlexDlWUBQJyyye	\N	\N	t	2026-04-22 03:20:34.336048
a184f757-e245-4fff-a7f4-a695b15a2448	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	David Brown	david@company.com	$2b$12$8J2EnKf31.u6N2qpv4f1qOutg3ZxNVuwxJbrrf4rmp4e2l9bbxiWy	\N	\N	t	2026-04-22 03:20:34.336051
2582acb7-66fa-4f02-99b8-97e3c8b0179e	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Frank Miller	frank@company.com	$2b$12$f8AV0E5N7XpSE3qgoKVhhe2jOEX3za0rvtyyQ3qF/IxEQOYY.vrpm	\N	\N	t	2026-04-22 03:20:34.336055
2ee122ba-0acb-4ed8-9338-fa87c1cabef8	bea322a4-011e-4e06-95bb-d6534250e8b8	\N	Super Administrator	superadmin@optiasset.com	$2b$12$T86ya9ry.HeJTDGYBCkGxu5PKhNZHVlF8zDIs3/b6Fc7aRtf9GQ.S	\N	\N	t	2026-04-22 03:20:34.336031
939c9bfc-ffb2-4d56-ae30-23ebbce4e2ca	3282c72b-c4f0-40d5-86b6-1fa5d86ed5ed	\N	Admin User	admin@optiasset.com	$2b$12$2kG83OJ2UQjKzoIk8xbd7OJ2xcnK.Tj9K.rbWaNaCyABEKgc3bTRu	\N	\N	t	2026-04-22 03:20:34.336038
bb7ee643-c9cb-49de-a6f7-ca5f8abb46b7	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Employee User	employee@optiasset.com	$2b$12$VISlHoNLFye2RfkR76pNXOppZIQfs3zGoufymAaG/6.u8mQWHMtOG	\N	\N	t	2026-04-22 07:06:58.600134
56d3caed-1808-4bf1-b361-784c511f2405	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Test Employee 1776860555	test_emp_1776860555@company.com	$2b$12$4scIub7ks6ZFUXEkyXv5JOz3nAh/RkUzkARMLvfMCb/IppkpzT4N6	\N	\N	t	2026-04-22 12:22:36.021277
aba3617f-4314-4140-874f-12f85cc09557	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	skanda	skandashri@optiasset.com	$2b$12$A8M3e65aZ8JbTmEmMTzQyOwe1T.Mxmww3U0JpSZ0p7EFezOzJWgl6	\N	\N	t	2026-04-22 12:35:10.034542
d0327810-3f89-47d8-ae08-6d80ddf339bb	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	Eve Davis	eve@company.com	$2b$12$DsFeyoQ1Uz39JWyeE3x8XOOBdbbfPWLFdPvXpcCWdw147Bulzvo2m	\N	\N	f	2026-04-22 03:20:34.336053
a8bb319d-ee45-4ad3-944a-1c29dfe3b961	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	john	john@optiasset.com	$2b$12$NHO99TlxLnn2TwbMIcybau8jcsHDw0JgOwAv0OXQfjRVZ5rjLkJm6	tech	55666	t	2026-04-22 13:29:57.924155
7e4fc6f2-17b3-4968-97c9-339e45318a2b	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	john	johne@optiasset.com	$2b$12$NEWH0sd4f3ogVBqcL20FO.FvR5Q9hEkdiDmz0PBzaTT8kQFDQHKOC	\N	\N	t	2026-04-22 13:30:31.935786
5a0f0b27-c047-4aec-be13-511cf9049c47	31ce2068-6d35-4d92-b0c3-764f032f3f9e	\N	joe	joe@optiasset.com	$2b$12$M877gCH7wOJsJGQmcjvvjO5VGhYPKpQoj.rUVkfu6UOIZTO5PRG/2	\N	\N	t	2026-04-22 17:43:09.640092
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: asset_categories asset_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asset_categories
    ADD CONSTRAINT asset_categories_pkey PRIMARY KEY (id);


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
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
--



--
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


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
-- Name: ix_asset_categories_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asset_categories_id ON public.asset_categories USING btree (id);


--
-- Name: ix_asset_categories_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_asset_categories_name ON public.asset_categories USING btree (name);


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
-- Name: ix_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);


--
-- Name: ix_audit_logs_performed_by_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_logs_performed_by_id ON public.audit_logs USING btree (performed_by_id);


--
--



--
--



--
--



--
-- Name: ix_requests_asset_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_requests_asset_id ON public.requests USING btree (asset_id);


--
-- Name: ix_requests_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_requests_id ON public.requests USING btree (id);


--
-- Name: ix_requests_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_requests_user_id ON public.requests USING btree (user_id);


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
-- Name: assets assets_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.asset_categories(id);


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
-- Name: audit_logs audit_logs_performed_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_performed_by_id_fkey FOREIGN KEY (performed_by_id) REFERENCES public.users(id);


--
-- Name: users fk_user_secondary_role; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_user_secondary_role FOREIGN KEY (secondary_role_id) REFERENCES public.roles(id);


--
--



--
-- Name: requests requests_asset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES public.assets(id);


--
-- Name: requests requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- PostgreSQL database dump complete
--




