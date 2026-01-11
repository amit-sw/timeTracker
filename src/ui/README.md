# UI Requirements

## Purpose
Summarize the Streamlit UI goals and user flows for the time tracker.

## Core Screens
- Dashboard (active timer, summary stats)
- Project/task list
- Timer history/logs

## UX Notes
- Keep primary actions above the fold (start/stop, select project).
- Show running timer clearly with elapsed time.

## Data Contracts
List any required API endpoints or data shapes the UI depends on.

## Authentication
Use Supabase Auth with email magic-link and Google OAuth. The UI should provide a minimal login screen and persist the Supabase session for API calls.

## Acceptance Criteria
Define what "done" looks like for the UI (e.g., can start/stop timers, view history).
