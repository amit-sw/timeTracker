CREATE OR REPLACE FUNCTION get_schema()
RETURNS TABLE (name text)
LANGUAGE sql
AS $$

SELECT
    'CREATE TABLE ' || quote_ident(table_schema) || '.' || quote_ident(table_name) || E' (\n' ||
    string_agg(
        '    ' || quote_ident(column_name) || ' ' || data_type ||
        CASE
            WHEN character_maximum_length IS NOT NULL
            THEN '(' || character_maximum_length || ')'
            ELSE ''
        END ||
        CASE
            WHEN is_nullable = 'NO' THEN ' NOT NULL'
            ELSE ''
        END,
        E',\n'
        ORDER BY ordinal_position
    ) || E'\n);\n'
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema','extensions','storage','vault','realtime')
GROUP BY table_schema, table_name
ORDER BY table_schema, table_name;
$$