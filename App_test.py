import random
from flask import Flask, render_template, jsonify, abort, redirect, url_for, request, session, flash
from flask_caching import Cache
from DatabaseScript import (get_node_info, get_node_history, get_node_region,
                            get_parent_node_reports, get_nodes_for_dashboard, get_region_id, get_nodes_by_region)

app = Flask(__name__)

# Set a fixed secret key for development (use environment variable in production)
app.config['SECRET_KEY'] = '123123123'


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


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/set_region', methods=['POST'])
def set_region():
    try:
        region = request.form.get('region')
        if not region:
            flash('Παρακαλώ επιλέξτε μια Περιφερειακή Πυροσβεστική Διοίκηση')
            return redirect(url_for('login'))

        # Store the selected region in the session
        session['region'] = region
        return redirect(url_for('dashboard'))
    except Exception as e:
        app.logger.error(f"Error in set_region: {str(e)}")
        flash('Προέκυψε σφάλμα κατά την επιλογή περιοχής. Παρακαλώ δοκιμάστε ξανά.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'region' not in session:
        return redirect(url_for('login'))

    try:
        nodes = get_nodes_for_dashboard(session['region'])
        if nodes is None:
            abort(500)

        print("Nodes data from database:", nodes)
        return render_template('index.html', region=session['region'], nodes=nodes)
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {str(e)}")
        abort(500)


@app.route('/node/<node_id>')
def node(node_id):
    if 'region' not in session:
        return redirect(url_for('login'))

    try:
        supabase_node_id = f"N{node_id.replace('.', '_')}"
        node_info = get_node_info(supabase_node_id)

        # Ensure the node exists
        if not node_info:
            abort(404, description=f"Node {node_id} not found")

        # Secure region validation
        current_region_id = get_region_id(session['region'])
        node_region = get_node_region(supabase_node_id)

        # Allow access if:
        # 1. User is from headquarters (current_region_id is None)
        # OR
        # 2. Node's region matches user's region
        if current_region_id is not None and node_region != current_region_id:
            abort(404, description=f"Node {node_id} not found in this region")

        # Merge with latest readings
        history_data = get_node_history(supabase_node_id)
        latest_data = history_data[0] if history_data else {}
        node_info.update(latest_data)

        return render_template('node.html', node=node_info)
    except Exception as e:
        app.logger.error(f"Error in /node/{node_id}: {str(e)}")
        abort(500)


@app.route('/nodes')
def nodes_info():
    if 'region' not in session:
        return redirect(url_for('login'))

    region_id = get_region_id(session['region'])
    if not region_id:
        abort(404, description="Region not found")

    try:
        nodes = get_nodes_by_region(region_id)
        return render_template('nodes.html', nodes=nodes)
    except Exception as e:
        app.logger.error(f"Error rendering nodes: {str(e)}")
        abort(500)


@app.route('/parent/<node_id>')
def parent_node(node_id):
    if 'region' not in session:
        return redirect(url_for('login'))

    try:
        supabase_node_id = f"N{node_id.replace('.', '_')}"
        node_info = get_node_info(supabase_node_id)

        if not node_info:
            abort(404, description=f"Parent node {node_id} not found")

        # Get report data
        reports = get_parent_node_reports(supabase_node_id)

        return render_template('parent_node.html',
                               parent=node_info,
                               reports=reports,
                               region=session['region'])
    except Exception as e:
        app.logger.error(f"Error in /parent/{node_id}: {str(e)}")
        abort(500)


@app.route('/history/<node_id>')
def history(node_id):
    try:
        node_info = get_node_info(node_id)

        # Fallback: if no metadata, use latest sensor reading
        if not node_info:
            history_data = get_node_history(node_id)
            if history_data:
                node_info = {"node_id": node_id, **history_data[0]}
            else:
                abort(404, description=f"Node {node_id} not found")

        else:
            history_data = get_node_history(node_id)

        return render_template('history.html',
                               node=node_info,
                               readings=history_data or [],
                               message=None if history_data else "No historical data available")
    except Exception as e:
        app.logger.error(f"Error in /history/{node_id}: {str(e)}")
        abort(500)


@app.route('/drone')
def drone_info():
    return render_template('drone.html')


@app.route('/api/drone_telemetry')
def drone_telemetry():
    # Simulate real-time updates (replace with actual drone data)
    movement_range = 0.0005
    drone_data["location"]["lat"] += random.uniform(-movement_range, movement_range)
    drone_data["location"]["lon"] += random.uniform(-movement_range, movement_range)
    drone_data["location"]["altitude"] = random.uniform(45, 55)
    drone_data["movement"]["speed"] = random.uniform(4, 6)
    drone_data["battery"]["percentage"] = max(0, drone_data["battery"]["percentage"] - 0.1)
    drone_data["fire_detection"]["detected"] = random.random() > 0.8
    drone_data["fire_detection"]["confidence"] = random.uniform(0.7, 0.95) if drone_data["fire_detection"][
        "detected"] else 0.0
    drone_data["fire_detection"]["temperature"] = random.uniform(200, 300) if drone_data["fire_detection"][
        "detected"] else 0.0
    return jsonify(drone_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)