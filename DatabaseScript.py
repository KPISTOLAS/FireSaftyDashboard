from supabase import create_client, Client

# Replace with your Supabase details
SUPABASE_URL = "https://vbsohfwxxezlxjqumaqr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZic29oZnd4eGV6bHhqcXVtYXFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcyMzg1NDgsImV4cCI6MjA2MjgxNDU0OH0.ZPpg5B2A6ozUMRTjapeo_GqvT9lD5jxknHr-LvddUe4"

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Test connection
    supabase.table("nodes").select("*").limit(1).execute()
except Exception as e:
    print(f"Failed to connect to Supabase: {e}")
    raise

# Function to get node information
def get_node_info(node_id):
    try:
        response = supabase.table("nodes").select("*").eq("node_id", node_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error querying node {node_id}: {e}")
        return None

def get_node_history(node_id):
    try:
        response = supabase.table("sensor_readings")\
            .select("*")\
            .eq("node_id", node_id)\
            .order("timestamp", desc=True)\
            .execute()
        return response.data
    except Exception as e:
        print(f"Error querying history for node {node_id}: {e}")
        return None

def get_nodes_by_region(region_id):
    """Get all nodes for a specific region"""
    response = supabase.rpc('get_nodes_by_region', {'region_id_param': region_id}).execute()
    return response.data or []

def get_node_region(node_id):
    """Get the region_id for a specific node"""
    response = supabase.table('node_regions') \
        .select('region_id') \
        .eq('node_id', node_id) \
        .execute()
    return response.data[0]['region_id'] if response.data else None

def get_parent_node_reports(parent_id):
    try:
        response = supabase.table("Parent_Node_Reports") \
            .select("*") \
            .eq("parent_id", parent_id) \
            .order("timestamp", desc=True) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error querying Parent_Node_Reports for parent {parent_id}: {e}")
        return []

def get_region_id(region_name):
    if region_name == "Αρχηγείο / Ε.Σ.Κ.Ε.ΔΙ.Κ.":
        return None  # Headquarters has access to all regions

    region_mapping = {
        "Ανατολικής Μακεδονίας και Θράκης": "FR1",
        "Κεντρικής Μακεδονίας": "FR2",
        "Δυτικής Μακεδονίας": "FR3",
        "Ηπείρου": "FR4",
        "Θεσσαλίας": "FR5",
        "Ιονίων Νήσων": "FR6",
        "Δυτικής Ελλάδας": "FR7",
        "Στερεάς Ελλάδας": "FR8",
        "Αττικής": "FR9",
        "Πελοποννήσου": "FR10",
        "Βορείου Αιγαίου": "FR11",
        "Νοτίου Αιγαίου": "FR12",
        "Κρήτης": "FR13"
    }
    return region_mapping.get(region_name)

def get_nodes_for_dashboard(region_name):
    try:
        if region_name == 'Αρχηγείο / Ε.Σ.Κ.Ε.ΔΙ.Κ.':
            # For headquarters, get all nodes without region filtering
            response = supabase.table("nodes") \
                .select("node_id, title, location, is_parent, lat, lng") \
                .execute()
        else:
            # For regional offices, filter by region
            region_id = get_region_id(region_name)
            if not region_id:
                return None

            # First get all node_ids for this region from node_regions table
            node_regions = supabase.table('node_regions') \
                .select('node_id') \
                .eq('region_id', region_id) \
                .execute()

            node_ids = [nr['node_id'] for nr in node_regions.data] if node_regions.data else []

            if not node_ids:
                return []

            # Then get all node details for these node_ids
            response = supabase.table("nodes") \
                .select("node_id, title, location, is_parent, lat, lng") \
                .in_("node_id", node_ids) \
                .execute()

        return response.data or []
    except Exception as e:
        print(f"Error loading nodes for dashboard: {str(e)}")
        return None