"""
API blueprint for handling API endpoints
"""
import random
from flask import Blueprint, jsonify, current_app, request, session
from app.main import drone_data
from app.database import db_manager

api = Blueprint('api', __name__)

@api.route('/drone_telemetry')
def drone_telemetry():
    """Get real-time drone telemetry data"""
    try:
        # Simulate real-time updates (replace with actual drone data)
        movement_range = 0.0005
        drone_data["location"]["lat"] += random.uniform(-movement_range, movement_range)
        drone_data["location"]["lon"] += random.uniform(-movement_range, movement_range)
        drone_data["location"]["altitude"] = random.uniform(45, 55)
        drone_data["movement"]["speed"] = random.uniform(4, 6)
        drone_data["battery"]["percentage"] = max(0, drone_data["battery"]["percentage"] - 0.1)
        drone_data["fire_detection"]["detected"] = random.random() > 0.8
        drone_data["fire_detection"]["confidence"] = random.uniform(0.7, 0.95) if drone_data["fire_detection"]["detected"] else 0.0
        drone_data["fire_detection"]["temperature"] = random.uniform(200, 300) if drone_data["fire_detection"]["detected"] else 0.0
        
        return jsonify(drone_data)
    except Exception as e:
        current_app.logger.error(f"Error in drone telemetry: {str(e)}")
        return jsonify({"error": "Failed to get drone telemetry"}), 500

@api.route('/nodes')
def api_nodes():
    """Return nodes for a region as JSON. Region comes from querystring or session."""
    try:
        region_name = request.args.get('region') or session.get('region')
        current_app.logger.info(f"API /nodes called with region: {region_name}")
        
        if not region_name:
            current_app.logger.warning("API /nodes: No region specified")
            return jsonify({"error": "region not specified"}), 400

        current_app.logger.info(f"API /nodes: Fetching nodes for region: {region_name}")
        nodes = db_manager.get_nodes_for_dashboard(region_name)
        current_app.logger.info(f"API /nodes: Retrieved {len(nodes) if nodes else 0} nodes")
        current_app.logger.info(f"API /nodes: Database connected: {db_manager.connected}")
        
        if not nodes:
            current_app.logger.warning(f"API /nodes: No nodes found for region: {region_name}")
            return jsonify({"error": "No nodes found for this region", "region": region_name, "db_connected": db_manager.connected}), 404
            
        return jsonify({
            "nodes": nodes,
            "region": region_name,
            "db_connected": db_manager.connected,
            "count": len(nodes)
        })
    except Exception as e:
        current_app.logger.error(f"/api/nodes failed: {e}")
        return jsonify({"error": "Failed to fetch nodes", "details": str(e)}), 500

@api.route('/node/<node_id>')
def api_node(node_id: str):
    """Return a single node's merged info as JSON."""
    try:
        current_app.logger.info(f"API /node/{node_id}: Fetching node info")
        
        # Accept both raw IDs (e.g. N1_1) and dotted format (e.g. 1.1)
        supabase_node_id = node_id if node_id.startswith('N') else f"N{node_id.replace('.', '_')}"
        current_app.logger.info(f"API /node/{node_id}: Converted to Supabase ID: {supabase_node_id}")
        
        node_info = db_manager.get_node_info(supabase_node_id)
        if not node_info:
            current_app.logger.warning(f"API /node/{node_id}: Node not found")
            return jsonify({"error": "Node not found", "node_id": node_id, "supabase_id": supabase_node_id}), 404

        history_data = db_manager.get_node_history(supabase_node_id)
        latest_data = history_data[0] if history_data else {}
        merged = {**node_info, **latest_data}
        
        current_app.logger.info(f"API /node/{node_id}: Successfully retrieved node with {len(latest_data) if latest_data else 0} history records")
        
        return jsonify({
            "node": merged,
            "db_connected": db_manager.connected,
            "has_history": bool(history_data)
        })
    except Exception as e:
        current_app.logger.error(f"/api/node/{node_id} failed: {e}")
        return jsonify({"error": "Failed to fetch node", "details": str(e)}), 500

@api.route('/history/<node_id>')
def api_history(node_id: str):
    """Return chronological readings for a node as JSON."""
    try:
        current_app.logger.info(f"API /history/{node_id}: Fetching history")
        
        supabase_node_id = node_id if node_id.startswith('N') else f"N{node_id.replace('.', '_')}"
        current_app.logger.info(f"API /history/{node_id}: Converted to Supabase ID: {supabase_node_id}")
        
        history_data = db_manager.get_node_history(supabase_node_id)
        current_app.logger.info(f"API /history/{node_id}: Retrieved {len(history_data) if history_data else 0} history records")
        
        return jsonify({
            "history": history_data or [],
            "node_id": node_id,
            "supabase_id": supabase_node_id,
            "db_connected": db_manager.connected,
            "count": len(history_data) if history_data else 0
        })
    except Exception as e:
        current_app.logger.error(f"/api/history/{node_id} failed: {e}")
        return jsonify({"error": "Failed to fetch history", "details": str(e)}), 500

@api.route('/parent/<node_id>/reports')
def api_parent_reports(node_id: str):
    """Return reports for a parent node as JSON."""
    try:
        current_app.logger.info(f"API /parent/{node_id}/reports: Fetching reports")
        
        supabase_node_id = node_id if node_id.startswith('N') else f"N{node_id.replace('.', '_')}"
        current_app.logger.info(f"API /parent/{node_id}/reports: Converted to Supabase ID: {supabase_node_id}")
        
        reports = db_manager.get_parent_node_reports(supabase_node_id)
        current_app.logger.info(f"API /parent/{node_id}/reports: Retrieved {len(reports) if reports else 0} reports")
        
        return jsonify({
            "reports": reports or [],
            "parent_id": node_id,
            "supabase_id": supabase_node_id,
            "db_connected": db_manager.connected,
            "count": len(reports) if reports else 0
        })
    except Exception as e:
        current_app.logger.error(f"/api/parent/{node_id}/reports failed: {e}")
        return jsonify({"error": "Failed to fetch reports", "details": str(e)}), 500

@api.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        from app.database import db_manager
        return jsonify({
            "status": "healthy",
            "database_connected": db_manager.connected,
            "database_status": "connected" if db_manager.connected else "disconnected",
            "version": "1.2.0",
            "endpoints": [
                "/api/nodes",
                "/api/node/<node_id>",
                "/api/history/<node_id>",
                "/api/parent/<node_id>/reports",
                "/api/health"
            ]
        })
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500 