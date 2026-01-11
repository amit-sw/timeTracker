import json
import os
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import streamlit as st

DEFAULT_TIMEZONE = "America/Los_Angeles"
LOCATION_OPTIONS = {"zoom": "Zoom", "office": "At Office"}
FIELD_ORDER = [
    "timezone",
    "start_at",
    "duration",
    "location",
    "topic",
    "progress",
    "comments",
]
PROMPTS = {
    "timezone": f"Timezone? Type `default` for {DEFAULT_TIMEZONE}.",
    "start_at": "When did the engagement start? Use `YYYY-MM-DD HH:MM`.",
    "duration": "Duration? Examples: `1h 30m`, `90m`, or `1:30`.",
    "location": "Location? Options: Zoom, At Office, or type a custom location.",
    "topic": "Topic of discussion?",
    "progress": "Progress made?",
    "comments": "Any comments? (optional, reply with `no` to skip)",
}


def _get_supabase_env():
    return (
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_ANON_KEY"),
        os.getenv("SUPABASE_TABLE", "time_entries"),
        os.getenv("SUPABASE_ACCESS_TOKEN"),
    )


def _google_oauth_url(supabase_url: str, redirect_to: str) -> str:
    base = supabase_url.rstrip("/")
    return f"{base}/auth/v1/authorize?provider=google&redirect_to={redirect_to}"


def _supabase_headers(supabase_key: str, access_token: str | None) -> dict:
    token = access_token or supabase_key
    return {
        "apikey": supabase_key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _supabase_fetch_entries(
    supabase_url: str,
    table: str,
    headers: dict,
    user_email: str,
) -> tuple[list[dict], str | None]:
    query = urlencode(
        {
            "user_email": f"eq.{user_email}",
            "order": "start_at.desc",
        }
    )
    url = f"{supabase_url.rstrip('/')}/rest/v1/{table}?{query}"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=10) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload), None
    except (HTTPError, URLError, json.JSONDecodeError) as exc:
        return [], f"Failed to fetch entries: {exc}"


def _supabase_insert_entry(
    supabase_url: str,
    table: str,
    headers: dict,
    record: dict,
) -> tuple[dict | None, str | None]:
    url = f"{supabase_url.rstrip('/')}/rest/v1/{table}"
    data = json.dumps(record).encode("utf-8")
    request = Request(url, data=data, headers=headers, method="POST")
    try:
        with urlopen(request, timeout=10) as response:
            payload = response.read().decode("utf-8")
        inserted = json.loads(payload)
        return (inserted[0] if isinstance(inserted, list) and inserted else record), None
    except (HTTPError, URLError, json.JSONDecodeError) as exc:
        return None, f"Failed to insert entry: {exc}"


def _parse_timezone(text: str) -> tuple[str | None, str | None]:
    cleaned = text.strip()
    if not cleaned or cleaned.lower() == "default":
        return DEFAULT_TIMEZONE, None
    lowered = cleaned.lower()
    if lowered in {"pt", "pst", "pdt", "pacific", "pacific time"}:
        return DEFAULT_TIMEZONE, None
    try:
        ZoneInfo(cleaned)
    except Exception:
        return None, "Unknown timezone. Try `America/Los_Angeles` or `UTC`."
    return cleaned, None


def _parse_start_datetime(text: str, tz_name: str) -> tuple[str | None, str | None]:
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"):
        try:
            naive = datetime.strptime(text.strip(), fmt)
            tzinfo = ZoneInfo(tz_name)
            aware = naive.replace(tzinfo=tzinfo)
            return aware.isoformat(), None
        except ValueError:
            continue
    return None, "Use format `YYYY-MM-DD HH:MM` (e.g., 2025-01-15 09:30)."


def _parse_duration(text: str) -> tuple[tuple[int, int] | None, str | None]:
    cleaned = text.strip().lower()
    if not cleaned:
        return None, "Enter a duration."
    if ":" in cleaned:
        parts = cleaned.split(":", 1)
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            hours = int(parts[0])
            minutes = int(parts[1])
            if minutes < 60:
                return (hours, minutes), None
        return None, "Use `H:MM` format (e.g., 1:30)."

    digits = "".join(ch if ch.isdigit() else " " for ch in cleaned).split()
    numbers = [int(value) for value in digits if value.isdigit()]
    hours = minutes = 0

    if "h" in cleaned and numbers:
        hours = numbers[0]
        if len(numbers) > 1:
            minutes = numbers[1]
    elif "m" in cleaned and numbers:
        minutes = numbers[0]
    elif numbers:
        hours = numbers[0]
        if len(numbers) > 1:
            minutes = numbers[1]

    if hours == 0 and minutes == 0:
        return None, "Enter a duration like `1h 30m` or `90m`."
    if minutes >= 60:
        extra_hours = minutes // 60
        minutes = minutes % 60
        hours += extra_hours
    return (hours, minutes), None


def _normalize_location(text: str) -> str:
    cleaned = text.strip()
    lowered = cleaned.lower()
    for key, value in LOCATION_OPTIONS.items():
        if key in lowered:
            return value
    return cleaned


def _init_state() -> None:
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("entry_draft", {})
    st.session_state.setdefault("awaiting_field", FIELD_ORDER[0])
    st.session_state.setdefault("last_prompted_field", None)
    st.session_state.setdefault("insert_result", None)


def _prompt_for_field(field: str) -> None:
    if st.session_state.get("last_prompted_field") == field:
        return
    st.session_state["chat_history"].append({"role": "assistant", "content": PROMPTS[field]})
    st.session_state["last_prompted_field"] = field


def _advance_field() -> None:
    entry = st.session_state["entry_draft"]
    for field in FIELD_ORDER:
        if field not in entry:
            st.session_state["awaiting_field"] = field
            _prompt_for_field(field)
            return
    st.session_state["awaiting_field"] = None


def _handle_user_input(user_input: str) -> None:
    entry = st.session_state["entry_draft"]
    field = st.session_state.get("awaiting_field")

    if not field:
        _advance_field()
        return

    if field == "start_at":
        tz_name = entry.get("timezone", DEFAULT_TIMEZONE)
        start_at, error = _parse_start_datetime(user_input, tz_name)
        if error:
            st.session_state["chat_history"].append({"role": "assistant", "content": error})
            return
        entry["start_at"] = start_at

    elif field == "timezone":
        tz_name, error = _parse_timezone(user_input)
        if error:
            st.session_state["chat_history"].append({"role": "assistant", "content": error})
            return
        entry["timezone"] = tz_name

    elif field == "duration":
        parsed, error = _parse_duration(user_input)
        if error:
            st.session_state["chat_history"].append({"role": "assistant", "content": error})
            return
        hours, minutes = parsed
        entry["duration_hours"] = hours
        entry["duration_minutes"] = minutes

    elif field == "location":
        location = _normalize_location(user_input)
        if not location:
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": "Please provide a location."}
            )
            return
        entry["location"] = location

    elif field == "topic":
        topic = user_input.strip()
        if not topic:
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": "Please provide a topic."}
            )
            return
        entry["topic"] = topic

    elif field == "progress":
        progress = user_input.strip()
        if not progress:
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": "Please describe the progress made."}
            )
            return
        entry["progress"] = progress

    elif field == "comments":
        cleaned = user_input.strip()
        if cleaned.lower() in {"no", "none", "skip", "n/a"}:
            entry["comments"] = None
        else:
            entry["comments"] = cleaned

    _advance_field()


def _render_entries(entries: list[dict]) -> None:
    if not entries:
        st.write("No entries yet.")
        return
    rows = []
    for entry in entries:
        rows.append(
            {
                "Start": entry.get("start_at"),
                "Duration": f"{entry.get('duration_hours', 0)}h {entry.get('duration_minutes', 0)}m",
                "Location": entry.get("location"),
                "Topic": entry.get("topic"),
                "Progress": entry.get("progress"),
                "Comments": entry.get("comments") or "",
            }
        )
    st.dataframe(rows, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Time Tracker", page_icon="TT", layout="centered")

    st.title("Time Tracker")
    st.write("Track your time across projects with a simple, focused workflow.")

    supabase_url, supabase_key, supabase_table, access_token = _get_supabase_env()
    if not supabase_url or not supabase_key:
        st.warning("Set SUPABASE_URL and SUPABASE_ANON_KEY to enable login and storage.")

    st.subheader("Sign in")
    st.caption("Choose email magic link or Google to continue.")

    with st.form("email_login"):
        email = st.text_input("Email", placeholder="you@example.com")
        submitted = st.form_submit_button("Send magic link")
        if submitted:
            if not email:
                st.error("Enter an email address to receive a magic link.")
            elif not supabase_url or not supabase_key:
                st.error("Supabase is not configured yet.")
            else:
                st.session_state["user_email"] = email.strip()
                st.info("Magic link flow will be wired to Supabase Auth.")
                st.success("Signed in for now (temporary until auth is wired).")

    st.divider()

    redirect_to = os.getenv("SUPABASE_REDIRECT_URL", "http://localhost:8501")
    if supabase_url:
        google_url = _google_oauth_url(supabase_url, redirect_to)
        st.link_button("Continue with Google", google_url, use_container_width=True)
    else:
        st.button("Continue with Google", disabled=True, use_container_width=True)

    user_email = st.session_state.get("user_email")
    if not user_email:
        st.info("Complete login to view and add time entries.")
        return
    st.caption(f"Signed in as {user_email}")

    _init_state()

    st.subheader("Your time entries")
    entries: list[dict] = []
    if supabase_url and supabase_key:
        headers = _supabase_headers(supabase_key, access_token)
        entries, error = _supabase_fetch_entries(
            supabase_url, supabase_table, headers, user_email
        )
        if error:
            st.error(error)
    _render_entries(entries)

    st.subheader("Add a new entry")
    if st.session_state.get("awaiting_field"):
        _prompt_for_field(st.session_state["awaiting_field"])

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Describe your entry")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        _handle_user_input(user_input)

    if st.session_state.get("awaiting_field") is None:
        entry = st.session_state["entry_draft"]
        entry_payload = {
            "user_email": user_email,
            "start_at": entry["start_at"],
            "timezone": entry.get("timezone", DEFAULT_TIMEZONE),
            "duration_hours": entry["duration_hours"],
            "duration_minutes": entry["duration_minutes"],
            "location": entry["location"],
            "topic": entry["topic"],
            "progress": entry["progress"],
            "comments": entry.get("comments"),
        }

        if not supabase_url or not supabase_key:
            st.error("Supabase is not configured; cannot save entry yet.")
        else:
            headers = _supabase_headers(supabase_key, access_token)
            inserted, error = _supabase_insert_entry(
                supabase_url, supabase_table, headers, entry_payload
            )
            if error:
                st.error(error)
            else:
                st.success("Entry added to Supabase.")
                if inserted:
                    entries.insert(0, inserted)
                st.session_state["entry_draft"] = {}
                st.session_state["awaiting_field"] = FIELD_ORDER[0]
                st.session_state["last_prompted_field"] = None
                st.session_state["chat_history"].append(
                    {
                        "role": "assistant",
                        "content": "Ready for another entry. "
                        f"Timezone? Type `default` for {DEFAULT_TIMEZONE}.",
                    }
                )


if __name__ == "__main__":
    main()
