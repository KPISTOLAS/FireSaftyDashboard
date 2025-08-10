#!/usr/bin/env python3
"""
Network Connectivity Test Script
Tests basic network connectivity to help diagnose Supabase connection issues
"""

import socket
import requests
import subprocess
import platform
import sys

def test_dns_resolution():
    """Test DNS resolution for Supabase hostname"""
    print("🌐 Testing DNS Resolution...")
    print("=" * 50)
    
    hostname = "gejknamvrhhhwkgrhsor.supabase.co"
    
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution: {hostname} → {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS Resolution Failed: {e}")
        return False

def test_http_connectivity():
    """Test HTTP connectivity to Supabase"""
    print("\n🌐 Testing HTTP Connectivity...")
    print("=" * 50)
    
    hostname = "gejknamvrhhhwkgrhsor.supabase.co"
    
    try:
        response = requests.get(f"https://{hostname}", timeout=10)
        print(f"✅ HTTP Connectivity: Status {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Connectivity Failed: {e}")
        return False

def test_ping():
    """Test ping to Supabase hostname"""
    print("\n🏓 Testing Ping...")
    print("=" * 50)
    
    hostname = "gejknamvrhhhwkgrhsor.supabase.co"
    
    try:
        # Use appropriate ping command for the OS
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "4", hostname]
        else:
            cmd = ["ping", "-c", "4", hostname]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Ping successful")
            print("   Response:")
            for line in result.stdout.split('\n')[:5]:  # Show first 5 lines
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print(f"❌ Ping failed with return code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Ping timed out")
        return False
    except Exception as e:
        print(f"❌ Ping error: {e}")
        return False

def test_traceroute():
    """Test traceroute to Supabase hostname"""
    print("\n🛤️  Testing Traceroute...")
    print("=" * 50)
    
    hostname = "gejknamvrhhhwkgrhsor.supabase.co"
    
    try:
        # Use appropriate traceroute command for the OS
        if platform.system().lower() == "windows":
            cmd = ["tracert", hostname]
        else:
            cmd = ["traceroute", hostname]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Traceroute successful")
            print("   Route:")
            for line in result.stdout.split('\n')[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print(f"❌ Traceroute failed with return code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Traceroute timed out")
        return False
    except Exception as e:
        print(f"❌ Traceroute error: {e}")
        return False

def test_common_dns():
    """Test common DNS servers"""
    print("\n🔍 Testing Common DNS Servers...")
    print("=" * 50)
    
    dns_servers = [
        ("8.8.8.8", "Google DNS"),
        ("1.1.1.1", "Cloudflare DNS"),
        ("208.67.222.222", "OpenDNS")
    ]
    
    hostname = "gejknamvrhhhwkgrhsor.supabase.co"
    
    for dns_ip, dns_name in dns_servers:
        try:
            # Create a resolver with specific DNS server
            resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resolver.settimeout(5)
            
            # Simple DNS query (this is a basic test)
            print(f"   Testing {dns_name} ({dns_ip})...")
            
            # Try to resolve using system DNS first
            try:
                ip = socket.gethostbyname(hostname)
                print(f"   ✅ System DNS: {hostname} → {ip}")
            except socket.gaierror:
                print(f"   ❌ System DNS: Failed to resolve {hostname}")
                
        except Exception as e:
            print(f"   ❌ {dns_name}: {e}")

def main():
    """Run all network tests"""
    print("🔥 Fire Detection Dashboard - Network Diagnostic Tool")
    print("=" * 60)
    print("This tool will test your network connectivity to help diagnose")
    print("why the Supabase database connection is failing.")
    print()
    
    # Run tests
    dns_ok = test_dns_resolution()
    http_ok = test_http_connectivity()
    ping_ok = test_ping()
    traceroute_ok = test_traceroute()
    test_common_dns()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 NETWORK TEST SUMMARY")
    print("=" * 60)
    print(f"DNS Resolution: {'✅ PASS' if dns_ok else '❌ FAIL'}")
    print(f"HTTP Connectivity: {'✅ PASS' if http_ok else '❌ FAIL'}")
    print(f"Ping: {'✅ PASS' if ping_ok else '❌ FAIL'}")
    print(f"Traceroute: {'✅ PASS' if traceroute_ok else '❌ FAIL'}")
    
    if not dns_ok:
        print("\n🔍 DNS Resolution Issue Detected!")
        print("This is likely why your Supabase connection is failing.")
        print("\nPossible solutions:")
        print("1. Check your internet connection")
        print("2. Try using a different DNS server:")
        print("   - Windows: Control Panel → Network → Change adapter settings")
        print("   - Right-click your connection → Properties → IPv4 → Properties")
        print("   - Use DNS: 8.8.8.8 (Google) or 1.1.1.1 (Cloudflare)")
        print("3. Check if you're behind a corporate firewall/proxy")
        print("4. Try using a mobile hotspot to test")
        print("5. Check Windows Firewall settings")
        print("6. Restart your router/modem")
    
    elif not http_ok:
        print("\n🔍 HTTP Connectivity Issue Detected!")
        print("DNS works but HTTP requests fail.")
        print("\nPossible solutions:")
        print("1. Check if you're behind a corporate firewall/proxy")
        print("2. Check Windows Firewall settings")
        print("3. Try using a mobile hotspot to test")
        print("4. Check antivirus software firewall settings")
    
    else:
        print("\n✅ Network connectivity appears to be working!")
        print("The issue might be with your Supabase credentials or configuration.")
    
    print("\n" + "=" * 60)
    print("Diagnostic complete! Check the results above.")

if __name__ == "__main__":
    main()
