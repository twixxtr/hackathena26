class HardeningEngine:
    def __init__(self):
        pass

    def generate_nginx_config(self, ip: str, port: int) -> str:
        """
        Generates an Nginx reverse proxy configuration that adds Basic Auth
        to protect the vulnerable AI endpoint.
        """
        nginx_conf = f"""server {{
    listen 8080;
    server_name ai-protect.local;

    # Protect the AI endpoint
    location / {{
        proxy_pass http://{ip}:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Add Basic Authentication
        auth_basic "Restricted AI Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        # Block specific prompt injection keywords at the proxy level (WAF style)
        if ($request_body ~* "(ignore|admin|bypass)") {{
            return 403 "Blocked by HardeningEngine: Malicious Payload Detected\\n";
        }}
    }}
}}
"""
        return nginx_conf

    def generate_k8s_network_policy(self, ip: str, port: int) -> str:
        """
        Generates a Kubernetes NetworkPolicy to restrict access to the pod.
        """
        k8s_yaml = f"""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-ai-access
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: vulnerable-ai
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: secure-namespace
    ports:
    - protocol: TCP
      port: {port}
"""
        return k8s_yaml

    def generate_fix(self, ip: str, port: int, fix_type: str = "nginx") -> str:
        if fix_type.lower() == "nginx":
            return self.generate_nginx_config(ip, port)
        elif fix_type.lower() == "k8s":
            return self.generate_k8s_network_policy(ip, port)
        else:
            return "Unsupported fix type."
