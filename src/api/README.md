# API Requirements

## Purpose
Document FastAPI endpoints and non-UI interface requirements for the time tracker.

## Endpoints
- `POST /timers/start`
- `POST /timers/stop`
- `GET /timers/active`
- `GET /timers/history`

## Auth
Use Supabase Auth. Support email magic-link login and Google OAuth. The API should validate Supabase JWTs on protected routes and extract the user ID from the token.

## Errors & Status Codes
List standard error responses and status codes.

## Acceptance Criteria
Define what "done" looks like for the API (e.g., start/stop timers, list history).
