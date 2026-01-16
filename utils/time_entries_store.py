from utils.supabase_client import get_supabase_client


def create_time_entry(payload):
    client = get_supabase_client()
    return client.table("time_entries").insert(payload).execute()
