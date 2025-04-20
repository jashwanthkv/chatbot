

from data import supabase
from datetime import datetime

class CustomMemoryManager:
    def __init__(self, table_name="user_memory"):
        self.table_name = table_name

    def log_interaction(self, user_email, interaction):
        """Logs an interaction for a user."""
        response = supabase.table(self.table_name).insert({
            "user_email": user_email,
            "interaction": interaction,
            "timestamp": datetime.utcnow().isoformat()
        }).execute()
        return response.data

    def get_recent_interactions(self, user_email, limit=5):
        """Fetch recent interactions for memory simulation."""
        response = supabase.table(self.table_name) \
            .select("interaction") \
            .eq("user_email", user_email) \
            .order("timestamp", desc=True) \
            .limit(limit) \
            .execute()
        return [item["interaction"] for item in response.data]
