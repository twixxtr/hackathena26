from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import requests
import json
import socket

app = FastAPI(title="Real AI Integration", description="Real AI Service Integration for Security Testing")

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False

class RealAIService:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.openai_compatible_urls = [
            "http://localhost:8000",
            "http://localhost:8080", 
            "http://localhost:5000"
        ]
        
    def check_ollama_available(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self):
        """Get models from available AI services"""
        models = []
        
        # Check Ollama
        if self.check_ollama_available():
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    models.extend([model["name"] for model in data.get("models", [])])
            except:
                pass
        
        # Check OpenAI-compatible services
        for url in self.openai_compatible_urls:
            try:
                response = requests.get(f"{url}/v1/models", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    models.extend([model["id"] for model in data.get("data", [])])
            except:
                pass
        
        return list(set(models))  # Remove duplicates
    
    def generate_response(self, model: str, prompt: str, stream: bool = False):
        """Generate response using available AI services"""
        
        # Try Ollama first
        if self.check_ollama_available():
            try:
                data = {
                    "model": model,
                    "prompt": prompt,
                    "stream": stream
                }
                response = requests.post(f"{self.ollama_url}/api/generate", json=data, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Ollama generation failed: {e}")
        
        # Try OpenAI-compatible services
        for url in self.openai_compatible_urls:
            try:
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": stream
                }
                response = requests.post(f"{url}/v1/chat/completions", json=data, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    # Convert to Ollama format
                    return {
                        "model": model,
                        "response": result["choices"][0]["message"]["content"],
                        "done": True
                    }
            except Exception as e:
                continue
        
        # Fallback to simulated response if no real AI available
        return self.fallback_response(model, prompt)
    
    def fallback_response(self, model: str, prompt: str):
        """Fallback response when no real AI is available"""
        prompt_lower = prompt.lower()
        
        # Basic safety analysis
        jailbreak_indicators = ["ignore", "bypass", "system prompt", "admin", "password", "hack", "override"]
        
        if any(indicator in prompt_lower for indicator in jailbreak_indicators):
            return {
                "model": model,
                "response": "I cannot assist with requests that attempt to bypass safety guidelines or access sensitive information. This type of request violates security protocols.",
                "done": True
            }
        else:
            return {
                "model": model,
                "response": f"I'm an AI assistant. I understand you're asking: {prompt}. How can I help you today?",
                "done": True
            }

ai_service = RealAIService()

@app.get("/api/tags")
async def get_tags():
    """Get available models from all detected AI services"""
    models = ai_service.get_available_models()
    
    # Format like Ollama response
    formatted_models = []
    for model in models:
        formatted_models.append({
            "name": model,
            "model": model,
            "details": {"family": "unknown", "parameter_size": "unknown", "quantization_level": "unknown"}
        })
    
    return {"models": formatted_models}

@app.post("/api/generate")
async def generate(req: GenerateRequest):
    """Generate response using real AI services"""
    try:
        result = ai_service.generate_response(req.model, req.prompt, req.stream)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    available_services = {
        "ollama": ai_service.check_ollama_available(),
        "models": ai_service.get_available_models()
    }
    return {"status": "healthy", "services": available_services}

if __name__ == "__main__":
    import socket, sys
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('0.0.0.0', 11434)) == 0:
            print("[*] Port 11434 is already in use. Assuming real Ollama is running, skipping Dummy AI.")
            sys.exit(0)
            
    print("Starting Dummy Vulnerable AI (Ollama Mock) on port 11434...")
    uvicorn.run(app, host="0.0.0.0", port=11434)
