from data import supabase

def log_interaction(email: str, interaction: str):
    """Logs an interaction for a user in the 'user_memory' table."""
    response = supabase.table("user_memory").insert({
        "user_email": email,
        "interaction": interaction
    }).execute()

    if response.error:
        return {"error": response.error.message}

    return response.data

def get_recent_interactions(email: str, limit: int = 5):
    """Fetch recent interactions for memory simulation."""
    response = supabase.table("user_memory") \
        .select("interaction") \
        .eq("user_email", email) \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    if response.error:
        return {"error": response.error.message}

    return [item["interaction"] for item in response.data]
