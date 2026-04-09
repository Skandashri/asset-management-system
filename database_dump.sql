BEGIN TRANSACTION;
CREATE TABLE asset_status_logs (
	id VARCHAR NOT NULL, 
	asset_id VARCHAR NOT NULL, 
	old_status VARCHAR, 
	new_status VARCHAR NOT NULL, 
	changed_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(asset_id) REFERENCES assets (id)
);
CREATE TABLE assets (
	id VARCHAR NOT NULL, 
	asset_tag VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	status VARCHAR NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE assignments (
	id VARCHAR NOT NULL, 
	user_id VARCHAR NOT NULL, 
	asset_id VARCHAR NOT NULL, 
	assigned_date DATETIME NOT NULL, 
	return_date DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(asset_id) REFERENCES assets (id)
);
CREATE TABLE roles (
	id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	permissions TEXT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "roles" VALUES('21e9ed2c-5f16-4567-a97b-885a1f62c9a0','Admin','["all"]');
INSERT INTO "roles" VALUES('82371563-ca24-47b4-8a68-d3ff7aff1bdc','Employee','["view:assets", "view:assignments", "view:dashboard"]');
CREATE TABLE users (
	id VARCHAR NOT NULL, 
	role_id VARCHAR, 
	name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	hashed_password VARCHAR NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);
INSERT INTO "users" VALUES('061d9f58-6fc2-46c0-b8af-603b35a5095a','21e9ed2c-5f16-4567-a97b-885a1f62c9a0','OptiAsset Admin','admin@optiasset.com','$2b$12$wfLLwG8kuEWZ8kgzsBaFa.GEz60BR5S1gmTKVe6tdt.Bdx6Rr1fhm',1,'2026-03-07 15:44:21.435762');
INSERT INTO "users" VALUES('ec324e55-b46b-48e2-8d2b-892e473ff24e','82371563-ca24-47b4-8a68-d3ff7aff1bdc','Standard Employee','employee@optiasset.com','$2b$12$AeGDLxJyQRybVbtdgj6./.nTEKWeSoz8nhTgk2CXuXCnnuMslWhP2',1,'2026-03-07 15:44:21.683830');
CREATE UNIQUE INDEX ix_roles_name ON roles (name);
CREATE INDEX ix_roles_id ON roles (id);
CREATE INDEX ix_assets_id ON assets (id);
CREATE UNIQUE INDEX ix_assets_asset_tag ON assets (asset_tag);
CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_asset_status_logs_asset_id ON asset_status_logs (asset_id);
CREATE INDEX ix_asset_status_logs_id ON asset_status_logs (id);
CREATE INDEX ix_assignments_id ON assignments (id);
CREATE INDEX ix_assignments_asset_id ON assignments (asset_id);
CREATE INDEX ix_assignments_user_id ON assignments (user_id);
COMMIT;
