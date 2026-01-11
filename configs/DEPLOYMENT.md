# Deployment Requirements

## Target Environment
Describe where the app will run (VM, container, PaaS) and required runtime.

## Services
- Streamlit UI service
- FastAPI service

## Configuration
List required environment variables and configuration files. At minimum:
- `SUPABASE_URL` (Supabase project URL/ID)
- `SUPABASE_ANON_KEY` (Supabase public anon key)

Optional:
- `SUPABASE_REDIRECT_URL` (OAuth redirect, defaults to `http://localhost:8501`)
- `SUPABASE_TABLE` (defaults to `time_entries`)
- `SUPABASE_ACCESS_TOKEN` (user JWT if RLS requires authenticated inserts)

## Process Management
Define how services are started/stopped (systemd, supervisor, container).
