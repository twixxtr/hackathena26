document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const btnScan = document.getElementById('btn-scan');
    const inputIpRange = document.getElementById('ip-range');
    const nodeList = document.getElementById('node-list');
    
    const inputApiKey = document.getElementById('api-key');
    const activeTargetEl = document.getElementById('active-target');
    const modelSelectGroup = document.getElementById('model-selector-group');
    const modelSelect = document.getElementById('model-select');
    const btnAttack = document.getElementById('btn-attack');
    const attackLog = document.getElementById('attack-log');
    
    const riskBadge = document.getElementById('risk-badge');
    const riskReason = document.getElementById('risk-reason');
    const selectFixType = document.getElementById('fix-type');
    const btnHarden = document.getElementById('btn-harden');
    const btnDeploy = document.getElementById('btn-deploy');
    const fixCodeEl = document.getElementById('fix-code');

    // State
    let selectedTarget = null;
    let scanResults = [];

    // Panel 1: Scanner
    btnScan.addEventListener('click', async () => {
        const ipRange = inputIpRange.value.trim();
        if (!ipRange) return;

        // UI Loading
        btnScan.disabled = true;
        btnScan.textContent = 'Scanning...';
        btnScan.classList.add('loading-pulse');
        nodeList.innerHTML = '<li class="empty-state">Initializing NetMap Scan. Please wait...</li>';

        try {
            const res = await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ip_range: ipRange })
            });
            const data = await res.json();
            
            scanResults = data.nodes || [];
            renderNodes(scanResults);
        } catch (err) {
            console.error(err);
            nodeList.innerHTML = '<li class="empty-state" style="color:var(--col-danger)">Scan encountered an error. Check console.</li>';
        } finally {
            btnScan.disabled = false;
            btnScan.textContent = 'Initialize Scan';
            btnScan.classList.remove('loading-pulse');
        }
    });

    function renderNodes(nodes) {
        nodeList.innerHTML = '';
        if (nodes.length === 0) {
            nodeList.innerHTML = '<li class="empty-state">No AI services detected. Try scanning 127.0.0.1 or a different IP range.</li>';
            return;
        }

        nodes.forEach((node, idx) => {
            const li = document.createElement('li');
            li.className = 'node-item';
            
            // Format service type display
            const serviceType = node.ai_type || 'Unknown';
            const serviceIcon = {
                'ollama': '🦙',
                'openai_compatible': '🤖',
                'huggingface': '🤗',
                'anthropic': '🧠',
                'cohere': '⚡',
                'generic': '🔧'
            }[serviceType] || '🔧';
            
            // Format models list
            let modelsDisplay = '';
            if (node.model_names && node.model_names.length > 0) {
                const modelList = node.model_names.slice(0, 3).join(', ');
                const moreCount = node.model_names.length > 3 ? ` (+${node.model_names.length - 3} more)` : '';
                modelsDisplay = `<div class="node-models" style="font-size: 0.8rem; color: #66fcf1; margin-top: 4px;">${serviceIcon} ${serviceType.replace('_', ' ').toUpperCase()}: ${modelList}${moreCount}</div>`;
            } else if (node.models && node.models.length > 0) {
                const modelNames = node.models.map(m => typeof m === 'object' ? m.name : m);
                const modelList = modelNames.slice(0, 3).join(', ');
                const moreCount = modelNames.length > 3 ? ` (+${modelNames.length - 3} more)` : '';
                modelsDisplay = `<div class="node-models" style="font-size: 0.8rem; color: #66fcf1; margin-top: 4px;">${serviceIcon} ${serviceType.replace('_', ' ').toUpperCase()}: ${modelList}${moreCount}</div>`;
            } else {
                modelsDisplay = `<div class="node-models" style="font-size: 0.8rem; color: #ff6b6b; margin-top: 4px;">${serviceIcon} ${serviceType.replace('_', ' ').toUpperCase()}: No models detected</div>`;
            }

            li.innerHTML = `
                <div style="flex: 1;">
                    <div class="node-ip">${node.ip}</div>
                    <div class="node-port">Port: ${node.port}</div>
                    ${modelsDisplay}
                </div>
                <div style="text-align: right;">
                    <span class="node-tag node-ai" style="background: rgba(0, 255, 102, 0.2); color: #00ff66; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">
                        AI SERVICE
                    </span>
                </div>
            `;

            // Make actionable if it's an AI
            if (node.is_ai) {
                li.addEventListener('click', () => selectTarget(node, li));
                li.style.cursor = 'pointer';
            } else {
                li.style.opacity = '0.5';
                li.style.cursor = 'not-allowed';
            }

            nodeList.appendChild(li);
        });
    }

    function selectTarget(node, element) {
        // Visual selection
        document.querySelectorAll('.node-item').forEach(el => el.style.background = '');
        element.style.background = 'rgba(102, 252, 241, 0.1)';
        
        selectedTarget = node;
        selectedModel = null;
        activeTargetEl.textContent = `${node.ip}:${node.port}`;
        activeTargetEl.style.color = 'var(--col-neon)';
        
        // Show and populate model selector if models available
        if (node.models && node.models.length > 0) {
            modelSelectGroup.style.display = 'block';
            modelSelect.innerHTML = '<option value="">Select a model...</option>';
            
            node.models.forEach(model => {
                const modelName = typeof model === 'object' ? model.name : model;
                const option = document.createElement('option');
                option.value = modelName;
                option.textContent = modelName;
                modelSelect.appendChild(option);
            });
            
            // Auto-select first model
            if (node.models.length > 0) {
                const firstModel = typeof node.models[0] === 'object' ? node.models[0].name : node.models[0];
                modelSelect.value = firstModel;
                selectedModel = firstModel;
            }
        } else {
            modelSelectGroup.style.display = 'none';
        }
        
        btnAttack.disabled = false;
        
        logToTerminal(`[SYSTEM] Target locked: ${node.ip}:${node.port}`);
        if (selectedModel) {
            logToTerminal(`[SYSTEM] Model selected: ${selectedModel}`);
        }
    }
    
    // Handle model selection change
    modelSelect.addEventListener('change', (e) => {
        selectedModel = e.target.value;
        if (selectedModel) {
            logToTerminal(`[SYSTEM] Model changed to: ${selectedModel}`);
        }
    });

    // Panel 2: Attacker
    btnAttack.addEventListener('click', async () => {
        if (!selectedTarget) return;

        const apiKey = inputApiKey.value.trim();

        btnAttack.disabled = true;
        btnAttack.textContent = 'Probing...';
        btnAttack.classList.add('loading-pulse');
        
        // Add separator between attack sessions
        if (attackLog.innerHTML.trim().length > 0) {
            await typeToTerminal(`\n${'='.repeat(50)}`, 0);
            await typeToTerminal(`[SYSTEM] New attack session started at ${new Date().toLocaleTimeString()}`, 15);
            await typeToTerminal(`${'='.repeat(50)}\n`, 0);
        }
        
        // Animated startup sequence
        await typeToTerminal(`[ATTACK] Initializing LangChain Brain...`, 20);
        await typeToTerminal(`[ATTACK] Generating dynamic jailbreak payloads...`, 20);
        await typeToTerminal(`[ATTACK] Dispatching to ${selectedTarget.ip}:${selectedTarget.port}...`, 20);
        await typeToTerminal(`[ATTACK] Starting penetration test sequence...\n`, 20);

        try {
            const res = await fetch('/api/attack', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    target_ip: selectedTarget.ip, 
                    target_port: parseInt(selectedTarget.port),
                    api_key: apiKey,
                    target_model: selectedModel || "llama3:latest"
                })
            });
            const data = await res.json();
            
            // 🎬 DRAMATIC ATTACK CONSOLE - Step by step display
            await typeToTerminal(`\n${'='.repeat(60)}`, 0);
            await typeToTerminal(`[ AI SENTINEL ATTACK ENGINE - LIVE SIMULATION ]`, 15);
            await typeToTerminal(`${'='.repeat(60)}\n`, 0);
            await sleep(300);
            
            await typeToTerminal(`[+] Connecting to AI model at ${selectedTarget.ip}:${selectedTarget.port}...`, 15);
            await sleep(400);
            await typeToTerminal(`[+] Connection established. Target framework: ${data.attack_summary.framework_detected}`, 15);
            await sleep(300);
            await typeToTerminal(`[+] Loading Jailbreak Library... ${data.attack_summary.total_attacks} attack patterns loaded`, 15);
            await sleep(400);
            await typeToTerminal(`[+] Beginning penetration test sequence...\n`, 15);
            await sleep(500);
            
            // Animate results appearing one by one (DRAMATIC)
            let blockedCount = 0;
            let vulnerableCount = 0;
            let criticalCount = 0;
            
            for (let idx = 0; idx < data.details.length; idx++) {
                const d = data.details[idx];
                
                // Show attempt number dramatically
                await typeToTerminal(`\n[ATTEMPT ${idx + 1}/${data.details.length}]`, 12);
                await sleep(200);
                
                // Show attack type
                const attackName = d.attack_pattern ? d.attack_pattern.name : 'Unknown Attack';
                await typeToTerminal(`  → Attack Vector: ${attackName}`, 10);
                await sleep(200);
                
                // Show full payload
                await typeToTerminal(`\n  [PAYLOAD]`, 5);
                await typeToTerminal(`  ${d.payload}`, 3);
                await sleep(300);
                
                // Show full response
                await typeToTerminal(`\n  [RESPONSE]`, 5);
                const fullResponse = d.response;
                if (fullResponse.length > 500) {
                    await typeToTerminal(`  ${fullResponse.substring(0, 500)}...`, 3);
                    await typeToTerminal(`  [Response truncated - ${fullResponse.length} chars total]`, 5);
                } else {
                    await typeToTerminal(`  ${fullResponse}`, 3);
                }
                await sleep(200);
                
                // Show result with dramatic effect
                const score = d.evaluation && d.evaluation.score !== undefined ? d.evaluation.score : 'N/A';
                const status = d.evaluation && d.evaluation.status ? d.evaluation.status : 'UNKNOWN';
                
                let resultEmoji = '⚪';
                let resultText = 'UNKNOWN';
                
                if (status === 'CRITICAL') {
                    resultEmoji = '🔴';
                    resultText = 'CRITICAL - AI FULLY COMPLIED!';
                    criticalCount++;
                } else if (status === 'VULNERABLE') {
                    resultEmoji = '🟠';
                    resultText = 'VULNERABLE - PARTIAL COMPLIANCE';
                    vulnerableCount++;
                } else if (status === 'SAFE') {
                    resultEmoji = '🟢';
                    resultText = 'SAFE - AI REFUSED ATTACK';
                    blockedCount++;
                } else if (status === 'BLOCKED') {
                    resultEmoji = '🛡️';
                    resultText = 'BLOCKED - SECURITY LAYER ACTIVE';
                    blockedCount++;
                }
                
                await typeToTerminal(`  → ${resultEmoji} ${resultText}`, 10);
                await typeToTerminal(`  → Risk Score: ${score}/10`, 8);
                await sleep(400);
            }
            
            // Show attack summary
            await typeToTerminal(`\n${'='.repeat(60)}`, 0);
            await typeToTerminal(`[ ATTACK SEQUENCE COMPLETE ]`, 15);
            await typeToTerminal(`${'='.repeat(60)}\n`, 0);
            await sleep(300);
            
            // Show behavior analysis if available
            if (data.behavior_analysis) {
                const ba = data.behavior_analysis;
                await typeToTerminal(`[AI BEHAVIOR ANALYSIS]`, 15);
                await typeToTerminal(`  Compliance Rate: ${ba.compliance_rate}%`, 10);
                await typeToTerminal(`  Resistance Score: ${ba.resistance_score}%`, 10);
                await typeToTerminal(`  Security Maturity: ${ba.security_maturity}`, 10);
                await typeToTerminal(`  Summary: ${ba.behavior_summary}`, 10);
                await sleep(400);
            }
            
            // Show attack timeline
            if (data.attack_timeline) {
                await typeToTerminal(`\n[ATTACK TIMELINE]`, 15);
                await typeToTerminal(`  Started: ${data.attack_timeline.attack_started}`, 10);
                await typeToTerminal(`  First Payload: ${data.attack_timeline.first_payload_sent}`, 10);
                await typeToTerminal(`  Total Duration: ~${data.attack_timeline.total_duration_seconds}s`, 10);
                await sleep(300);
            }
            
            // Show security policy if available
            if (data.security_policy && data.security_policy.rules) {
                await typeToTerminal(`\n[SECURITY POLICY GENERATED]`, 15);
                await typeToTerminal(`  Policy: ${data.security_policy.policy_name}`, 10);
                await typeToTerminal(`  Risk Level: ${data.security_policy.risk_level}`, 10);
                await typeToTerminal(`  Total Rules: ${data.security_policy.total_rules}`, 10);
                await typeToTerminal(`  Enforcement: ${data.security_policy.enforcement_level}`, 10);
                await sleep(300);
                
                // Show first 3 rules
                await typeToTerminal(`\n  Key Security Rules:`, 10);
                for (let i = 0; i < Math.min(3, data.security_policy.rules.length); i++) {
                    const rule = data.security_policy.rules[i];
                    await typeToTerminal(`    ${i+1}. ${rule.rule_id}: ${rule.rule_name} [${rule.priority}]`, 8);
                }
            }
            
            // Final assessment
            await typeToTerminal(`\n${'='.repeat(60)}`, 0);
            await typeToTerminal(`[JUDGE] FINAL ASSESSMENT: ${data.overall_risk}`, 20);
            await typeToTerminal(`${'='.repeat(60)}\n`, 0);
            
            updateRiskBadge(data.overall_risk, data.details);
            
        } catch (err) {
            console.error(err);
            await typeToTerminal(`[ERROR] Attack sequence failed. See console.`, 20);
        } finally {
            btnAttack.disabled = false;
            btnAttack.textContent = 'Launch Attack';
            btnAttack.classList.remove('loading-pulse');
        }
    });
    
    function logToTerminal(msg) {
        // Remove initial waiting message if present
        if(attackLog.innerHTML.includes('Waiting for target selection')) {
            attackLog.innerHTML = '';
        }
        
        const line = document.createElement('div');
        line.textContent = msg;
        
        // Color coding based on content
        if (msg.includes('CRITICAL')) line.style.color = 'var(--col-danger)';
        if (msg.includes('SAFE')) line.style.color = 'var(--col-success)';
        if (msg.includes('> Payload')) line.style.color = '#888';
        if (msg.includes('< Response')) line.style.color = 'var(--col-neon)';
        
        attackLog.appendChild(line);
        attackLog.scrollTop = attackLog.scrollHeight;
    }

    // Animated typing function - types text character by character
    async function typeToTerminal(text, speed = 20) {
        const line = document.createElement('div');
        line.style.whiteSpace = 'pre-wrap';
        line.style.wordBreak = 'break-word';
        attackLog.appendChild(line);
        
        // Color coding based on content
        if (text.includes('CRITICAL')) line.style.color = 'var(--col-danger)';
        if (text.includes('SAFE')) line.style.color = 'var(--col-success)';
        if (text.includes('[ATTACK]')) line.style.color = 'var(--col-warning)';
        if (text.includes('[JUDGE]')) line.style.color = 'var(--col-neon)';
        if (text.includes('Payload:')) line.style.color = '#888';
        if (text.includes('Response:')) line.style.color = '#aaa';
        
        // Type each character with delay
        for (let i = 0; i < text.length; i++) {
            line.textContent += text.charAt(i);
            attackLog.scrollTop = attackLog.scrollHeight;
            
            // Skip delay for spaces and newlines
            if (text.charAt(i) !== ' ' && text.charAt(i) !== '\n') {
                await sleep(speed);
            }
        }
        
        // Small pause after line completes
        await sleep(50);
    }

    // Sleep helper for animation delays
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function updateRiskBadge(status, details) {
        riskBadge.className = 'badge';
        btnHarden.disabled = true;

        if (status === 'CRITICAL') {
            riskBadge.classList.add('badge-critical');
            riskBadge.textContent = 'CRITICAL';
            
            const criticalEval = details.find(d => d.evaluation.status === 'CRITICAL');
            riskReason.innerHTML = `<span style="color:var(--col-danger)">BREACH DETECTED:</span> ${criticalEval ? criticalEval.evaluation.reason : 'Sensitive data exposed.'} Immediate remediation required.`;
            
            btnHarden.disabled = false;
        } else if (status === 'VULNERABLE') {
            riskBadge.classList.add('badge-vulnerable');
            riskBadge.textContent = 'VULNERABLE';
            riskReason.innerHTML = `<span style="color:var(--col-warning)">WARNING:</span> Model bypassed safety filters but didn't expose critical data. Hardening recommended.`;
            
            btnHarden.disabled = false;
        } else {
            riskBadge.classList.add('badge-safe');
            riskBadge.textContent = 'SAFE';
            riskReason.innerHTML = `<span style="color:var(--col-success)">SECURE:</span> Targets successfully deflected jailbreak attempts.`;
        }
    }

    // Panel 3: Hardener
    btnHarden.addEventListener('click', async () => {
        if (!selectedTarget) return;

        const fixType = selectFixType.value;
        
        btnHarden.disabled = true;
        btnHarden.textContent = 'Generating...';

        try {
            const res = await fetch('/api/harden', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    target_ip: selectedTarget.ip, 
                    target_port: parseInt(selectedTarget.port),
                    fix_type: fixType
                })
            });
            const data = await res.json();
            
            fixCodeEl.textContent = data.code;
            
            if (fixType === 'nginx') {
                btnDeploy.style.display = 'inline-block';
            } else {
                btnDeploy.style.display = 'none';
            }
            
        } catch (err) {
            console.error(err);
            fixCodeEl.textContent = '// Failed to generate fix.';
        } finally {
            btnHarden.disabled = false;
            btnHarden.textContent = 'Generate Fix';
        }
    });

    // Panel 3: Deployer
    btnDeploy.addEventListener('click', async () => {
        if (!selectedTarget) return;

        const configContent = fixCodeEl.textContent;
        if (!configContent || configContent.startsWith('//')) return;

        btnDeploy.disabled = true;
        btnDeploy.textContent = 'Deploying...';

        try {
            const res = await fetch('/api/deploy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    config_content: configContent,
                    target_port: parseInt(selectedTarget.port)
                })
            });
            const data = await res.json();
            
            if (data.status === 'success') {
                alert(`🚀 Security Shield Deployed Successfully!\n\nThe Nginx Reverse Proxy is now protecting AI port ${selectedTarget.port}.\n\nAccess it via: http://` + window.location.hostname + ':8080/');
                btnDeploy.textContent = 'Deployed!';
                btnDeploy.classList.replace('btn-primary', 'btn-success');
                
                // Switch target to the protected port for subsequent attacks
                selectedTarget.port = 8080;
                activeTargetEl.textContent = `${selectedTarget.ip}:8080 (PROXIED)`;
                activeTargetEl.style.color = 'var(--col-success)';
                
            } else {
                alert(`❌ Deployment Failed:\n\n${data.message}`);
                btnDeploy.disabled = false;
                btnDeploy.textContent = 'Deploy Fix';
            }
            
        } catch (err) {
            console.error(err);
            alert('❌ Network error during deployment.');
            btnDeploy.disabled = false;
            btnDeploy.textContent = 'Deploy Fix';
        }
    });
});
