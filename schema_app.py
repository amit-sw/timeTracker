import streamlit as st
from supabase import create_client
import os

def get_schema():
    url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        st.error("Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY.")
        st.stop()

    client = create_client(url, key)

    # Query Postgres information_schema via RPC or SQL
    # This assumes you have a Postgres function named `get_schema`
    # If not, replace with your preferred schema query.
    response = client.rpc("get_schema").execute()

    if response.data is None:
        return {"error": "No schema returned"}

    return response.data
import json

st.title("Database Schema Viewer")

if "schema_data" not in st.session_state:
    st.session_state["schema_data"] = None

if st.button("Show"):
    st.session_state["schema_data"] = get_schema()

if st.session_state["schema_data"] is not None:
    schema_data = st.session_state["schema_data"]

    # Convert schema into plain SQL text
    if isinstance(schema_data, list):
        sql_statements = []
        for item in schema_data:
            if isinstance(item, dict) and "name" in item:
                sql_statements.append(item["name"])
            elif isinstance(item, str):
                sql_statements.append(item)
            else:
                sql_statements.append(str(item))

        schema_text = "\n\n".join(sql_statements)

    elif isinstance(schema_data, dict) and "name" in schema_data:
        schema_text = schema_data["name"]

    else:
        schema_text = schema_data if isinstance(schema_data, str) else str(schema_data)

    st.text_area("Schema SQL", schema_text, height=400)

    st.download_button(
        label="Download Schema",
        data=schema_text,
        file_name="schema.sql",
        mime="text/plain"
    )
