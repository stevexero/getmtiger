import os
from supabase import create_client, Client

SB_URL = os.environ.get('SUPABASE_URL')
if not SB_URL:
    raise ValueError("Configuration error: SUPABASE_URL is not set.")

SB_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
if not SB_KEY:
    raise ValueError("Configuration error: SUPABASE_SERVICE_ROLE_KEY is not set.")

supabase: Client = create_client(SB_URL, SB_KEY)


#
# Save Unique IP Address to Database if it doesn't exist
#
def save_ip_address(ip_address):
    try:
        query = supabase.table('ip_addresses').select('*').eq('ip', ip_address).execute()
        if len(query.data) == 0:
            supabase.table('ip_addresses').insert({'ip': ip_address}).execute()
            return {"message": "IP address added to the database"}
        else:
            return {"message": "IP address already exists in the database"}
    except Exception as e:
        return {"error": str(e)}
