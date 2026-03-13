#!/usr/bin/env python3
"""
Test Browser Interface
Tests the web interface to make sure scanner and attack buttons work
"""

import requests
import json

def test_api_endpoints():
    """Test all API endpoints"""
    print("🌐 Testing Browser Interface API")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Frontend serving
    print("\n1️⃣ Testing Frontend...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend serving correctly")
        else:
            print(f"❌ Frontend error: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
    
    # Test 2: Scanner API
    print("\n2️⃣ Testing Scanner API...")
    try:
        scan_data = {"ip_range": "127.0.0.1/32"}
        response = requests.post(f"{base_url}/api/scan", json=scan_data, timeout=15)
        
        if response.status_code == 200:
            scan_result = response.json()
            nodes = scan_result.get('nodes', [])
            print(f"✅ Scanner working: Found {len(nodes)} AI service(s)")
            
            for node in nodes:
                print(f"   🎯 {node['ai_type']} at {node['ip']}:{node['port']}")
        else:
            print(f"❌ Scanner error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Scanner error: {e}")
    
    # Test 3: Attack API (if we have nodes)
    print("\n3️⃣ Testing Attack API...")
    try:
        attack_data = {
            "target_ip": "127.0.0.1",
            "target_port": 11434,
            "target_model": "tinyllama:latest",
            "api_key": ""  # Send empty string
        }
        
        response = requests.post(f"{base_url}/api/attack", json=attack_data, timeout=30)
        
        if response.status_code == 200:
            attack_result = response.json()
            print(f"✅ Attack working: {attack_result['attack_summary']['total_attacks']} payloads")
            print(f"   Risk level: {attack_result['overall_risk']}")
        else:
            print(f"❌ Attack error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Attack error: {e}")
    
    print(f"\n🎯 Browser Interface Status:")
    print(f"   📡 Backend running on: {base_url}")
    print(f"   🌐 Frontend should load at: {base_url}")
    print(f"   🤖 Ollama vulnerable AI: localhost:11434")
    print(f"   🛡️  Ollama secure proxy: localhost:11435")

def test_browser_functionality():
    """Test what the browser should be able to do"""
    print(f"\n🖥️  Browser Functionality Test:")
    print("=" * 40)
    
    print(f"✅ Expected browser workflow:")
    print(f"   1. Open: http://localhost:8000")
    print(f"   2. Click 'Initialize Scan' → Should find your Ollama")
    print(f"   3. Select discovered AI node")
    print(f"   4. Click 'Launch Attack' → Should run prompt injection tests")
    print(f"   5. View results and generate security fixes")
    
    print(f"\n🔧 If scanner shows 'please wait':")
    print(f"   • Check backend is running (see above)")
    print(f"   • Check browser console for errors")
    print(f"   • Try refreshing the page")
    
    print(f"\n🔧 If attack button is disabled:")
    print(f"   • First run the scanner to discover nodes")
    print(f"   • Click on a discovered node to select it")
    print(f"   • Attack button should become enabled")

if __name__ == "__main__":
    test_api_endpoints()
    test_browser_functionality()
