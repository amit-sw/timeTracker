# Prompt History

1. "Generate a file named AGENTS.md that serves as a contributor guide for this repository.
Your goal is to produce a clear, concise, and well-structured document with descriptive headings and actionable explanations for each section.
Follow the outline below, but adapt as needed — add sections if relevant, and omit those that do not apply to this project.

Document Requirements

- Title the document "Repository Guidelines".
- Use Markdown headings (#, ##, etc.) for structure.
- Keep the document concise. 200-400 words is optimal.
- Keep explanations short, direct, and specific to this repository.
- Provide examples where helpful (commands, directory paths, naming patterns).
- Maintain a professional, instructional tone.

Recommended Sections

Project Structure & Module Organization

- Outline the project structure, including where the source code, tests, and assets are located.

Build, Test, and Development Commands

- List key commands for building, testing, and running locally (e.g., npm test, make build).
- Briefly explain what each command does.

Coding Style & Naming Conventions

- Specify indentation rules, language-specific style preferences, and naming patterns.
- Include any formatting or linting tools used.

Testing Guidelines

- Identify testing frameworks and coverage requirements.
- State test naming conventions and how to run tests.

Commit & Pull Request Guidelines

- Summarize commit message conventions found in the project’s Git history.
- Outline pull request requirements (descriptions, linked issues, screenshots, etc.).

(Optional) Add other sections if relevant, such as Security & Configuration Tips, Architecture Overview, or Agent-Specific Instructions."
2. "I want to create a time tracker. Here is the tech stack: Python with Streamlit as well as non-UI interface via API. Source code maintained in Github."
3. "Code needs to have CRON jobs run through Github Actions. Dependency manager is Github."
4. "Where do I specify the UI, Testing, and Deployment requuirements? We will do CRON after the main code is done. Also I prefer FastAPI."
5. "OK"
6. "The users login via Supabase Auth - off the gate, support email + magic link, as well as Google Auth."
7. "We will have Supabase ID and Supabase Key."
8. "Yes."
9. "Lets start building the code. For Streamlit, the main page should just show a simple helpful screen along with UI for users to login - two options: email, or Google."
10. "Once logged in, the users should see the current infromation in their time tracker. It should support users making changes via a chat interface. The common use case is for the users to add a new entry. IN this case, the system should walk the user through to ensure all the information needed is present. Once the full information is available, it should add a new record to Supabase DB. The required fields are: Engagement start date and time and timezone (default Pacific Time), Duration (hours and minutes), Location (Options: Zoom, At Office, <User provided>), Topic of Discussion, Progress made, and Comments. Allf fields are mandatory except for comments, and you must ask user to provide them - the user can decline. ALso, as we build this functionality, please keep a running log of all my requests in prompt_history.md"
11. "/mcp add playwriter"
12. "Here is config file for playwriter: {
  \"mcpServers\": {
    \"playwriter\": {
      \"command\": \"npx\",
      \"args\": [\"playwriter@latest\"]
    }
  }
}"
13. "Please write my full commans to prompt_history.md, and not just a summary."
14. "Save all secret keys in .env files."
15. "Also use Playwriter to create the appropriate tables in Supabase for this App."
16. "Change the field name from duration_minutes to duration. Everything else is good."
17. "I ran the SQL in SQL editor. Please confirm that everything is good now."
18. "Please update the prompt history."

19. "Solve the Git problem here."
20. "It is not letting me create a new remote directory in Github. Please see the selection."
21. "I have files creates in the current directory and pushed to local Git. I want to set up a remote on GIthub."
22. "Repo does not exist on github."
23. "% git push -u origin main
Enter passphrase for key '/Users/amitamit/.ssh/id_rsa':

I dont know the passphrase, and Iwasnt asked before."
24. "% git remote set-url origin https://github.com/amit-sw/timeTracker.git
amitamit(base) amitamit@Amits-Mac-Studio timeTracker % 
amitamit(base) amitamit@Amits-Mac-Studio timeTracker % git push -u origin main
remote: Repository not found.
fatal: repository 'https://github.com/amit-sw/timeTracker.git/' not found"
25. "What is the git command to create an empty repo on Github?"
26. "% gh repo create amit-sw/timeTracker --public --source=. --remote=origin --push

✓ Created repository amit-sw/timeTracker on github.com
  https://github.com/amit-sw/timeTracker
X Unable to add remote \"origin\""
27. "Run the Streamlit App"
28. "First - set up venv. Second, add all dependencies to requirements.txt"
29. "Secrets (like SUPABASE_URL, SUPABASE_ANON_KEY etc.) are in file .env ; copy these also to .streamlit/secrets.toml, add .streamlit/secrets.toml to .gitignore, and then update the code to use these secrets."
30. "When I run the App, it warns me: \"Set SUPABASE_URL and SUPABASE_ANON_KEY to enable login and storage.\""
31. "UI says:  Sign in\nChoose email magic link or Google to continue.\n\nEmail\n\namit@gprof.com\n\nMagic link flow will be wired to Supabase Auth.\n\nSigned in for now (temporary until auth is wired)."
32. "I signed in via magic link but still get the same login page. The URL is http://localhost:8501/..."
33. "Same issue.URL is: http://localhost:8501/#access_token=eyJhbGciOiJFUzI1NiIsImtpZCI6ImU1YmI2YmFjLTU1MzktNDEyNi1hNWZkLTQwMjRhZTNhZTI2OSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3VuZGpudnlzb2lzZ3lsd3B2bm5uLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiIwYmIyNDI2YS1kZmI4LTQxYWItYWFhMi1kZDZkZmEzZTAwOGQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY4MTE3NzM1LCJpYXQiOjE3NjgxMTQxMzUsImVtYWlsIjoiYW1pdEBncHJvZi5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoiYW1pdEBncHJvZi5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiIwYmIyNDI2YS1kZmI4LTQxYWItYWFhMi1kZDZkZmEzZTAwOGQifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvdHAiLCJ0aW1lc3RhbXAiOjE3NjgxMTQxMzV9XSwic2Vzc2lvbl9pZCI6Ijg1MWU3MTQxLTY3OGEtNDM1Zi05YmI4LWVkOTg2YWE0ODUzNyIsImlzX2Fub255bW91cyI6ZmFsc2V9._0TYO6synUhc9ycVoFLsPDNPSzhnWlKQydakbe6X-V1zTN0mqrM74uPKBRFlJr1OY1T7fh6qO9e0ph2Wdhivaw&expires_at=1768117735&expires_in=3600&refresh_token=k56h2lwpxgl5&token_type=bearer&type=magiclink"
34. "After manually replacing # with ?, it made progress. I now see: Time Tracker\nTrack your time across projects with a simple, focused workflow.\n\nSign in\nSign in with a magic link or Google (PKCE).\n\nSigned in as None\n\nYour time entries\nFailed to fetch entries: HTTP Error 401: Unauthorized\n\nNo entries yet.\n\nAdd a new entry\nTimezone? Type default for America/Los_Angeles."
35. "For Supabase MagicLink, customize the email to let the user know that it is from AIClub, and that it is for the TimeTracker system. Also, I still need to replace # with ? - can you please fix this asap? After logging in, the screen looks like: Time Tracker\nTrack your time across projects with a simple, focused workflow.\n\nSign in\nSign in with a magic link or Google (PKCE).\n\nSigned in as None\n\nYour time entries\nFailed to fetch entries: HTTP Error 401: Unauthorized\n\nNo entries yet.\n\nAdd a new entry\nTimezone? Type default for America/Los_Angeles."
36. "Remains a Hash"
User: The browser is open on Google Cloud page in the project timetracker. Set it up so that we can use Google Sign-In for this project, saving the secret keys in .env file
User: I have finished everything, including pasting the secrets in .env
User: I still see the same behavior. Also, please remove all the code related to magic link.
User: Got Failed to exchange auth code: HTTP Error 400: Bad Request | {"code":400,"error_code":"validation_failed","msg":"invalid request: both auth code and code verifier should be non-empty"} for http://localhost:8501/?code=24335daf-b3f2-47aa-ac78-eb499d0d32d0&code_verifier=7EzTwwiNGGrpp4Vg1PjX_j3K7UZcbY9X8NHYoZOpPOc
Why are there so many files in node_modules - this is a python project
Yes.
I want to delete all the source code files here and restart from scratch.
