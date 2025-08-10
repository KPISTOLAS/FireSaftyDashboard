#!/usr/bin/env python3
"""
Database Connection Diagnostic Tool
This script will help identify why you're getting mock data instead of real sensor data.
"""

import os
import socket
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
import time

load_dotenv()  # Load environment variables

SUPABASE_URL = (os.environ.get("SUPABASE_URL") or "").strip()
SUPABASE_KEY = (os.environ.get("SUPABASE_KEY") or "").strip()

def test_network_connectivity():
    """Test basic network connectivity"""
    print("🌐 Testing Network Connectivity...")
    print("=" * 50)
    
    # Test DNS resolution
    try:
        hostname = "gejknamvrhhhwkgrhsor.supabase.co"
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution: {hostname} → {ip}")
    except socket.gaierror as e:
        print(f"❌ DNS Resolution Failed: {e}")
        return False
    
    # Test HTTP connectivity
    try:
        response = requests.get(f"https://{hostname}", timeout=10)
        print(f"✅ HTTP Connectivity: Status {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Connectivity Failed: {e}")
        return False

def test_connection():
    print("🔥 Fire Detection Dashboard - Database Diagnostic Tool")
    print("=" * 60)
    
    # First test network connectivity
    if not test_network_connectivity():
        print("\n❌ Network connectivity issues detected!")
        print("Possible solutions:")
        print("1. Check your internet connection")
        print("2. Check if you're behind a corporate firewall/proxy")
        print("3. Try using a different network (mobile hotspot)")
        print("4. Check Windows Firewall settings")
        return False
    
    print("\n🔍 Testing Supabase Connection...")
    print("=" * 50)
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY environment variables are not set.")
        print("   Please ensure you have a .env file or set them in your environment.")
        return False

    print(f"📋 Configuration:")
    print(f"   URL: {SUPABASE_URL}")
    print(f"   Key: {SUPABASE_KEY[:20]}...{SUPABASE_KEY[-10:]}")

    try:
        print("\n1. Creating Supabase client...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("   ✅ Client created successfully")

        print("\n2. Testing basic connection...")
        # Test with a simple query
        response = supabase.table("nodes").select("*").limit(1).execute()
        print("   ✅ Connection successful!")
        print(f"   📊 Test query returned {len(response.data)} rows")

        print("\n3. Testing table access...")
        tables_to_check = ["nodes", "sensor_readings", "node_regions"]
        for table in tables_to_check:
            try:
                response = supabase.table(table).select("*").limit(1).execute()
                print(f"   ✅ Table '{table}': accessible ({len(response.data)} rows)")
            except Exception as e:
                print(f"   ❌ Table '{table}': {e}")

        print("\n4. Testing data retrieval...")
        try:
            nodes = supabase.table("nodes").select("*").limit(5).execute()
            if nodes.data:
                print(f"   ✅ Found {len(nodes.data)} nodes")
                for node in nodes.data[:3]:
                    print(f"      - {node.get('node_id', 'N/A')}: {node.get('title', 'N/A')}")
            else:
                print("   ⚠️  No nodes found in database")
        except Exception as e:
            print(f"   ❌ Error retrieving nodes: {e}")

        print("\n✅ All tests passed! Database connection is working.")
        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        
        if "getaddrinfo failed" in str(e):
            print("\n🔍 This appears to be a DNS resolution issue.")
            print("Possible solutions:")
            print("1. Check your internet connection")
            print("2. Try using a different DNS server (8.8.8.8 or 1.1.1.1)")
            print("3. Check if you're behind a corporate firewall/proxy")
            print("4. Try using a mobile hotspot to test")
        elif "401" in str(e) or "permission" in str(e).lower():
            print("\n🔍 This appears to be an authentication issue.")
            print("Possible solutions:")
            print("1. Verify your SUPABASE_KEY is correct")
            print("2. Check if your Supabase project is active")
            print("3. Ensure RLS policies allow 'anon' role to read tables")
        elif "404" in str(e):
            print("\n🔍 This appears to be a table not found issue.")
            print("Possible solutions:")
            print("1. Check if your database tables exist")
            print("2. Verify table names match: nodes, sensor_readings, node_regions")
            print("3. Run the database setup scripts")
        
        return False

    print("\n" + "=" * 50)
    print("Diagnostic complete! Check the results above.")

if __name__ == "__main__":
    test_connection() 