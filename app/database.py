"""
Database connection and query management module
"""
import time
import logging
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from flask import current_app

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.connected = False
        # Retry state for connection attempts
        self._failed_connect_attempts: int = 0
        self._last_retry_time: float = 0.0
        self._current_retry_delay: float = 0.0
        # Don't initialize connection during import. Lazily init on first use
    
    def _initialize_connection(self):
        """Initialize Supabase connection with retry logic"""
        if self.connected and self.supabase:
            return self.supabase

        current_time = time.time()
        if current_time - self._last_retry_time < self._current_retry_delay:
            logger.debug(f"Still in backoff period, waiting {self._current_retry_delay - (current_time - self._last_retry_time):.1f}s")
            return None

        supabase_url = current_app.config.get('SUPABASE_URL')
        supabase_key = current_app.config.get('SUPABASE_KEY')
        if not supabase_url or not supabase_key:
            raise RuntimeError("SUPABASE_URL/SUPABASE_KEY not configured. Set them in environment or .env")

        # Be robust against accidental whitespace in env/.env
        supabase_url = supabase_url.strip()
        supabase_key = supabase_key.strip()

        max_retries = current_app.config.get('DB_RETRY_ATTEMPTS', 3)
        initial_retry_delay = current_app.config.get('DB_RETRY_DELAY', 2)
        max_retry_delay = current_app.config.get('DB_MAX_RETRY_DELAY', 60)

        if self._current_retry_delay == 0:
            self._current_retry_delay = initial_retry_delay
        else:
            self._current_retry_delay = min(self._current_retry_delay * 2, max_retry_delay)

        self._last_retry_time = current_time

        logger.info(f"Attempting Supabase connection (attempt {self._failed_connect_attempts + 1}/{max_retries})")
        logger.info(f"URL: {supabase_url}")
        logger.info(f"Key: {supabase_key[:20]}...{supabase_key[-10:] if len(supabase_key) > 30 else ''}")

        try:
            logger.info("Creating Supabase client...")
            self.supabase = create_client(supabase_url, supabase_key)
            logger.info("Supabase client created, testing connection...")
            
            # Test connection with a simple query
            logger.info("Executing test query...")
            response = self.supabase.table("nodes").select("*").limit(1).execute()
            logger.info(f"Test query successful, returned {len(response.data) if response.data else 0} rows")
            
            self.connected = True
            self._current_retry_delay = 0
            self._failed_connect_attempts = 0
            logger.info("✅ Successfully connected to Supabase!")
            return self.supabase

        except Exception as e:
            self._failed_connect_attempts += 1
            error_msg = str(e)
            logger.warning(
                f"Failed to connect to Supabase (attempt {self._failed_connect_attempts}): {error_msg}"
            )
            
            # Provide specific guidance based on error type
            if "getaddrinfo failed" in error_msg:
                logger.error("🔍 DNS Resolution Error - This is a network connectivity issue")
                logger.error("   Possible causes:")
                logger.error("   1. No internet connection")
                logger.error("   2. Corporate firewall/proxy blocking the connection")
                logger.error("   3. DNS server issues")
                logger.error("   4. Windows Firewall blocking outbound connections")
            elif "401" in error_msg or "permission" in error_msg.lower():
                logger.error("🔍 Authentication Error - Check your API key")
            elif "404" in error_msg:
                logger.error("🔍 Table Not Found - Check if database tables exist")
            
            if self._failed_connect_attempts >= max_retries:
                logger.error(f"❌ All {max_retries} connection attempts failed. Application will run with mock data.")
                logger.error("   To fix this:")
                logger.error("   1. Check your internet connection")
                logger.error("   2. Verify SUPABASE_URL and SUPABASE_KEY in .env file")
                logger.error("   3. Try using a mobile hotspot to test")
                logger.error("   4. Check Windows Firewall settings")
            else:
                logger.info(f"Next connection attempt in {self._current_retry_delay} seconds")

            self.connected = False
            return None
    
    def get_node_info(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get node information by ID"""
        try:
            if not self.connected:
                self._initialize_connection()
                if not self.connected:
                    return self._get_mock_node_info(node_id)
            
            response = self.supabase.table("nodes").select("*").eq("node_id", node_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error querying node {node_id}: {e}")
            return self._get_mock_node_info(node_id)
    
    def get_node_history(self, node_id: str) -> List[Dict[str, Any]]:
        """Get historical data for a node"""
        try:
            if not self.connected:
                self._initialize_connection()
                if not self.connected:
                    return self._get_mock_node_history(node_id)
            
            response = self.supabase.table("sensor_readings")\
                .select("*")\
                .eq("node_id", node_id)\
                .order("timestamp", desc=True)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error querying history for node {node_id}: {e}")
            return self._get_mock_node_history(node_id)

    # ---- Normalization helpers for templates and API ----
    def normalize_reading(self, reading: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a single sensor reading to the fields expected by templates/API."""
        if not reading:
            return {}
        normalized = dict(reading)
        # Map known alternate field names
        if 'gas_and_smoke' not in normalized and 'smoke_level' in normalized:
            normalized['gas_and_smoke'] = normalized.get('smoke_level')
        # Provide sane defaults if missing
        normalized.setdefault('danger_level', normalized.get('danger_level', 0))
        normalized.setdefault('temperature', normalized.get('temperature', 0))
        normalized.setdefault('humidity', normalized.get('humidity', 0))
        normalized.setdefault('rain', normalized.get('rain', False))
        normalized.setdefault('wind_speed', normalized.get('wind_speed', 0))
        normalized.setdefault('flora_density', normalized.get('flora_density', 0))
        normalized.setdefault('slope', normalized.get('slope', 0))
        return normalized

    def normalize_readings(self, readings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.normalize_reading(r) for r in readings or []]

    def build_node_view(self, node_info: Dict[str, Any], latest_reading: Dict[str, Any]) -> Dict[str, Any]:
        """Merge node info with normalized latest reading and defaults for UI/API."""
        base = dict(node_info or {})
        reading = self.normalize_reading(latest_reading or {})
        merged = {**base, **reading}
        # Ensure required keys exist for templates
        merged.setdefault('title', base.get('title', base.get('node_id', 'Unknown Node')))
        merged.setdefault('location', base.get('location', ''))
        merged.setdefault('node_id', base.get('node_id'))
        return merged
    
    def get_nodes_by_region(self, region_id: str) -> List[Dict[str, Any]]:
        """Get all nodes for a specific region"""
        try:
            if not self.connected:
                self._initialize_connection()
                if not self.connected:
                    return self._get_mock_nodes()
            
            # Get node IDs for this region
            node_regions = self.supabase.table('node_regions')\
                .select('node_id')\
                .eq('region_id', region_id)\
                .execute()
            
            node_ids = [nr['node_id'] for nr in node_regions.data] if node_regions.data else []
            
            if not node_ids:
                return []
            
            # Get the actual nodes
            response = self.supabase.table("nodes")\
                .select("*")\
                .in_('node_id', node_ids)\
                .execute()
            
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting nodes by region: {e}")
            return self._get_mock_nodes()
    
    def get_node_region(self, node_id: str) -> Optional[str]:
        """Get the region_id for a specific node"""
        try:
            if not self.connected:
                self._initialize_connection()
                if not self.connected:
                    return "FR1"  # Mock region
            
            response = self.supabase.table('node_regions')\
                .select('region_id')\
                .eq('node_id', node_id)\
                .execute()
            return response.data[0]['region_id'] if response.data else None
        except Exception as e:
            logger.error(f"Error getting node region: {e}")
            return "FR1"
    
    def get_parent_node_reports(self, parent_id: str) -> List[Dict[str, Any]]:
        """Get reports for a parent node"""
        try:
            if not self.connected:
                self._initialize_connection()
                if not self.connected:
                    return self._get_mock_parent_reports(parent_id)
            
            response = self.supabase.table("Parent_Node_Reports")\
                .select("*")\
                .eq("parent_id", parent_id)\
                .order("timestamp", desc=True)\
                .execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error querying Parent_Node_Reports for parent {parent_id}: {e}")
            return self._get_mock_parent_reports(parent_id)
    
    def get_nodes_for_dashboard(self, region_name: str) -> List[Dict[str, Any]]:
        """Get nodes for dashboard based on region"""
        try:
            if not self.connected:
                self._initialize_connection()
                if not self.connected:
                    return self._get_mock_nodes()
            
            if region_name == 'Αρχηγείο / Ε.Σ.Κ.Ε.ΔΙ.Κ.':
                # For headquarters, get all nodes without region filtering
                response = self.supabase.table("nodes")\
                    .select("node_id, title, location, is_parent, lat, lng")\
                    .execute()
            else:
                # For regional offices, filter by region
                region_id = self._get_region_id(region_name)
                if not region_id:
                    return []
                
                # First get all node_ids for this region from node_regions table
                node_regions = self.supabase.table('node_regions')\
                    .select('node_id')\
                    .eq('region_id', region_id)\
                    .execute()
                
                node_ids = [nr['node_id'] for nr in node_regions.data] if node_regions.data else []
                
                if not node_ids:
                    return []
                
                # Then get all node details for these node_ids
                response = self.supabase.table("nodes")\
                    .select("node_id, title, location, is_parent, lat, lng")\
                    .in_("node_id", node_ids)\
                    .execute()
            
            return response.data or []
        except Exception as e:
            logger.error(f"Error loading nodes for dashboard: {str(e)}")
            return self._get_mock_nodes()
    
    def _get_region_id(self, region_name: str) -> Optional[str]:
        """Get region ID from region name"""
        if region_name == "Αρχηγείο / Ε.Σ.Κ.Ε.ΔΙ.Κ.":
            return None  # Headquarters has access to all regions
        
        return current_app.config['REGION_MAPPING'].get(region_name)
    
    # Mock data methods
    def _get_mock_nodes(self) -> List[Dict[str, Any]]:
        """Return mock nodes data"""
        return [
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
    
    def _get_mock_node_info(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Return mock node info"""
        for node in self._get_mock_nodes():
            if node["node_id"] == node_id:
                return node
        return None
    
    def _get_mock_node_history(self, node_id: str) -> List[Dict[str, Any]]:
        """Return mock node history"""
        return [
            {
                "node_id": node_id,
                "temperature": 25.5,
                "humidity": 60.2,
                "smoke_level": 0.1,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        ]
    
    def _get_mock_parent_reports(self, parent_id: str) -> List[Dict[str, Any]]:
        """Return mock parent reports"""
        return [
            {
                "parent_id": parent_id,
                "report_type": "Mock Report",
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "active"
            }
        ]

# Global database manager instance
db_manager = DatabaseManager() 