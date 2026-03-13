import os

# Clean CSS content
css_content = """:root {
    --col-bg: #0b0c10;
    --col-bg-alt: #1f2833;
    --col-primary: #45a29e;
    --col-neon: #66fcf1;
    --col-danger: #ff003c;
    --col-warning: #ffb800;
    --col-success: #00ff66;
    --col-text: #c5c6c7;
    --col-text-light: #ffffff;
    --font-heading: 'Fira Code', monospace;
    --font-body: 'Inter', sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--col-bg);
    color: var(--col-text);
    font-family: var(--font-body);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.glow-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle at 50% 50%, rgba(102, 252, 241, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
}

.dashboard-header {
    text-align: center;
    font-family: var(--font-heading);
    padding: 2rem;
    border-bottom: 1px solid rgba(102, 252, 241, 0.2);
}

.dashboard-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.text-neon-blue { color: var(--col-neon); }
.text-neon-red { color: var(--col-danger); }
.subtitle { color: var(--col-primary); font-size: 1rem; }

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
    flex: 1;
}

.panel {
    background: rgba(31, 40, 51, 0.8);
    border: 1px solid rgba(102, 252, 241, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(102, 252, 241, 0.2);
}

.panel-header h2 {
    font-family: var(--font-heading);
    font-size: 1.2rem;
    color: var(--col-text-light);
}

.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--col-success);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.input-group { margin-bottom: 1rem; }
.input-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: var(--col-primary);
    font-size: 0.9rem;
}
.input-group input {
    width: 100%;
    padding: 0.75rem;
    background: rgba(11, 12, 16, 0.8);
    border: 1px solid rgba(102, 252, 241, 0.3);
    border-radius: 6px;
    color: var(--col-text-light);
    font-family: var(--font-body);
}
.input-group input:focus {
    outline: none;
    border-color: var(--col-neon);
    box-shadow: 0 0 10px rgba(102, 252, 241, 0.3);
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    font-family: var(--font-heading);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.btn-primary {
    background: linear-gradient(135deg, var(--col-primary), rgba(69, 162, 158, 0.8));
    color: var(--col-text-light);
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 252, 241, 0.4);
}
.btn-danger {
    background: linear-gradient(135deg, var(--col-danger), rgba(255, 0, 60, 0.8));
    color: var(--col-text-light);
}
.btn-danger:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 0, 60, 0.4);
}
.btn-success {
    background: linear-gradient(135deg, var(--col-success), rgba(0, 255, 102, 0.8));
    color: var(--col-bg);
}
.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
.btn.loading-pulse {
    animation: loading-pulse 1.5s infinite;
}
@keyframes loading-pulse {
    0%, 100% { box-shadow: 0 0 5px var(--col-neon); }
    50% { box-shadow: 0 0 20px var(--col-neon); }
}

.results-container { margin-top: 1.5rem; }
.results-container h3 {
    font-family: var(--font-heading);
    color: var(--col-primary);
    margin-bottom: 1rem;
}
.node-list { list-style: none; }
.node-list li {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: rgba(11, 12, 16, 0.6);
    border: 1px solid rgba(102, 252, 241, 0.2);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.node-list li:hover {
    border-color: var(--col-neon);
    box-shadow: 0 0 10px rgba(102, 252, 241, 0.2);
}
.node-list li.selected {
    border-color: var(--col-neon);
    background: rgba(102, 252, 241, 0.1);
}
.node-list li.empty-state {
    text-align: center;
    color: var(--col-text);
    cursor: default;
    border-style: dashed;
}

.target-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: rgba(11, 12, 16, 0.6);
    border-radius: 6px;
    margin: 1rem 0;
}
.target-display .label { color: var(--col-primary); }
.target-display .value {
    color: var(--col-neon);
    font-weight: 600;
}

.terminal-container {
    margin-top: 1rem;
    background: rgba(11, 12, 16, 0.9);
    border-radius: 8px;
    border: 1px solid rgba(102, 252, 241, 0.2);
    overflow: hidden;
}
.terminal-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(31, 40, 51, 0.8);
    border-bottom: 1px solid rgba(102, 252, 241, 0.2);
}
.terminal-header .dots {
    display: flex;
    gap: 0.25rem;
}
.terminal-header .dots span {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--col-danger);
}
.terminal-header .dots span:nth-child(2) { background: var(--col-warning); }
.terminal-header .dots span:nth-child(3) { background: var(--col-success); }
.terminal-header .title {
    margin-left: 1rem;
    font-family: var(--font-heading);
    font-size: 0.8rem;
    color: var(--col-text);
}
.terminal-body {
    padding: 1rem;
    font-family: var(--font-heading);
    font-size: 0.9rem;
    min-height: 150px;
    max-height: 300px;
    overflow-y: auto;
}
.terminal-body p {
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.badge {
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-family: var(--font-heading);
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
}
.badge-safe {
    background: var(--col-success);
    color: var(--col-bg);
}
.badge-warning {
    background: var(--col-warning);
    color: var(--col-bg);
}
.badge-danger {
    background: var(--col-danger);
    color: var(--col-text-light);
}

.risk-assessment {
    padding: 1rem;
    background: rgba(11, 12, 16, 0.6);
    border-radius: 6px;
    margin-bottom: 1rem;
}
.risk-assessment p { color: var(--col-text); }

.fix-controls {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}
.select-css {
    padding: 0.75rem;
    background: rgba(11, 12, 16, 0.8);
    border: 1px solid rgba(102, 252, 241, 0.3);
    border-radius: 6px;
    color: var(--col-text-light);
    font-family: var(--font-body);
    flex: 1;
    min-width: 200px;
}

.code-container {
    background: rgba(11, 12, 16, 0.9);
    border-radius: 8px;
    border: 1px solid rgba(102, 252, 241, 0.2);
    overflow: hidden;
}
.code-container pre {
    padding: 1rem;
    overflow-x: auto;
    font-family: var(--font-heading);
    font-size: 0.85rem;
    line-height: 1.5;
}
.code-container code { color: var(--col-neon); }

@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
        padding: 1rem;
    }
    .dashboard-header h1 { font-size: 1.8rem; }
    .fix-controls { flex-direction: column; }
}
"""

# Write the clean CSS file
frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'styles.css')
with open(frontend_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print(f"✅ CSS file fixed: {frontend_path}")
print(f"📊 File size: {len(css_content)} characters")
