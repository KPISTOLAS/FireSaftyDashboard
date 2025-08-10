#!/usr/bin/env python3
"""
Import Sample Data Script
This script will import the sample sensor data into your Supabase database.
"""

from supabase import create_client
import time

# Supabase configuration
SUPABASE_URL = "https://gejknamvrhhhwkgrhsor.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdlamtuYW12cmhoaHdrZ3Joc29yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQxNDkyMDgsImV4cCI6MjA2OTcyNTIwOH0.nkPB0B7pGREgFdCSIA7J0WpbNhKCH96sYa9s9QyZ508"

def import_sample_data():
    """Import sample sensor data into Supabase"""
    print("🔥 Importing Sample Sensor Data...")
    print("=" * 50)
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Sample nodes data
        nodes_data = [
            {'node_id': 'N1', 'title': 'Node 1', 'location': 'Αμυγδαλεώνας, Κεντρικο', 'description': None, 'is_parent': True, 'lat': 40.97, 'lng': 24.37},
            {'node_id': 'N1_1', 'title': 'Node 1.1', 'location': 'Αμυγδαλεώνας, Δυτικά', 'description': None, 'is_parent': False, 'lat': 40.959556, 'lng': 24.353472},
            {'node_id': 'N1_2', 'title': 'Node 1.2', 'location': 'Αμυγδαλεώνας, Κεντρικά', 'description': None, 'is_parent': False, 'lat': 40.983277, 'lng': 24.380628},
            {'node_id': 'N1_3', 'title': 'Node 1.3', 'location': 'Αμυγδαλεώνας, Ανατολικά', 'description': None, 'is_parent': False, 'lat': 40.963, 'lng': 24.362999},
            {'node_id': 'N2', 'title': 'Node 2', 'location': 'Χρυσούπολη, Κεντρικό', 'description': None, 'is_parent': True, 'lat': 40.995, 'lng': 24.7},
            {'node_id': 'N2_1', 'title': 'Node 2.1', 'location': 'Χρυσούπολη, Ανατολικά', 'description': None, 'is_parent': False, 'lat': 40.978577, 'lng': 24.686108},
            {'node_id': 'N2_2', 'title': 'Node 2.2', 'location': 'Χρυσούπολη, Βόρεια', 'description': None, 'is_parent': False, 'lat': 41.01721, 'lng': 24.711714}
        ]
        
        # Fire regions data
        fire_regions_data = [
            {'region_id': 'FR1', 'name': 'ΠΕΚΕ Ανατολικής Μακεδονίας και Θράκης'},
            {'region_id': 'FR2', 'name': 'ΠΕΚΕ Κεντρικής Μακεδονίας'},
            {'region_id': 'FR3', 'name': 'ΠΕΚΕ Δυτικής Μακεδονίας'},
            {'region_id': 'FR4', 'name': 'ΠΕΚΕ Ηπείρου'},
            {'region_id': 'FR5', 'name': 'ΠΕΚΕ Θεσσαλίας'},
            {'region_id': 'FR6', 'name': 'ΠΕΚΕ Ιονίων Νήσων'},
            {'region_id': 'FR7', 'name': 'ΠΕΚΕ Δυτικής Ελλάδας'},
            {'region_id': 'FR8', 'name': 'ΠΕΚΕ Στερεάς Ελλάδας'},
            {'region_id': 'FR9', 'name': 'ΠΕΚΕ Πελοποννήσου'},
            {'region_id': 'FR10', 'name': 'ΠΕΚΕ Αττικής'},
            {'region_id': 'FR11', 'name': 'ΠΕΚΕ Βορείου Αιγαίου'},
            {'region_id': 'FR12', 'name': 'ΠΕΚΕ Νοτίου Αιγαίου'},
            {'region_id': 'FR13', 'name': 'ΠΕΚΕ Κρήτης'}
        ]
        
        # Node hierarchy data
        node_hierarchy_data = [
            {'parent_id': 'N1', 'child_id': 'N1_1'},
            {'parent_id': 'N1', 'child_id': 'N1_2'},
            {'parent_id': 'N1', 'child_id': 'N1_3'},
            {'parent_id': 'N2', 'child_id': 'N2_1'},
            {'parent_id': 'N2', 'child_id': 'N2_2'}
        ]
        
        # Sensor readings data
        sensor_readings_data = [
            {'reading_id': 11, 'node_id': 'N1_1', 'timestamp': '2025-05-15 08:57:49.815107', 'danger_level': 2, 'temperature': 25.50, 'humidity': 45.30, 'gas_and_smoke': 12.45, 'rain': False, 'wind_speed': 5.20, 'flora_density': 75.30, 'slope': 10.50, 'vegetation_type': 'Deciduous'},
            {'reading_id': 12, 'node_id': 'N1_1', 'timestamp': '2025-05-15 08:57:49.815107', 'danger_level': 3, 'temperature': 28.75, 'humidity': 40.20, 'gas_and_smoke': 15.80, 'rain': False, 'wind_speed': 6.50, 'flora_density': 74.80, 'slope': 10.60, 'vegetation_type': 'Deciduous'},
            {'reading_id': 13, 'node_id': 'N2_1', 'timestamp': '2025-05-15 08:57:49.815107', 'danger_level': 1, 'temperature': 22.30, 'humidity': 50.10, 'gas_and_smoke': 8.90, 'rain': True, 'wind_speed': 8.20, 'flora_density': 60.50, 'slope': 15.30, 'vegetation_type': 'Coniferous'},
            {'reading_id': 14, 'node_id': 'N2_2', 'timestamp': '2025-05-15 08:57:49.815107', 'danger_level': 4, 'temperature': 30.10, 'humidity': 35.60, 'gas_and_smoke': 25.30, 'rain': False, 'wind_speed': 12.40, 'flora_density': 45.20, 'slope': 5.80, 'vegetation_type': 'Mixed'},
            {'reading_id': 15, 'node_id': 'N1_3', 'timestamp': '2025-05-15 09:16:59.531068', 'danger_level': 1, 'temperature': 22.50, 'humidity': 60.00, 'gas_and_smoke': 10.20, 'rain': False, 'wind_speed': 5.50, 'flora_density': 65.00, 'slope': 12.00, 'vegetation_type': None},
            {'reading_id': 16, 'node_id': 'N1_3', 'timestamp': '2025-05-15 09:16:59.531068', 'danger_level': 2, 'temperature': 24.10, 'humidity': 58.50, 'gas_and_smoke': 15.70, 'rain': True, 'wind_speed': 8.20, 'flora_density': 63.50, 'slope': 12.00, 'vegetation_type': None},
            {'reading_id': 17, 'node_id': 'N1_3', 'timestamp': '2025-05-15 09:16:59.531068', 'danger_level': 1, 'temperature': 21.80, 'humidity': 62.30, 'gas_and_smoke': 8.90, 'rain': False, 'wind_speed': 4.80, 'flora_density': 66.20, 'slope': 12.00, 'vegetation_type': None}
        ]
        
        # Parent node reports data
        parent_reports_data = [
            {'report_id': 1, 'parent_id': 'N1', 'child_id': 'N1_1', 'timestamp': '2025-05-15 15:57:11.958786', 'data_received': True, 'data_valid': True, 'status_message': 'All OK'},
            {'report_id': 2, 'parent_id': 'N1', 'child_id': 'N1_2', 'timestamp': '2025-05-15 15:57:11.958786', 'data_received': True, 'data_valid': False, 'status_message': 'Invalid reading'},
            {'report_id': 3, 'parent_id': 'N1', 'child_id': 'N1_3', 'timestamp': '2025-05-15 15:57:11.958786', 'data_received': False, 'data_valid': None, 'status_message': 'No data received'},
            {'report_id': 4, 'parent_id': 'N2', 'child_id': 'N2_1', 'timestamp': '2025-05-15 15:59:19.862867', 'data_received': True, 'data_valid': True, 'status_message': 'Data received and validated successfully.'},
            {'report_id': 5, 'parent_id': 'N2', 'child_id': 'N2_2', 'timestamp': '2025-05-15 15:59:19.862867', 'data_received': True, 'data_valid': False, 'status_message': 'Gas and smoke level too high.'}
        ]
        
        # Node regions data
        node_regions_data = [
            {'node_id': 'N1', 'region_id': 'FR1'},
            {'node_id': 'N1_1', 'region_id': 'FR1'},
            {'node_id': 'N1_2', 'region_id': 'FR1'},
            {'node_id': 'N1_3', 'region_id': 'FR1'},
            {'node_id': 'N2', 'region_id': 'FR1'},
            {'node_id': 'N2_1', 'region_id': 'FR1'},
            {'node_id': 'N2_2', 'region_id': 'FR1'}
        ]
        
        print("1. Importing nodes...")
        for node in nodes_data:
            try:
                supabase.table("nodes").upsert(node).execute()
                print(f"   ✅ Added node: {node['title']}")
            except Exception as e:
                print(f"   ❌ Error adding node {node['title']}: {e}")
        
        print("\n2. Importing fire regions...")
        for region in fire_regions_data:
            try:
                supabase.table("fire_regions").upsert(region).execute()
                print(f"   ✅ Added region: {region['name']}")
            except Exception as e:
                print(f"   ❌ Error adding region {region['name']}: {e}")
        
        print("\n3. Importing node hierarchy...")
        for hierarchy in node_hierarchy_data:
            try:
                supabase.table("node_hierarchy").upsert(hierarchy).execute()
                print(f"   ✅ Added hierarchy: {hierarchy['parent_id']} -> {hierarchy['child_id']}")
            except Exception as e:
                print(f"   ❌ Error adding hierarchy: {e}")
        
        print("\n4. Importing sensor readings...")
        for reading in sensor_readings_data:
            try:
                supabase.table("sensor_readings").upsert(reading).execute()
                print(f"   ✅ Added reading for node: {reading['node_id']}")
            except Exception as e:
                print(f"   ❌ Error adding reading: {e}")
        
        print("\n5. Importing parent node reports...")
        for report in parent_reports_data:
            try:
                supabase.table("Parent_Node_Reports").upsert(report).execute()
                print(f"   ✅ Added report: {report['parent_id']} -> {report['child_id']}")
            except Exception as e:
                print(f"   ❌ Error adding report: {e}")
        
        print("\n6. Importing node regions...")
        for region in node_regions_data:
            try:
                supabase.table("node_regions").upsert(region).execute()
                print(f"   ✅ Added node region: {region['node_id']} -> {region['region_id']}")
            except Exception as e:
                print(f"   ❌ Error adding node region: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Sample data imported successfully!")
        print("   You should now see real sensor data instead of mock data.")
        print("   Restart your Flask application to see the changes.")
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        print("\nPossible solutions:")
        print("1. Check your internet connection")
        print("2. Verify Supabase credentials")
        print("3. Ensure database tables exist")
        print("4. Check table permissions in Supabase")

if __name__ == "__main__":
    print("🔥 Fire Detection Dashboard - Data Import Tool")
    print("=" * 60)
    
    response = input("This will import sample sensor data. Continue? (y/n): ")
    if response.lower() == 'y':
        import_sample_data()
    else:
        print("Import cancelled.")
    
    print("\n" + "=" * 60)
    print("Import process complete!") 