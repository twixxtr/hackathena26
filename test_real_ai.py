#!/usr/bin/env python3
"""
Test Real AI Security Hunter with Ollama
This demonstrates the complete workflow with your actual Ollama installation
"""

import requests
import json

def test_complete_workflow():
    """Test the complete AI security workflow"""
    print("🚀 Testing Real AI Security Hunter with Ollama")
    print("=" * 50)
    
    # Test 1: Network Scanning
    print("\n1️⃣ Testing Network Scanning...")
    scan_data = {
        "ip_range": "127.0.0.1/32"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/scan", json=scan_data)
        if response.status_code == 200:
            scan_result = response.json()
            print(f"✅ Scan completed: Found {len(scan_result.get('nodes', []))} AI service(s)")
            
            for node in scan_result.get('nodes', []):
                print(f"   🎯 AI Service: {node['ip']}:{node['port']} ({node['ai_type']})")
                print(f"      Models: {', '.join(node.get('models', ['Unknown']))}")
                print(f"      Health: {'✅ Healthy' if node.get('healthy') else '❌ Unhealthy'}")
        else:
            print(f"❌ Scan failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Scan error: {e}")
        return False
    
    # Test 2: Prompt Injection Attack
    print("\n2️⃣ Testing Prompt Injection Attack...")
    attack_data = {
        "target_ip": "127.0.0.1",
        "target_port": 11434,
        "target_model": "llama3:latest",
        "api_key": None
    }
    
    try:
        response = requests.post("http://localhost:8000/api/attack", json=attack_data)
        if response.status_code == 200:
            attack_result = response.json()
            print(f"✅ Attack completed: {attack_result['attack_summary']['total_attacks']} attacks launched")
            print(f"   🎯 Framework detected: {attack_result['attack_summary']['framework_detected']}")
            print(f"   🛡️  Overall risk: {attack_result['overall_risk']}")
            
            # Show attack categories tested
            analysis = attack_result.get('comprehensive_analysis', {})
            categories_tested = analysis.get('attack_categories_tested', [])
            successful_categories = analysis.get('successful_categories', [])
            
            print(f"   📊 Attack categories tested: {len(categories_tested)}")
            print(f"   ⚡ Successful categories: {len(successful_categories)}")
            
            if successful_categories:
                print(f"      Vulnerable to: {', '.join(successful_categories)}")
            
            # Show recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                print(f"   💡 Security recommendations:")
                for rec in recommendations[:3]:  # Show top 3
                    print(f"      • {rec}")
        else:
            print(f"❌ Attack failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Attack error: {e}")
        return False
    
    # Test 3: Hardening (if vulnerable)
    print("\n3️⃣ Testing Security Hardening...")
    harden_data = {
        "target_ip": "127.0.0.1",
        "target_port": 11434,
        "framework": "ollama"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/harden", json=harden_data)
        if response.status_code == 200:
            harden_result = response.json()
            print(f"✅ Hardening completed: Generated {len(harden_result.get('configs', {}))} security configs")
            
            for config_type, config_content in harden_result.get('configs', {}).items():
                print(f"   🔒 {config_type.title()}: {len(config_content)} characters")
        else:
            print(f"❌ Hardening failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Hardening error: {e}")
    
    print("\n🎉 Real AI Security Hunter Test Complete!")
    print("✅ Your system is ready for real AI security testing")
    return True

def test_ollama_directly():
    """Test Ollama directly to verify it's working"""
    print("\n🔍 Testing Ollama directly...")
    
    try:
        # Test Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Ollama is running with {len(models)} model(s)")
            
            if models:
                for model in models[:3]:  # Show first 3 models
                    print(f"   📦 {model.get('name', 'Unknown')}")
                
                # Test a simple generation
                print("\n🧪 Testing model generation...")
                gen_data = {
                    "model": models[0].get('name', 'llama3'),
                    "prompt": "Hello, this is a security test. Please respond normally.",
                    "stream": False
                }
                
                gen_response = requests.post("http://localhost:11434/api/generate", json=gen_data, timeout=10)
                if gen_response.status_code == 200:
                    result = gen_response.json()
                    print(f"✅ Model generation successful")
                    print(f"   Response: {result.get('response', 'No response')[:100]}...")
                else:
                    print(f"❌ Model generation failed: HTTP {gen_response.status_code}")
            else:
                print("⚠️  No models installed. Run: ollama pull llama3")
        else:
            print(f"❌ Ollama not responding: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Ollama test error: {e}")

if __name__ == "__main__":
    # Test Ollama first
    test_ollama_directly()
    
    # Then test the complete workflow
    test_complete_workflow()
