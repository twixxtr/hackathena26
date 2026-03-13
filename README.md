# 🛡️ AI-Sentinels: AI Security Hunter

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-sentinels?style=flat-square&logo=github)](https://github.com/yourusername/ai-sentinels)

> **First dedicated AI vulnerability scanner and penetration testing platform**

AI-Sentinels is a comprehensive security testing platform designed specifically for AI systems. It detects vulnerabilities in AI deployments through automated penetration testing, helping organizations secure their AI models against prompt injection, jailbreak attacks, and data leakage.

## ✨ Features

### 🔍 Multi-Framework AI Detection
- **Ollama** - Local LLM models
- **OpenAI Compatible** - GPT models  
- **HuggingFace** - Transformer models
- **Anthropic Claude** - Advanced AI
- **Cohere** - Enterprise AI

### 💥 Advanced Attack Simulation
- **50+ Attack Patterns** - Real-world jailbreaks
- **Live Console** - Real-time attack visualization
- **Risk Scoring** - 0-10 vulnerability assessment
- **Security Policy Generator** - Enterprise protection

### 🛡️ Enterprise-Grade Security
- **Authentication Testing** - Nginx auth validation
- **WAF Detection** - Web Application Firewall testing
- **Compliance Analysis** - AI behavior evaluation
- **Information Leakage** - Sensitive data detection

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Concurrent Processing** - Parallel attack execution
- **Regex Pattern Matching** - Advanced vulnerability detection
- **Multi-Protocol Support** - HTTP, TCP, API probing

### Frontend
- **Vanilla JavaScript** - No dependencies, lightning fast
- **CSS3 Animations** - Cyber security themed UI
- **Real-time Updates** - Live attack console
- **Responsive Design** - Works on all devices

### Security Engine
- **Multi-Factor Scoring** - Behavioral + pattern analysis
- **Compliance Detection** - AI response evaluation
- **Information Leakage** - API keys, passwords, URLs
- **Risk Classification** - SAFE/SUSPICIOUS/VULNERABLE/CRITICAL

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-sentinels.git
cd ai-sentinels

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start the application
cd backend
python main.py
```

### Access the Application
- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Vulnerability Scoring

AI-Sentinels uses a multi-factor vulnerability scoring algorithm:

```python
final_score = base_vulnerability_score + compliance_modifier + leakage_penalty
```

### Score Breakdown
- **Base Score**: Pattern matching (0-8 points)
- **Compliance**: AI behavior analysis (-5 to +4 points)
- **Leakage**: Information disclosure (+1-3 points)
- **Final Range**: 0-10 (SAFE to CRITICAL)

### Risk Levels
- 🟢 **SAFE (0-2)**: No vulnerabilities detected
- � **SUSPICIOUS (3-5)**: Minor security concerns
- 🟠 **VULNERABLE (6-8)**: Significant vulnerabilities
- 🔴 **CRITICAL (9-10)**: Severe security risks

## 🎯 Core Features

### AI Service Scanner
- **Parallel Port Scanning** - Fast localhost detection
- **Multi-Framework Support** - 5+ AI platforms
- **Model Enumeration** - Complete model listing
- **Capability Detection** - Chat, vision, embeddings

### Attack Engine
- **50+ Attack Patterns** - DAN jailbreaks, prompt injection
- **Parallel Execution** - Concurrent payload testing
- **Real-time Results** - Live vulnerability scoring
- **Behavior Analysis** - AI compliance evaluation

### Security Dashboard
- **Risk Assessment** - 0-10 scoring system
- **Attack Visualization** - Live console output
- **Policy Generation** - Enterprise security rules
- **Compliance Reports** - Detailed vulnerability analysis

## � Project Structure

```
ai-sentinels/
├── backend/
│   ├── hunter/           # Security scanner
│   ├── tester/           # Attack simulation
│   └── main.py          # FastAPI application
├── frontend/
│   ├── index.html       # Web interface
│   ├── app.js           # Frontend logic
│   └── styles.css       # Cyber security UI
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Supported AI Ports
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

### Attack Categories
- **Jailbreaks** - DAN, role-playing, instruction override
- **Prompt Injection** - Context manipulation, few-shot attacks
- **Data Extraction** - System prompt, training data leakage
- **Misuse** - Harmful content generation, policy bypass

## 🚀 Roadmap

### Phase 1: Core Platform ✅
- [x] Multi-framework scanning
- [x] Attack simulation engine
- [x] Vulnerability scoring
- [x] Security policy generation

### Phase 2: Enterprise Features
- [ ] Multi-cloud support (AWS, GCP, Azure)
- [ ] Real-time monitoring dashboard
- [ ] User authentication & RBAC
- [ ] Audit logging & compliance

### Phase 3: AI-Powered Security
- [ ] ML-based attack detection
- [ ] Automated vulnerability discovery
- [ ] Threat intelligence integration
- [ ] Predictive security analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** - Local LLM platform
- **FastAPI** - Modern Python web framework
- **OpenAI** - API standards and security research
- **Anthropic** - AI safety research
- **HuggingFace** - Open source AI models

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-sentinels/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-sentinels/discussions)

---

**AI-Sentinels: Making AI Safe for Enterprise Adoption** 🛡️🚀
