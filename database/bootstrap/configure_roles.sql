\set ON_ERROR_STOP on

SELECT format('CREATE ROLE vittavaan_migrator LOGIN PASSWORD %L', :'migrator_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'vittavaan_migrator')
\gexec

SELECT format('ALTER ROLE vittavaan_migrator PASSWORD %L', :'migrator_password')
\gexec

SELECT format('CREATE ROLE vittavaan_app LOGIN PASSWORD %L', :'app_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'vittavaan_app')
\gexec

SELECT format('ALTER ROLE vittavaan_app PASSWORD %L', :'app_password')
\gexec

REVOKE CREATE ON DATABASE vittavaan FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

GRANT CONNECT ON DATABASE vittavaan TO vittavaan_migrator, vittavaan_app;
GRANT USAGE, CREATE ON SCHEMA public TO vittavaan_migrator;
GRANT USAGE ON SCHEMA public TO vittavaan_app;

ALTER TABLE IF EXISTS public.alembic_version OWNER TO vittavaan_migrator;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO vittavaan_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO vittavaan_app;

ALTER DEFAULT PRIVILEGES FOR ROLE vittavaan_migrator IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO vittavaan_app;

ALTER DEFAULT PRIVILEGES FOR ROLE vittavaan_migrator IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO vittavaan_app;
