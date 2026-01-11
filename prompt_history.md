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
