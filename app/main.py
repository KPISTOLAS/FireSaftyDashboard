"""
Main blueprint for web routes and pages
"""
import random
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, abort, current_app
from app.database import db_manager

main = Blueprint('main', __name__)

# Drone telemetry data (simulated or real)
drone_data = {
    "drone_id": "DRONE_001",
    "location": {
        "lat": 40.95,
        "lon": 24.5,
        "altitude": 50.2
    },
    "movement": {
        "speed": 5.3,
        "heading": 120.5
    },
    "battery": {
        "voltage": 11.1,
        "percentage": 78
    },
    "fire_detection": {
        "detected": False,
        "confidence": 0.0,
    }
}

@main.route('/')
def index():
    """Redirect to login page"""
    return redirect(url_for('main.login'))

@main.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@main.route('/set_region', methods=['POST'])
def set_region():
    """Set user region and redirect to dashboard"""
    try:
        region = request.form.get('region')
        if not region:
            flash('Παρακαλώ επιλέξτε μια Περιφερειακή Πυροσβεστική Διοίκηση')
            return redirect(url_for('main.login'))

        # Store the selected region in the session
        session['region'] = region
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        current_app.logger.error(f"Error in set_region: {str(e)}")
        flash('Προέκυψε σφάλμα κατά την επιλογή περιοχής. Παρακαλώ δοκιμάστε ξανά.')
        return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    if 'region' not in session:
        return redirect(url_for('main.login'))

    try:
        nodes = db_manager.get_nodes_for_dashboard(session['region'])
        if nodes is None:
            abort(500)

        current_app.logger.info(f"Nodes data from database: {nodes}")
        return render_template('index.html', 
                             region=session['region'], 
                             nodes=nodes, 
                             db_connected=db_manager.connected)
    except Exception as e:
        current_app.logger.error(f"Error loading dashboard: {str(e)}")
        abort(500)

@main.route('/node/<node_id>')
def node(node_id):
    """Individual node details page"""
    if 'region' not in session:
        return redirect(url_for('main.login'))

    try:
        supabase_node_id = f"N{node_id.replace('.', '_')}"
        node_info = db_manager.get_node_info(supabase_node_id)

        # Ensure the node exists
        if not node_info:
            abort(404, description=f"Node {node_id} not found")

        # Secure region validation
        current_region_id = db_manager._get_region_id(session['region'])
        node_region = db_manager.get_node_region(supabase_node_id)

        # Allow access if:
        # 1. User is from headquarters (current_region_id is None)
        # OR
        # 2. Node's region matches user's region
        if current_region_id is not None and node_region != current_region_id:
            abort(404, description=f"Node {node_id} not found in this region")

        # Merge with normalized latest readings
        history_data = db_manager.get_node_history(supabase_node_id)
        latest_data = db_manager.normalize_reading(history_data[0]) if history_data else {}
        merged = db_manager.build_node_view(node_info, latest_data)

        return render_template('node.html', node=merged)
    except Exception as e:
        current_app.logger.error(f"Error in /node/{node_id}: {str(e)}")
        abort(500)

@main.route('/nodes')
def nodes_info():
    """Nodes listing page"""
    if 'region' not in session:
        return redirect(url_for('main.login'))

    region_id = db_manager._get_region_id(session['region'])
    
    try:
        if region_id is None:
            # Headquarters case - get all nodes
            if not db_manager.connected:
                nodes = db_manager._get_mock_nodes()
            else:
                response = db_manager.supabase.table("nodes").select("*").execute()
                nodes = response.data or []
        else:
            # Regional case - get nodes by region
            nodes = db_manager.get_nodes_by_region(region_id)
        
        return render_template('nodes.html', nodes=nodes)
    except Exception as e:
        current_app.logger.error(f"Error rendering nodes: {str(e)}")
        abort(500)

@main.route('/parent/<node_id>')
def parent_node(node_id):
    """Parent node reports page"""
    if 'region' not in session:
        return redirect(url_for('main.login'))

    try:
        supabase_node_id = f"N{node_id.replace('.', '_')}"
        node_info = db_manager.get_node_info(supabase_node_id)

        if not node_info:
            abort(404, description=f"Parent node {node_id} not found")

        # Get report data
        reports = db_manager.get_parent_node_reports(supabase_node_id)

        return render_template('parent_node.html',
                             parent=node_info,
                             reports=reports,
                             region=session['region'])
    except Exception as e:
        current_app.logger.error(f"Error in /parent/{node_id}: {str(e)}")
        abort(500)

@main.route('/history/<node_id>')
def history(node_id):
    """Node history page"""
    try:
        node_info = db_manager.get_node_info(node_id)

        # Fallback: if no metadata, use latest sensor reading
        if not node_info:
            history_data = db_manager.get_node_history(node_id)
            if history_data:
                node_info = {"node_id": node_id, **history_data[0]}
            else:
                abort(404, description=f"Node {node_id} not found")
        else:
            history_data = db_manager.get_node_history(node_id)

        return render_template('history.html',
                             node=node_info,
                             readings=db_manager.normalize_readings(history_data) or [],
                             message=None if history_data else "No historical data available")
    except Exception as e:
        current_app.logger.error(f"Error in /history/{node_id}: {str(e)}")
        abort(500)

@main.route('/drone')
def drone_info():
    """Drone surveillance page"""
    return render_template('drone.html', db_connected=db_manager.connected) 