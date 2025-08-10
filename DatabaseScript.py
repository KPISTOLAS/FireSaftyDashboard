from supabase import create_client, Client
import time

# Replace with your Supabase details
SUPABASE_URL = "https://gejknamvrhhhwkgrhsor.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdlamtuYW12cmhoaHdrZ3Joc29yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQxNDkyMDgsImV4cCI6MjA2OTcyNTIwOH0.nkPB0B7pGREgFdCSIA7J0WpbNhKCH96sYa9s9QyZ508"

# Global variable to track connection status
supabase_connected = False
supabase: Client = None

def initialize_supabase():
    """Initialize Supabase connection with retry logic"""
    global supabase, supabase_connected
    
    if supabase_connected and supabase:
        return supabase
    
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            # Test connection with timeout
            supabase.table("nodes").select("*").limit(1).execute()
            supabase_connected = True
            print("Successfully connected to Supabase")
            return supabase
        except Exception as e:
            print(f"Failed to connect to Supabase (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    print("All connection attempts failed. Application will run with mock data")
    supabase_connected = False
    return None

# Initialize connection
initialize_supabase()

# Mock data for when database is not available
MOCK_NODES = [
    {
        "node_id": "N1_1",
        "title": "Mock Sensor Node 1",
        "location": "Test Location 1",
        "is_parent": False,
        "lat": 40.95,
        "lng": 24.5
    },
    {
        "node_id": "N2_1", 
        "title": "Mock Parent Node 1",
        "location": "Test Location 2",
        "is_parent": True,
        "lat": 40.96,
        "lng": 24.51
    }
]

MOCK_SENSOR_READINGS = [
    {
        "node_id": "N1_1",
        "temperature": 25.5,
        "humidity": 60.2,
        "smoke_level": 0.1,
        "timestamp": "2024-01-15T10:30:00Z"
    }
]

# Function to get node information
def get_node_info(node_id):
    try:
        if not supabase_connected:
            # Return mock data
            for node in MOCK_NODES:
                if node["node_id"] == node_id:
                    return node
            return None
            
        response = supabase.table("nodes").select("*").eq("node_id", node_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error querying node {node_id}: {e}")
        # Fallback to mock data
        for node in MOCK_NODES:
            if node["node_id"] == node_id:
                return node
        return None

def get_node_history(node_id):
    try:
        if not supabase_connected:
            # Return mock data
            return [reading for reading in MOCK_SENSOR_READINGS if reading["node_id"] == node_id]
            
        response = supabase.table("sensor_readings")\
            .select("*")\
            .eq("node_id", node_id)\
            .order("timestamp", desc=True)\
            .execute()
        return response.data
    except Exception as e:
        print(f"Error querying history for node {node_id}: {e}")
        # Fallback to mock data
        return [reading for reading in MOCK_SENSOR_READINGS if reading["node_id"] == node_id]

def get_nodes_by_region(region_id):
    """Get all nodes for a specific region"""
    try:
        if not supabase_connected:
            # Return mock data for all regions
            return MOCK_NODES
            
        # Get node IDs for this region
        node_regions = supabase.table('node_regions') \
            .select('node_id') \
            .eq('region_id', region_id) \
            .execute()
        
        node_ids = [nr['node_id'] for nr in node_regions.data] if node_regions.data else []
        
        if not node_ids:
            return []
        
        # Get the actual nodes
        response = supabase.table("nodes") \
            .select("*") \
            .in_('node_id', node_ids) \
            .execute()
        
        return response.data or []
    except Exception as e:
        print(f"Error getting nodes by region: {e}")
        return MOCK_NODES

def get_node_region(node_id):
    """Get the region_id for a specific node"""
    try:
        if not supabase_connected:
            # Return mock region
            return "FR1"
            
        response = supabase.table('node_regions') \
            .select('region_id') \
            .eq('node_id', node_id) \
            .execute()
        return response.data[0]['region_id'] if response.data else None
    except Exception as e:
        print(f"Error getting node region: {e}")
        return "FR1"

def get_parent_node_reports(parent_id):
    try:
        if not supabase_connected:
            # Return mock reports
            return [
                {
                    "parent_id": parent_id,
                    "report_type": "Mock Report",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "status": "active"
                }
            ]
            
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
        if not supabase_connected:
            # Return mock data for all regions
            return MOCK_NODES
            
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
        return MOCK_NODES