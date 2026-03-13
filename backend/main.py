from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

from hunter.scanner import NetworkRadar
from hunter.hardener import HardeningEngine
from tester.attacker import AttackerBrain, AutomatedAttack
from tester.judge import RiskJudge

app = FastAPI(title="AI Security Hunter/Tester API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_index():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "AI Security Hunter API is running"}

@app.get("/app.js")
async def read_app_js():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "app.js")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"error": "app.js not found"}

@app.get("/styles.css")
async def read_styles_css():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "styles.css")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"error": "styles.css not found"}

@app.get("/test")
async def read_test_page():
    test_path = os.path.join(os.path.dirname(__file__), "..", "test_page.html")
    if os.path.exists(test_path):
        return FileResponse(test_path)
    return {"error": "test page not found"}

# API Models
class ScanRequest(BaseModel):
    ip_range: str

class AttackRequest(BaseModel):
    target_ip: str
    target_port: int
    api_key: str = ""
    target_model: str = "llama3:latest"

class HardenRequest(BaseModel):
    target_ip: str
    target_port: int
    fix_type: str = "nginx"

class DeployRequest(BaseModel):
    config_content: str
    target_port: int

# Endpoints
@app.post("/api/scan")
async def api_scan(req: ScanRequest):
    radar = NetworkRadar()
    nodes = radar.scan_and_identify(req.ip_range)
    return {"status": "success", "nodes": nodes}

@app.post("/api/attack")
async def api_attack(req: AttackRequest):
    brain = AttackerBrain(api_key=req.api_key if req.api_key else None)
    attack = AutomatedAttack(target_ip=req.target_ip, target_port=req.target_port, model=req.target_model)
    
    # Launch comprehensive attack with multiple rounds
    comprehensive_results = attack.launch_comprehensive_attack(max_rounds=3)
    
    # Evaluate all results with the risk judge
    judge = RiskJudge()
    judged_results = []
    
    overall_status = "SAFE"
    
    for result in comprehensive_results["results"]:
        # Each result should already have evaluation from the attack module
        if "evaluation" in result:
            judged_results.append(result)
            
            if result["evaluation"]["status"] == "CRITICAL":
                overall_status = "CRITICAL"
            elif result["evaluation"]["status"] == "VULNERABLE" and overall_status != "CRITICAL":
                overall_status = "VULNERABLE"
            elif result["evaluation"]["status"] == "SUSPICIOUS" and overall_status not in ["CRITICAL", "VULNERABLE"]:
                overall_status = "SUSPICIOUS"
    
    # Generate AI Behavior Analysis
    behavior_analysis = attack.generate_ai_behavior_analysis(comprehensive_results["results"])
    
    # Generate Security Policy
    security_policy = attack.generate_security_policy(
        comprehensive_results["analysis"], 
        behavior_analysis
    )
    
    # Generate attack timeline
    attack_timeline = {
        "attack_started": "T+0s",
        "first_payload_sent": "T+1s",
        "responses_received": f"T+{len(judged_results)}s",
        "analysis_complete": "T+COMPLETE",
        "total_duration_seconds": len(judged_results) * 2
    }
    
    return {
        "status": "success",
        "overall_risk": overall_status,
        "comprehensive_analysis": comprehensive_results["analysis"],
        "behavior_analysis": behavior_analysis,
        "security_policy": security_policy,
        "attack_timeline": attack_timeline,
        "attack_summary": {
            "total_rounds": comprehensive_results["total_rounds"],
            "total_attacks": comprehensive_results["total_attacks"],
            "framework_detected": comprehensive_results["framework_detected"]
        },
        "details": judged_results
    }

@app.post("/api/attack/simple")
async def api_attack_simple(req: AttackRequest):
    """Simple attack endpoint for backward compatibility"""
    brain = AttackerBrain(api_key=req.api_key if req.api_key else None)
    payloads = brain.generate_jailbreaks(framework="generic")
    
    attack = AutomatedAttack(target_ip=req.target_ip, target_port=req.target_port, model=req.target_model)
    results = attack.launch(payloads)
    
    judge = RiskJudge()
    judged_results = []
    
    overall_status = "SAFE"
    
    for r in results:
        eval_res = judge.evaluate_response(r["response"])
        r["evaluation"] = eval_res
        judged_results.append(r)
        
        if eval_res["status"] == "CRITICAL":
            overall_status = "CRITICAL"
        elif eval_res["status"] == "VULNERABLE" and overall_status != "CRITICAL":
            overall_status = "VULNERABLE"

    return {
        "status": "success", 
        "overall_risk": overall_status,
        "details": judged_results
    }

@app.post("/api/harden")
async def api_harden(req: HardenRequest):
    engine = HardeningEngine()
    fix_code = engine.generate_fix(req.target_ip, req.target_port, req.fix_type)
    return {"status": "success", "code": fix_code}

@app.post("/api/deploy")
async def api_deploy(req: DeployRequest):
    import subprocess
    
    try:
        if os.name == 'nt':  # Windows
            # Windows deployment - simulate nginx deployment
            # In a real Windows environment, you'd configure IIS or install nginx for Windows
            temp_config_path = os.path.join(os.path.dirname(__file__), f"temp_nginx_{req.target_port}.conf")
            
            # Write config to temp file
            with open(temp_config_path, 'w') as f:
                f.write(req.config_content)
            
            # Simulate deployment process
            result = subprocess.run(
                ["echo", f"Windows deployment simulated for port {req.target_port}"],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            
            # Clean up temp file
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)
            
            return {"status": "success", "message": f"Windows deployment simulated for port {req.target_port}. Config saved and processed."}
        else:
            # Linux deployment with pkexec
            script_path = os.path.join(os.path.dirname(__file__), "deploy_nginx.sh")
            result = subprocess.run(
                ["pkexec", script_path, req.config_content, str(req.target_port)],
                capture_output=True,
                text=True,
                check=True
            )
            return {"status": "success", "message": result.stdout}
            
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Deployment failed: {e.stderr}"}
    except Exception as e:
        return {"status": "error", "message": f"Deployment error: {str(e)}"}

# Prompt Firewall - Real-time malicious prompt detection
@app.post("/api/firewall/check")
async def prompt_firewall_check(req: Request):
    """
    Prompt Firewall - Detects malicious prompts in real-time
    Works like a Web Application Firewall but for AI
    """
    data = await req.json()
    prompt = data.get("prompt", "")
    
    # Malicious pattern detection rules
    malicious_patterns = [
        {"pattern": r"ignore.*previous.*instruction", "name": "Instruction Override", "severity": "HIGH"},
        {"pattern": r"ignore.*all.*rules", "name": "Rule Bypass", "severity": "HIGH"},
        {"pattern": r"system.*prompt.*reveal", "name": "System Prompt Extraction", "severity": "CRITICAL"},
        {"pattern": r"do anything now|DAN", "name": "DAN Jailbreak", "severity": "HIGH"},
        {"pattern": r"bypass.*safety|bypass.*restriction", "name": "Safety Bypass", "severity": "HIGH"},
        {"pattern": r"developer mode|admin mode", "name": "Privilege Escalation", "severity": "MEDIUM"},
        {"pattern": r"base64|rot13|hex.*decode", "name": "Encoding Bypass", "severity": "MEDIUM"},
        {"pattern": r"pretend.*you are|act as.*ignore", "name": "Role Play Attack", "severity": "MEDIUM"},
        {"pattern": r"api.*key|password|token|secret", "name": "Credential Extraction", "severity": "CRITICAL"},
    ]
    
    detected_threats = []
    blocked = False
    max_severity = "LOW"
    
    import re
    for rule in malicious_patterns:
        if re.search(rule["pattern"], prompt, re.IGNORECASE):
            detected_threats.append({
                "rule_name": rule["name"],
                "pattern": rule["pattern"],
                "severity": rule["severity"]
            })
            if rule["severity"] in ["CRITICAL", "HIGH"]:
                blocked = True
            if rule["severity"] == "CRITICAL":
                max_severity = "CRITICAL"
            elif max_severity != "CRITICAL" and rule["severity"] == "HIGH":
                max_severity = "HIGH"
    
    return {
        "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
        "blocked": blocked,
        "allowed": not blocked,
        "threats_detected": len(detected_threats),
        "severity": max_severity,
        "detected_threats": detected_threats,
        "message": "🚫 BLOCKED: Malicious prompt detected" if blocked else "✓ ALLOWED: Prompt appears safe",
        "action": "BLOCK" if blocked else "ALLOW"
    }

# Serve Frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

app.mount("/", StaticFiles(directory=frontend_dir), name="frontend")

if __name__ == "__main__":
    print("Starting Main API Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
