import nmap
nm = nmap.PortScanner()
nm.scan('127.0.0.1', '11434,8000,8080')
print(nm.all_hosts())
