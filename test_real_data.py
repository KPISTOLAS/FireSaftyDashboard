#!/usr/bin/env python3
"""
Test Real Data Script
Tests if the database connection is working and can retrieve real project data
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test if we can connect to the database and get real data"""
    print("🔥 Testing Database Connection for Real Project Data")
    print("=" * 60)
    
    # Check environment variables
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Environment variables not set!")
        print("   Please create a .env file with:")
        print("   SUPABASE_URL=your_supabase_url")
        print("   SUPABASE_KEY=your_supabase_key")
        return False
    
    print(f"✅ Environment variables found:")
    print(f"   URL: {supabase_url}")
    print(f"   Key: {supabase_key[:20]}...{supabase_key[-10:]}")
    
    try:
        # Import and test database manager
        from app.database import db_manager
        
        print("\n🔍 Testing database connection...")
        
        # Try to initialize connection
        supabase = db_manager._initialize_connection()
        
        if not supabase:
            print("❌ Database connection failed!")
            print("   Check the logs above for specific error details.")
            return False
        
        print("✅ Database connection successful!")
        
        # Test getting real data
        print("\n📊 Testing data retrieval...")
        
        # Test 1: Get all nodes
        print("1. Testing: Get all nodes...")
        try:
            response = supabase.table("nodes").select("*").execute()
            node_count = len(response.data) if response.data else 0
            print(f"   ✅ Found {node_count} nodes in database")
            
            if node_count > 0:
                print("   Sample nodes:")
                for i, node in enumerate(response.data[:3]):
                    print(f"      {i+1}. {node.get('title', 'No title')} (ID: {node.get('node_id', 'No ID')})")
            else:
                print("   ⚠️  No nodes found in database!")
                print("   This means your database is empty or tables don't exist.")
                
        except Exception as e:
            print(f"   ❌ Error getting nodes: {e}")
        
        # Test 2: Get sensor readings
        print("\n2. Testing: Get sensor readings...")
        try:
            response = supabase.table("sensor_readings").select("*").limit(5).execute()
            reading_count = len(response.data) if response.data else 0
            print(f"   ✅ Found {reading_count} sensor readings in database")
            
            if reading_count > 0:
                print("   Sample readings:")
                for i, reading in enumerate(response.data[:3]):
                    print(f"      {i+1}. Node {reading.get('node_id', 'No ID')}: Temp={reading.get('temperature', 'N/A')}°C")
            else:
                print("   ⚠️  No sensor readings found in database!")
                
        except Exception as e:
            print(f"   ❌ Error getting sensor readings: {e}")
        
        # Test 3: Get node regions
        print("\n3. Testing: Get node regions...")
        try:
            response = supabase.table("node_regions").select("*").execute()
            region_count = len(response.data) if response.data else 0
            print(f"   ✅ Found {region_count} node-region mappings in database")
            
            if region_count > 0:
                print("   Sample mappings:")
                for i, mapping in enumerate(response.data[:3]):
                    print(f"      {i+1}. Node {mapping.get('node_id', 'No ID')} → Region {mapping.get('region_id', 'No ID')}")
            else:
                print("   ⚠️  No node-region mappings found in database!")
                
        except Exception as e:
            print(f"   ❌ Error getting node regions: {e}")
        
        # Test 4: Test the database manager methods
        print("\n4. Testing: Database manager methods...")
        try:
            # Test getting nodes for a specific region
            region_name = "Ανατολικής Μακεδονίας και Θράκης"
            nodes = db_manager.get_nodes_for_dashboard(region_name)
            
            if nodes and len(nodes) > 0:
                print(f"   ✅ Database manager returned {len(nodes)} nodes for region: {region_name}")
                print("   Sample nodes from manager:")
                for i, node in enumerate(nodes[:3]):
                    print(f"      {i+1}. {node.get('title', 'No title')} (ID: {node.get('node_id', 'No ID')})")
            else:
                print(f"   ⚠️  Database manager returned no nodes for region: {region_name}")
                print("   This might mean:")
                print("   - No nodes are assigned to this region")
                print("   - The region mapping is incorrect")
                print("   - The node_regions table is empty")
                
        except Exception as e:
            print(f"   ❌ Error testing database manager: {e}")
        
        print("\n" + "=" * 60)
        print("📊 DATABASE TEST SUMMARY")
        print("=" * 60)
        
        if node_count > 0 and reading_count > 0:
            print("✅ Database has data and connection is working!")
            print("   Your APIs should now return real project data instead of mock data.")
        elif node_count > 0:
            print("⚠️  Database has nodes but no sensor readings!")
            print("   You need to populate the sensor_readings table with data.")
        else:
            print("❌ Database is empty or tables don't exist!")
            print("   You need to:")
            print("   1. Create the database tables")
            print("   2. Import sample data")
            print("   3. Or populate with your real project data")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database test completed successfully!")
        print("   If you still see mock data in your application,")
        print("   restart the Flask app to pick up the new connection.")
    else:
        print("\n💥 Database test failed!")
        print("   Check the error messages above and fix the issues.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
