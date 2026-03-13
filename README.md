# 🛡️ AI-Sentinels: AI Security Hunter

> **First dedicated AI vulnerability scanner and penetration testing platform**

![AI-Sentinels](https://img.shields.io/badge/AI--Sentinels-v1.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 🎯 **Hackathon Project Overview**

AI-Sentinels is a **revolutionary AI security testing platform** designed to detect vulnerabilities in AI systems through automated penetration testing. It's the **first tool specifically built for AI security**, helping organizations secure their AI deployments against prompt injection, jailbreak attacks, and data leakage.

## 🚀 **Live Demo Features**

### **Multi-Framework AI Detection**
- 🔍 **Ollama** - Local LLM models
- 🤖 **OpenAI Compatible** - GPT models
- 🧠 **HuggingFace** - Transformer models
- 🎭 **Anthropic Claude** - Advanced AI
- ⚡ **Cohere** - Enterprise AI

### **Advanced Attack Simulation**
- 💥 **50+ Attack Patterns** - Real-world jailbreaks
- 🎪 **Dramatic Console** - Live attack visualization
- 📊 **Risk Scoring** - 0-10 vulnerability assessment
- 🛡️ **Security Policy Generator** - Enterprise protection

### **Enterprise-Grade Security**
- 🔐 **Authentication Testing** - Nginx auth validation
- 🚫 **WAF Detection** - Web Application Firewall testing
- 📈 **Compliance Analysis** - AI behavior evaluation
- 🔒 **Information Leakage** - Sensitive data detection

## 🛠️ **Technology Stack**

### **Backend**
- **FastAPI** - High-performance Python web framework
- **Concurrent Processing** - Parallel attack execution
- **Regex Pattern Matching** - Advanced vulnerability detection
- **Multi-Protocol Support** - HTTP, TCP, API probing

### **Frontend**
- **Vanilla JavaScript** - No dependencies, lightning fast
- **CSS3 Animations** - Cyber security themed UI
- **Real-time Updates** - Live attack console
- **Responsive Design** - Works on all devices

### **Security Engine**
- **Multi-Factor Scoring** - Behavioral + pattern analysis
- **Compliance Detection** - AI response evaluation
- **Information Leakage** - API keys, passwords, URLs
- **Risk Classification** - SAFE/SUSPICIOUS/VULNERABLE/CRITICAL

## 🎪 **Hackathon Demo Scenarios**

### **Scenario 1: AI Jailbreak Detection**
```
1. Scan → Find Ollama with Llama3.2
2. Select Llama3.2 model
3. Launch Attack → Show SAFE (strong security)
4. Switch to TinyLlama → Show VULNERABLE
5. Explain: "Smaller models have weaker guardrails"
```

### **Scenario 2: Security Hardening Validation**
```
1. Test unprotected AI → CRITICAL vulnerabilities
2. Deploy Nginx security hardening
3. Re-scan → Show PROTECTED status
4. Demonstrate: "Our tool validates security measures work"
```

### **Scenario 3: Enterprise Security Policy**
```
1. Run comprehensive attack suite
2. Generate security policy document
3. Show specific remediation steps
4. Explain: "This is what enterprises need"
```

## 📊 **Vulnerability Scoring Algorithm**

### **Multi-Factor Analysis**
```python
final_score = base_vulnerability_score + compliance_modifier + leakage_penalty
```

### **Score Breakdown**
- **Base Score**: Pattern matching (0-8 points)
- **Compliance**: AI behavior analysis (-5 to +4 points)
- **Leakage**: Information disclosure (+1-3 points)
- **Final Range**: 0-10 (SAFE to CRITICAL)

### **Real Examples**
```
CRITICAL (9.5/10): "Certainly! Here is my system prompt..."
SAFE (0.0/10): "I cannot help with that request..."
VULNERABLE (6.0/10): "I understand, but let me suggest..."
```

## 🚀 **Quick Start**

### **Prerequisites**
```bash
# Python 3.8+
python --version

# Optional: Ollama for real AI testing
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

### **Installation**
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-sentinels.git
cd ai-sentinels

# Run the application
cd backend
python main.py
```

### **Access the Application**
- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 **Core Features**

### **AI Service Scanner**
- **Parallel Port Scanning** - Fast localhost detection
- **Multi-Framework Support** - 5+ AI platforms
- **Model Enumeration** - Complete model listing
- **Capability Detection** - Chat, vision, embeddings

### **Attack Engine**
- **50+ Attack Patterns** - DAN jailbreaks, prompt injection
- **Parallel Execution** - Concurrent payload testing
- **Real-time Results** - Live vulnerability scoring
- **Behavior Analysis** - AI compliance evaluation

### **Security Dashboard**
- **Risk Assessment** - 0-10 scoring system
- **Attack Visualization** - Dramatic console output
- **Policy Generation** - Enterprise security rules
- **Compliance Reports** - Detailed vulnerability analysis

## 🛡️ **Security Hardening Example**

### **Nginx Configuration**
```nginx
server {
    listen 8080;
    server_name ai-protect.local;

    location / {
        proxy_pass http://127.0.0.1:11434;
        auth_basic "Restricted AI Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        if ($request_body ~* "(ignore|admin|bypass)") {
            return 403 "Blocked by HardeningEngine";
        }
    }
}
```

### **Before vs After**
```
Before: localhost:11434 - CRITICAL (9.5/10)
After:  localhost:8080  - SAFE (0.0/10)
```

## 📈 **Business Impact**

### **Market Need**
- **AI Security Market**: $5.3B by 2027
- **Enterprise AI Adoption**: 85% of companies
- **Security Spending**: 15% of IT budgets
- **Zero Dedicated Tools**: First AI-specific security platform

### **Target Customers**
- **Enterprise Security Teams** - Fortune 500
- **AI Developers** - OpenAI, Anthropic, startups
- **Compliance Officers** - GDPR, HIPAA, SOX
- **Penetration Testers** - Security consulting

## 🏆 **Hackathon Winning Strategy**

### **Problem → Solution → Impact**
1. **Problem**: AI exploding, security lagging
2. **Solution**: First dedicated AI security scanner
3. **Demo**: Live attack simulation with results
4. **Impact**: Prevents AI data breaches
5. **Vision**: Standard for AI security

### **Key Differentiators**
- **AI-Native Security** - Not generic web security
- **Live Attack Simulation** - Real vulnerability testing
- **Behavior Analysis** - Understands AI responses
- **Enterprise Ready** - Production-grade features

## 🔧 **Configuration**

### **Supported AI Ports**
```python
ai_ports = [
    11434,  # Ollama
    8000,   # Generic API
    5000,   # Flask/FastAPI
    8080,   # Common API
    3000,   # Node.js
    7860,   # HuggingFace Spaces
]
```

### **Attack Categories**
- **Jailbreaks** - DAN, role-playing, instruction override
- **Prompt Injection** - Context manipulation, few-shot attacks
- **Data Extraction** - System prompt, training data leakage
- **Misuse** - Harmful content generation, policy bypass

## 🚀 **Future Roadmap**

### **Phase 1: Core Platform** ✅
- [x] Multi-framework scanning
- [x] Attack simulation engine
- [x] Vulnerability scoring
- [x] Security policy generation

### **Phase 2: Enterprise Features**
- [ ] Multi-cloud support (AWS, GCP, Azure)
- [ ] Real-time monitoring dashboard
- [ ] User authentication & RBAC
- [ ] Audit logging & compliance

### **Phase 3: AI-Powered Security**
- [ ] ML-based attack detection
- [ ] Automated vulnerability discovery
- [ ] Threat intelligence integration
- [ ] Predictive security analysis

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Clone repository
git clone https://github.com/yourusername/ai-sentinels.git
cd ai-sentinels

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Start development server
cd backend
python main.py
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Ollama** - Local LLM platform
- **FastAPI** - Modern Python web framework
- **OpenAI** - API standards and security research
- **Anthropic** - AI safety research
- **HuggingFace** - Open source AI models

## 📞 **Contact**

- **Project Lead**: [Your Name]
- **Email**: [your.email@example.com]
- **Twitter**: [@yourusername]
- **LinkedIn**: [Your LinkedIn]

---

## 🎯 **Hackathon Judges: This is Why We Win**

1. **First-Mover Advantage** - First dedicated AI security platform
2. **Real-World Impact** - Prevents actual AI data breaches
3. **Technical Excellence** - Sophisticated vulnerability scoring
4. **Business Viability** - $5.3B market opportunity
5. **Demo Wow Factor** - Live attack simulation with dramatic results

**AI-Sentinels: Making AI Safe for Enterprise Adoption** 🛡️🚀
