import uuid

import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase_client():
    url, key = _get_supabase_credentials()
    return create_client(url, key)


def _get_supabase_credentials():
    secrets = st.secrets
    url = _get_secret_value(secrets, ["SUPABASE_URL", "supabase_url"], section="supabase")
    key = _get_secret_value(secrets, ["SUPABASE_KEY", "supabase_key"], section="supabase")
    if not url or not key:
        raise ValueError("Missing Supabase credentials in .streamlit/secrets.toml")
    return url, key


def _get_secret_value(secrets, keys, section=None):
    if section and section in secrets:
        section_data = secrets[section]
        for key in keys:
            if key in section_data:
                return section_data[key]
    for key in keys:
        if key in secrets:
            return secrets[key]
    return None


def get_or_create_profile(email, name):
    if not email:
        raise ValueError("User email is required to create a profile.")

    client = get_supabase_client()
    response = (
        client.table("profiles")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]

    payload = {"id": str(uuid.uuid4()), "email": email}
    created = client.table("profiles").insert(payload).execute()
    if created.data:
        return created.data[0]
    return None
