


import streamlit as st
import re

st.title("Supabase → Oracle Schema Converter")


def convert_datatype(pg_type):
    t = pg_type.lower()

    if "bigint" in t:
        return "NUMBER(19)"
    if "integer" in t or "int" in t:
        return "NUMBER(10)"
    if "uuid" in t:
        return "VARCHAR2(36)"
    if "timestamp with time zone" in t:
        return "TIMESTAMP WITH TIME ZONE"
    if t.strip() == "text":
        return "CLOB"
    if "jsonb" in t or "json" in t:
        return "CLOB"
    if "boolean" in t:
        return "NUMBER(1)"
    if "double precision" in t:
        return "BINARY_DOUBLE"

    return pg_type.upper()


def convert_create_table(statement):
    # remove schema prefix
    statement = re.sub(r'CREATE TABLE\s+[\w"]+\.', 'CREATE TABLE ', statement, flags=re.IGNORECASE)

    lines = statement.splitlines()
    converted_lines = []

    primary_keys = []

    for line in lines:
        stripped = line.strip()

        if stripped.upper().startswith("CREATE TABLE"):
            converted_lines.append(stripped)
            continue

        if stripped.startswith(");"):
            # append PK if found
            if primary_keys:
                pk_line = f"    CONSTRAINT pk_{table_name} PRIMARY KEY ({', '.join(primary_keys)})"
                converted_lines.append(pk_line)

            converted_lines.append(");")
            continue

        # detect column
        match = re.match(r'"?(\w+)"?\s+(.+?)(,?)$', stripped)
        if match:
            col, dtype, comma = match.groups()

            # detect NOT NULL
            not_null = "NOT NULL" in dtype.upper()

            # remove NOT NULL before datatype conversion
            dtype_clean = dtype.replace("NOT NULL", "").strip()

            oracle_type = convert_datatype(dtype_clean)

            # add default for timestamps
            has_default = "DEFAULT" in dtype.upper()
            is_timestamp = "timestamp" in dtype_clean.lower()

            new_line = f"    {col} {oracle_type}"

            if is_timestamp and not has_default:
                new_line += " DEFAULT SYSTIMESTAMP"

            if not_null:
                new_line += " NOT NULL"

            if comma:
                new_line += ","

            # heuristic: treat NOT NULL id columns as PK
            if col == "id" and not_null:
                primary_keys.append(col)
                if new_line.endswith(","):
                    new_line = new_line[:-1]

            converted_lines.append(new_line)
            continue

        converted_lines.append(stripped)

    return "\n".join(converted_lines)


def convert_schema(pg_schema):
    statements = re.findall(r'CREATE TABLE.*?\);', pg_schema, re.DOTALL | re.IGNORECASE)

    oracle_statements = []

    for stmt in statements:
        global table_name
        table_match = re.search(r'CREATE TABLE\s+("?[\w]+"?)', stmt, re.IGNORECASE)
        table_name = table_match.group(1).replace('"', '') if table_match else "table"

        oracle_statements.append(convert_create_table(stmt))

    return "\n\n".join(oracle_statements)


uploaded_file = st.file_uploader("Upload Supabase schema (.sql)", type=["sql", "txt"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")

    oracle_schema = convert_schema(content)

    st.subheader("Generated Oracle Schema")
    st.text_area("Oracle SQL", oracle_schema, height=500)

    st.download_button(
        label="Download Oracle Schema",
        data=oracle_schema,
        file_name="oracle_schema.sql",
        mime="text/plain"
    )