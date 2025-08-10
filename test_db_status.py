#!/usr/bin/env python3
"""
Test Database Connection Status
This script will check why the system is using mock data instead of real data.
"""

from DatabaseScript import supabase_connected, supabase, get_nodes_for_dashboard

def test_connection_status():
    """Test the current connection status"""
    print("🔍 Testing Database Connection Status...")
    print("=" * 50)
    
    print(f"1. supabase_connected variable: {supabase_connected}")
    print(f"2. supabase client exists: {supabase is not None}")
    
    if supabase_connected and supabase:
        print("3. Testing direct database query...")
        try:
            response = supabase.table("nodes").select("*").limit(3).execute()
            print(f"   ✅ Query successful, found {len(response.data)} nodes")
            for node in response.data:
                print(f"      - {node.get('title', 'No title')} (ID: {node.get('node_id', 'No ID')})")
        except Exception as e:
            print(f"   ❌ Query failed: {e}")
    
    print("\n4. Testing get_nodes_for_dashboard function...")
    try:
        nodes = get_nodes_for_dashboard("Ανατολικής Μακεδονίας και Θράκης")
        if nodes:
            print(f"   ✅ Function returned {len(nodes)} nodes")
            for node in nodes[:3]:
                print(f"      - {node.get('title', 'No title')} (ID: {node.get('node_id', 'No ID')})")
        else:
            print("   ❌ Function returned None or empty list")
    except Exception as e:
        print(f"   ❌ Function failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    test_connection_status() 