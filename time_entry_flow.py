import json
import os
import uuid

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from utils.time_entries_store import create_time_entry


REQUIRED_FIELDS = [
    "started_at",
    "timezone",
    "duration",
    "location",
    "topic",
    "progress",
    "project",
]


def handle_user_message_stream(messages, profile_id):
    _ensure_state()
    prompt = _latest_user_message(messages)
    if not prompt:
        return iter(())
    if st.session_state["awaiting_confirmation"]:
        status = _handle_confirmation(prompt, profile_id)
        draft = status.get("draft") or {}
        return _stream_response(messages, draft, [], status)
    result = _extract_entry(messages, st.session_state["time_entry_draft"])
    draft = result["draft"]
    st.session_state["time_entry_draft"] = draft
    missing = _missing_fields(draft)
    if not missing:
        st.session_state["awaiting_confirmation"] = True
        st.session_state["pending_entry"] = _build_payload(profile_id, draft)
    status = {"state": "collect", "error": result.get("error")}
    return _stream_response(messages, draft, missing, status)


def _handle_confirmation(prompt, profile_id):
    payload = st.session_state.get("pending_entry")
    if _is_affirmative(prompt):
        if payload:
            try:
                create_time_entry(payload)
            except Exception as exc:
                return {"state": "error", "error": str(exc), "draft": payload}
        saved = payload or {}
        _reset_draft()
        return {"state": "saved", "draft": saved}
    if _is_negative(prompt):
        st.session_state["awaiting_confirmation"] = False
        return {"state": "rejected", "draft": st.session_state["time_entry_draft"]}
    return {"state": "confirm", "draft": st.session_state["time_entry_draft"]}


def _extract_entry(messages, draft):
    llm = _get_llm()
    history = _build_history(messages, _extraction_prompt(draft))
    result = llm.invoke(history)
    return _parse_draft(result.content, draft)


def _build_history(messages, system_prompt):
    history = [SystemMessage(content=system_prompt)]
    for message in messages:
        role = message.get("role")
        content = message.get("content", "")
        if role == "user":
            history.append(HumanMessage(content=content))
        elif role == "assistant":
            history.append(AIMessage(content=content))
    return history


def _parse_draft(content, draft):
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {"draft": draft, "error": "parse"}
    updated = data.get("draft", {})
    return {"draft": _merge_draft(draft, updated), "error": None}


def _merge_draft(existing, updated):
    merged = dict(existing)
    for key, value in updated.items():
        if value not in (None, ""):
            merged[key] = value
    return merged


def _missing_fields(draft):
    missing = []
    for field in REQUIRED_FIELDS:
        value = draft.get(field)
        if value in (None, ""):
            missing.append(field)
    return missing


def _stream_response(messages, draft, missing, status):
    llm = _get_llm()
    prompt = _response_prompt(draft, missing, status)
    history = _build_history(messages, prompt)
    for chunk in llm.stream(history):
        content = getattr(chunk, "content", "") or ""
        if content:
            yield content


def _extraction_prompt(draft):
    return (
        "Extract billable time entry fields and return JSON only. "
        "Return keys: draft. draft should include started_at (ISO 8601), timezone (IANA), "
        "duration (minutes int), location, topic, progress, project, comments if present. "
        f"Current draft: {json.dumps(draft)}."
    )


def _response_prompt(draft, missing, status):
    base = (
        "You help log billable time entries. Use the provided draft only. "
        "If fields are missing, ask for all missing fields in one message. "
        "If complete, summarize values and ask for confirmation. "
        "If status.state is saved, confirm the entry was saved. "
        "If status.state is rejected, ask what to change. "
        "If status.state is confirm, ask for yes or no. "
        "If status.state is error, apologize and include status.error."
    )
    return f"{base} Draft: {json.dumps(draft)}. Missing: {missing}. Status: {status}."


def _build_payload(profile_id, draft):
    payload = {
        "id": str(uuid.uuid4()),
        "started_at": draft.get("started_at"),
        "timezone": draft.get("timezone"),
        "duration": _coerce_duration(draft.get("duration")),
        "location": draft.get("location"),
        "topic": draft.get("topic"),
        "progress": draft.get("progress"),
        "project": draft.get("project"),
    }
    if profile_id:
        payload["user_id"] = profile_id
    comments = draft.get("comments")
    if comments:
        payload["comments"] = comments
    return payload


def _latest_user_message(messages):
    for message in reversed(messages):
        if message.get("role") == "user":
            return message.get("content", "")
    return ""


def _is_affirmative(text):
    normalized = text.strip().lower()
    return normalized in {"yes", "y", "sure", "confirm", "ok", "okay"}


def _is_negative(text):
    normalized = text.strip().lower()
    return normalized in {"no", "n", "nope", "cancel"}


def _ensure_state():
    st.session_state.setdefault("time_entry_draft", {})
    st.session_state.setdefault("awaiting_confirmation", False)
    st.session_state.setdefault("pending_entry", None)


def _reset_draft():
    st.session_state["time_entry_draft"] = {}
    st.session_state["awaiting_confirmation"] = False
    st.session_state["pending_entry"] = None


def _coerce_duration(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def _get_llm():
    api_key = _get_openai_key()
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in environment or Streamlit secrets.")
    _configure_langsmith()
    model = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    return ChatOpenAI(model=model, api_key=api_key)


def _get_openai_key():
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY")


def _configure_langsmith():
    _set_env_from_secret("LANGCHAIN_API_KEY")
    _set_env_from_secret("LANGCHAIN_PROJECT")
    _set_env_from_secret("LANGCHAIN_ENDPOINT")
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")


def _set_env_from_secret(key):
    if key in st.secrets and st.secrets[key]:
        os.environ[key] = str(st.secrets[key])
