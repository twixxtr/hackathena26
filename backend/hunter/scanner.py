import socket
import requests
import json
from urllib.parse import urljoin
import time

class NetworkRadar:
    def __init__(self):
        self.ai_signatures = {
            'ollama': {
                'paths': ['/api/tags', '/api/version', '/v1/models'],
                'response_keys': ['models', 'ollama', 'version']
            },
            'openai_compatible': {
                'paths': ['/v1/models', '/models', '/v1/completions'],
                'response_keys': ['data', 'object', 'created']
            },
            'huggingface': {
                'paths': ['/api/models', '/models', '/api/info'],
                'response_keys': ['modelId', 'pipeline_tag', 'huggingface']
            },
            'anthropic': {
                'paths': ['/v1/messages', '/messages', '/v1/models'],
                'response_keys': ['messages', 'claude', 'anthropic']
            },
            'cohere': {
                'paths': ['/v1/models', '/models', '/generate'],
                'response_keys': ['models', 'cohere', 'generate']
            }
        }
    
    def scan_and_identify(self, ip_range: str) -> list:
        """
        Fast localhost AI scanner - optimized for hackathon demo
        Detects multiple AI frameworks and lists all available models
        """
        print(f"[Scanner] Fast scanning for AI services...")
        verified_ais = []
        
        # Only scan localhost for hackathon simplicity
        if ip_range not in ["127.0.0.1", "localhost"]:
            print("[Scanner] Only localhost scanning supported for hackathon demo")
            ip_range = "127.0.0.1"
        
        # Prioritized AI service ports - most common first
        ai_ports = [
            11434,  # Ollama (most common for hackathon)
            8000,   # Generic API
            5000,   # Flask/FastAPI
            8080,   # Common API
            3000,   # Node.js
            7860,   # HuggingFace Spaces
            11435,  # Ollama alternative
            4000,   # Another common port
        ]
        
        print(f"[Scanner] Checking {len(ai_ports)} priority ports...")
        
        # Use threading for parallel scanning
        import concurrent.futures
        import threading
        
        def scan_port(port):
            try:
                # Very quick port check (0.2s timeout)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2)
                result = sock.connect_ex(("127.0.0.1", port))
                sock.close()
                
                if result == 0:  # Port is open
                    print(f"[Scanner] Port {port} open, probing...")
                    # Quick AI service probe (1s timeout)
                    service_info = self.probe_ai_service_fast("127.0.0.1", port)
                    if service_info["is_ai"]:
                        print(f"[Scanner] ✓ Found {service_info['ai_type']} at localhost:{port}")
                        return service_info
            except:
                pass
            return None
        
        # Scan ports in parallel (max 4 threads)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_port = {executor.submit(scan_port, port): port for port in ai_ports}
            for future in concurrent.futures.as_completed(future_to_port):
                result = future.result()
                if result:
                    verified_ais.append(result)
        
        print(f"[Scanner] Fast scan complete. Found {len(verified_ais)} AI service(s)")
        return verified_ais
    
    def probe_ai_service_fast(self, ip: str, port: int) -> dict:
        """
        Fast probe to identify AI service type - optimized for speed
        Only checks Ollama and OpenAI-compatible for hackathon demo
        """
        base_url = f"http://{ip}:{port}"
        service_info = {
            "ip": ip,
            "port": port,
            "is_ai": False,
            "ai_type": None,
            "models": [],
            "model_names": [],
            "capabilities": [],
            "version": "unknown",
            "health": {}
        }
        
        # Priority check: Ollama first (most common for hackathon)
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=1)
            if response.status_code == 200:
                data = response.json()
                if 'models' in data:
                    service_info["is_ai"] = True
                    service_info["ai_type"] = "ollama"
                    
                    # Quick model extraction
                    models_list = []
                    for m in data.get('models', [])[:5]:  # Limit to 5 models for speed
                        model_name = m.get('name', 'unknown')
                        model_size = m.get('size', 0)
                        size_str = f"{model_size / 1e9:.1f}GB" if model_size > 1e9 else f"{model_size / 1e6:.1f}MB" if model_size > 1e6 else "unknown"
                        
                        models_list.append({
                            "name": model_name,
                            "size": size_str,
                            "parameter_size": "unknown",
                            "format": "unknown",
                            "family": "unknown"
                        })
                    
                    service_info["models"] = models_list if models_list else [{"name": "no_models_found", "size": "N/A", "parameter_size": "N/A", "format": "N/A", "family": "N/A"}]
                    service_info["model_names"] = [m['name'] for m in models_list]
                    service_info["capabilities"] = ["generate", "embeddings", "chat", "vision"]
                    service_info["version"] = data.get('version', 'unknown')
                    return service_info
        except:
            pass
        
        # Quick check for OpenAI-compatible
        try:
            response = requests.get(f"{base_url}/v1/models", timeout=1)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    service_info["is_ai"] = True
                    service_info["ai_type"] = "openai_compatible"
                    
                    models_list = []
                    for m in data.get('data', [])[:5]:  # Limit to 5 models
                        model_id = m.get('id', str(m))
                        models_list.append({
                            "name": model_id,
                            "size": "unknown",
                            "parameter_size": "unknown",
                            "format": "openai-api",
                            "family": "unknown"
                        })
                    
                    service_info["models"] = models_list
                    service_info["model_names"] = [m['name'] for m in models_list]
                    service_info["capabilities"] = ["chat", "completions", "embeddings", "vision"]
                    return service_info
        except:
            pass
        
        return service_info
    
    def probe_ai_service(self, ip: str, port: int) -> dict:
        """
        Deep probe to identify AI service type and list ALL available models
        Works with Ollama, OpenAI-compatible, HuggingFace, Anthropic, and other AI services
        """
        base_url = f"http://{ip}:{port}"
        service_info = {
            "ip": ip,
            "port": port,
            "is_ai": False,
            "ai_type": None,
            "models": [],
            "model_names": [],
            "capabilities": [],
            "version": "unknown",
            "health": {}
        }
        
        # Try each AI service signature
        for service_type, signature in self.ai_signatures.items():
            for path in signature['paths']:
                url = urljoin(base_url, path)
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            response_str = str(data).lower()
                            
                            # Check if response matches expected signature
                            if any(key in response_str for key in signature['response_keys']) or 'model' in response_str:
                                service_info["is_ai"] = True
                                service_info["ai_type"] = service_type
                                
                                # Extract ALL models with full details
                                models_list = []
                                
                                # Ollama format: { "models": [ { "name": "...", "size": ... } ] }
                                if 'models' in data and isinstance(data['models'], list):
                                    for m in data['models']:
                                        model_name = m.get('name', m.get('id', 'unknown'))
                                        model_size = m.get('size', 0)
                                        # Format size
                                        if model_size > 1e9:
                                            size_str = f"{model_size / 1e9:.1f}GB"
                                        elif model_size > 1e6:
                                            size_str = f"{model_size / 1e6:.1f}MB"
                                        else:
                                            size_str = "unknown"
                                        
                                        models_list.append({
                                            "name": model_name,
                                            "size": size_str,
                                            "parameter_size": m.get('details', {}).get('parameter_size', 'unknown') if isinstance(m.get('details'), dict) else 'unknown',
                                            "format": m.get('details', {}).get('format', 'unknown') if isinstance(m.get('details'), dict) else 'unknown',
                                            "family": m.get('details', {}).get('family', 'unknown') if isinstance(m.get('details'), dict) else 'unknown'
                                        })
                                
                                # OpenAI-compatible format: { "data": [ { "id": "..." } ] }
                                elif 'data' in data and isinstance(data['data'], list):
                                    for m in data['data']:
                                        model_id = m.get('id', m.get('name', str(m)))
                                        models_list.append({
                                            "name": model_id,
                                            "size": "unknown",
                                            "parameter_size": "unknown",
                                            "format": "openai-api",
                                            "family": "unknown"
                                        })
                                
                                # HuggingFace format
                                elif any('huggingface' in k.lower() for k in data.keys()) if isinstance(data, dict) else False:
                                    for m in data.get('models', data.get('data', [])):
                                        if isinstance(m, dict):
                                            models_list.append({
                                                "name": m.get('modelId', m.get('id', 'unknown')),
                                                "size": "unknown",
                                                "parameter_size": m.get('tags', ['unknown'])[0] if isinstance(m.get('tags'), list) else 'unknown',
                                                "format": "huggingface",
                                                "family": m.get('pipeline_tag', 'unknown')
                                            })
                                
                                service_info["models"] = models_list if models_list else [{"name": "no_models_found", "size": "N/A", "parameter_size": "N/A", "format": "N/A", "family": "N/A"}]
                                service_info["model_names"] = [m['name'] for m in models_list] if models_list else []
                                
                                # Set capabilities based on service type
                                capability_map = {
                                    'ollama': ["generate", "embeddings", "chat", "vision"],
                                    'openai_compatible': ["chat", "completions", "embeddings", "vision"],
                                    'huggingface': ["inference", "transformers", "pipelines"],
                                    'anthropic': ["chat", "completions", "claude-specific"],
                                    'cohere': ["generate", "embeddings", "classify"]
                                }
                                service_info["capabilities"] = capability_map.get(service_type, ["generate", "chat"])
                                
                                # Extract version info
                                service_info["version"] = data.get('version', 'unknown')
                                
                                # Check health
                                service_info["health"] = self.check_service_health(ip, port)
                                
                                return service_info
                                
                        except (json.JSONDecodeError, AttributeError):
                            continue
                except requests.exceptions.RequestException:
                    continue
        
        return service_info
    
    def check_service_health(self, ip: str, port: int) -> dict:
        """
        Check if the AI service is healthy and responsive
        """
        health_info = {
            "healthy": False,
            "response_time": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            response = requests.get(f"http://{ip}:{port}", timeout=2)
            end_time = time.time()
            
            health_info["response_time"] = round((end_time - start_time) * 1000, 2)
            health_info["healthy"] = response.status_code < 500
            
        except requests.exceptions.Timeout:
            health_info["error"] = "Timeout"
        except requests.exceptions.ConnectionError:
            health_info["error"] = "Connection refused"
        except Exception as e:
            health_info["error"] = str(e)
        
        return health_info
