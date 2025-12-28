#!/usr/bin/env python3
"""
OBSIDIAN CHIPER TOOLS v5
Professional Login System
3 Modul: Login • Create Account • Exit
License Key: Hubungi @Zxxtirwd
"""

import os
import sys
import time
import json
import random
import socket
import threading
import hashlib
import sqlite3
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# ==================== ASCII ART ====================
LOGIN_ASCII = """
███████╗██╗██╗      █████╗ ██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗    ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██╔════╝██║██║     ██╔══██╗██║  ██║██║ ██╔╝██╔══██╗████╗  ██║    ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
███████╗██║██║     ███████║███████║█████╔╝ ███████║██╔██╗ ██║    ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
╚════██║██║██║     ██╔══██║██╔══██║██╔═██╗ ██╔══██║██║╚██╗██║    ██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████║██║███████╗██║  ██║██║  ██║██║  ██╗██║  ██║██║ ╚████║    ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
"""

MAIN_ASCII = """
 ██████╗ ██████╗ ███████╗██╗██████╗ ██╗ █████╗ ███╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔═══██╗██╔══██╗██╔════╝██║██╔══██╗██║██╔══██╗████╗  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║   ██║██████╔╝███████╗██║██║  ██║██║███████║██╔██╗ ██║       ██║   ██║   ██║██║   ██║██║     ███████╗
██║   ██║██╔══██╗╚════██║██║██║  ██║██║██╔══██║██║╚██╗██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
╚██████╔╝██████╔╝███████║██║██████╔╝██║██║  ██║██║ ╚████║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
 ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""

WELCOME_ASCII = """
██╗    ██╗███████╗██╗     ██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
"""

# ==================== DATABASE SYSTEM ====================
class Database:
    def __init__(self):
        self.db_file = 'obsidian_users.db'
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.create_tables()
        self.create_default_admin()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                license_key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # License keys table (premium keys)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT UNIQUE NOT NULL,
                created_by TEXT DEFAULT 'system',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                max_users INTEGER DEFAULT 1,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
    
    def create_default_admin(self):
        """Create default admin account if not exists"""
        cursor = self.conn.cursor()
        
        # Check if admin exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            license_key = "obsidian-chiper"  # Default license for admin
            
            cursor.execute(
                "INSERT INTO users (username, password_hash, license_key) VALUES (?, ?, ?)",
                ('admin', password_hash, license_key)
            )
            self.conn.commit()
            print(f"{Fore.GREEN}[+] Default admin account created")
    
    def create_user(self, username, password, license_key):
        """Create new user account"""
        cursor = self.conn.cursor()
        
        # Check if username exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False, "Username already exists"
        
        # Check license key validity
        if not self.validate_license(license_key):
            return False, "Invalid or expired license key"
        
        # Create user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, license_key) VALUES (?, ?, ?)",
                (username, password_hash, license_key)
            )
            self.conn.commit()
            
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?",
                (username,)
            )
            self.conn.commit()
            
            return True, "Account created successfully"
        except Exception as e:
            return False, f"Error creating account: {str(e)}"
    
    def validate_license(self, license_key):
        """Validate license key"""
        cursor = self.conn.cursor()
        
        # Check in licenses table (premium keys)
        cursor.execute(
            "SELECT id FROM licenses WHERE license_key = ? AND status = 'active' AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)",
            (license_key,)
        )
        if cursor.fetchone():
            return True
        
        # Check default license
        if license_key == "obsidian-chiper":
            return True
        
        return False
    
    def authenticate(self, username, password, license_key):
        """Authenticate user login"""
        cursor = self.conn.cursor()
        
        # Get user
        cursor.execute(
            "SELECT id, password_hash, license_key FROM users WHERE username = ? AND status = 'active'",
            (username,)
        )
        user = cursor.fetchone()
        
        if not user:
            return False, "User not found or inactive"
        
        user_id, stored_hash, stored_license = user
        
        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != stored_hash:
            return False, "Invalid password"
        
        # Verify license key
        if license_key != stored_license:
            return False, "License key mismatch"
        
        # Update last login
        cursor.execute(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
            (user_id,)
        )
        self.conn.commit()
        
        # Create session
        session_token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
        
        return True, {
            'user_id': user_id,
            'username': username,
            'session_token': session_token,
            'license_key': stored_license
        }
    
    def get_user_stats(self):
        """Get user statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE last_login IS NOT NULL")
        active_users = cursor.fetchone()[0]
        
        return {
            'total_users': total_users,
            'active_users': active_users
        }

# ==================== LOGIN SYSTEM ====================
class LoginSystem:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.session_data = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_ascii(self, ascii_art, color_effect=True):
        """Display ASCII art with color effect"""
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        lines = ascii_art.strip().split('\n')
        
        for i, line in enumerate(lines):
            if color_effect:
                color = colors[i % len(colors)]
                print(color + line)
                time.sleep(0.02)
            else:
                print(Fore.CYAN + line)
    
    def show_main_menu(self):
        """Display main menu with 3 options"""
        self.clear_screen()
        self.display_ascii(LOGIN_ASCII)
        
        print(f"\n{Fore.CYAN}╔{'═'*60}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'OBSIDIAN CHIPER TOOLS v5 - MAIN MENU':^60}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        print(f"{Fore.CYAN}║{Fore.WHITE}{'Pilih salah satu opsi di bawah ini:':^60}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        print(f"{Fore.CYAN}║ {Fore.GREEN}[1] {Fore.WHITE}Login ke Akun                {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.GREEN}[2] {Fore.WHITE}Buat Akun Baru              {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.RED}[3] {Fore.WHITE}Keluar dari Program         {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*60}╝")
    
    def show_login_form(self):
        """Display login form"""
        self.clear_screen()
        self.display_ascii(LOGIN_ASCII)
        
        print(f"\n{Fore.CYAN}╔{'═'*60}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'LOGIN KE AKUN ANDA':^60}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        
        print(f"{Fore.YELLOW}[+] Default Account:")
        print(f"{Fore.CYAN}   Username: admin")
        print(f"{Fore.CYAN}   Password: admin123")
        print(f"{Fore.CYAN}   License: obsidian-chiper")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        
        attempts = 3
        while attempts > 0:
            print(f"\n{Fore.CYAN}┌{'─'*40}┐")
            username = input(f"{Fore.YELLOW}│ Username: {Fore.WHITE}").strip()
            password = input(f"{Fore.YELLOW}│ Password: {Fore.WHITE}")
            license_key = input(f"{Fore.YELLOW}│ License Key: {Fore.WHITE}").strip()
            print(f"{Fore.CYAN}└{'─'*40}┘")
            
            if not username or not password or not license_key:
                print(f"{Fore.RED}[!] Semua field harus diisi!")
                attempts -= 1
                print(f"{Fore.YELLOW}[!] Percobaan tersisa: {attempts}")
                continue
            
            # Authenticate
            success, result = self.db.authenticate(username, password, license_key)
            
            if success:
                self.current_user = username
                self.session_data = result
                
                print(f"\n{Fore.GREEN}[✓] Login berhasil!")
                print(f"{Fore.CYAN}[+] Selamat datang, {username}!")
                time.sleep(2)
                return True
            else:
                attempts -= 1
                print(f"\n{Fore.RED}[!] {result}")
                print(f"{Fore.YELLOW}[!] Percobaan tersisa: {attempts}")
                time.sleep(1)
        
        print(f"\n{Fore.RED}[!] Terlalu banyak percobaan gagal!")
        print(f"{Fore.YELLOW}[!] Silakan coba lagi nanti.")
        time.sleep(2)
        return False
    
    def show_create_account_form(self):
        """Display account creation form"""
        self.clear_screen()
        self.display_ascii(LOGIN_ASCII)
        
        print(f"\n{Fore.CYAN}╔{'═'*60}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'BUAT AKUN BARU':^60}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        
        print(f"{Fore.YELLOW}[+] Informasi Penting:")
        print(f"{Fore.CYAN}   1. Username harus unik")
        print(f"{Fore.CYAN}   2. Password minimal 6 karakter")
        print(f"{Fore.CYAN}   3. License key wajib dimiliki")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        
        print(f"\n{Fore.RED}[!] CARA DAPATKAN LICENSE KEY:")
        print(f"{Fore.YELLOW}[+] 1. Beli license key dari @Zxxtirwd di Telegram")
        print(f"{Fore.YELLOW}[+] 2. Hubungi WhatsApp: +62 812-XXXX-XXXX")
        print(f"{Fore.YELLOW}[+] 3. Harga: Rp 30.000 - Rp 50.000")
        print(f"{Fore.YELLOW}[+] 4. License berlaku seumur hidup + update")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        
        print(f"\n{Fore.YELLOW}[+] Test License (hanya untuk testing):")
        print(f"{Fore.CYAN}   License Key: obsidian-chiper")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        
        while True:
            print(f"\n{Fore.CYAN}┌{'─'*40}┐")
            username = input(f"{Fore.YELLOW}│ Username Baru: {Fore.WHITE}").strip()
            password = input(f"{Fore.YELLOW}│ Password Baru: {Fore.WHITE}")
            confirm_pass = input(f"{Fore.YELLOW}│ Konfirmasi Password: {Fore.WHITE}")
            license_key = input(f"{Fore.YELLOW}│ License Key: {Fore.WHITE}").strip()
            print(f"{Fore.CYAN}└{'─'*40}┘")
            
            # Validation
            if not username or not password or not confirm_pass or not license_key:
                print(f"{Fore.RED}[!] Semua field harus diisi!")
                continue
            
            if len(username) < 3:
                print(f"{Fore.RED}[!] Username minimal 3 karakter")
                continue
            
            if len(password) < 6:
                print(f"{Fore.RED}[!] Password minimal 6 karakter")
                continue
            
            if password != confirm_pass:
                print(f"{Fore.RED}[!] Password tidak cocok!")
                continue
            
            # Check license key
            if license_key == "obsidian-chiper":
                print(f"{Fore.YELLOW}[!] Ini license key untuk testing")
                print(f"{Fore.YELLOW}[!] Untuk full version, beli license asli")
            
            # Create account
            success, message = self.db.create_user(username, password, license_key)
            
            if success:
                print(f"\n{Fore.GREEN}[✓] {message}")
                print(f"{Fore.CYAN}[+] Username: {username}")
                print(f"{Fore.CYAN}[+] License: {license_key}")
                print(f"{Fore.YELLOW}[+] Silakan login dengan akun baru Anda")
                time.sleep(3)
                return True
            else:
                print(f"\n{Fore.RED}[!] {message}")
                
                retry = input(f"\n{Fore.YELLOW}[?] Coba lagi? (y/n): {Fore.WHITE}").lower()
                if retry != 'y':
                    return False
    
    def show_welcome_screen(self):
        """Display welcome screen after login"""
        self.clear_screen()
        self.display_ascii(WELCOME_ASCII)
        
        session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{Fore.CYAN}╔{'═'*60}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'SELAMAT DATANG DI OBSIDIAN TOOLS':^60}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═'*60}╣")
        print(f"{Fore.CYAN}║ {Fore.GREEN}User:{Fore.WHITE} {self.current_user:<48} {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.GREEN}Login Time:{Fore.WHITE} {session_time:<45} {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.GREEN}License:{Fore.WHITE} {self.session_data['license_key']:<46} {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.GREEN}Session ID:{Fore.WHITE} {self.session_data['session_token'][:16]:<43} {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*60}╝")
        
        # User statistics
        stats = self.db.get_user_stats()
        print(f"\n{Fore.YELLOW}[+] System Statistics:")
        print(f"{Fore.CYAN}   • Total Users: {stats['total_users']}")
        print(f"{Fore.CYAN}   • Active Users: {stats['active_users']}")
        
        print(f"\n{Fore.GREEN}[+] Tools yang tersedia:")
        print(f"{Fore.CYAN}   1. DDoS Protection Tester")
        print(f"{Fore.CYAN}   2. Advanced Dorking Tools")
        print(f"{Fore.CYAN}   3. IP Address Tracker")
        print(f"{Fore.CYAN}   4. Vulnerability Scanner")
        print(f"{Fore.CYAN}   5. Network Pentest Tools")
        
        print(f"\n{Fore.YELLOW}[+] Selamat menikmati, {self.current_user}!")
        time.sleep(3)
    
    def run(self):
        """Main login system loop"""
        while True:
            self.show_main_menu()
            
            choice = input(f"\n{Fore.YELLOW}[?] Pilih opsi (1-3): {Fore.WHITE}").strip()
            
            if choice == "1":
                # Login
                if self.show_login_form():
                    self.show_welcome_screen()
                    return True  # Login successful
                
            elif choice == "2":
                # Create account
                self.show_create_account_form()
                
            elif choice == "3":
                # Exit
                self.clear_screen()
                print(f"\n{Fore.CYAN}╔{'═'*60}╗")
                print(f"{Fore.CYAN}║{Fore.YELLOW}{'TERIMA KASIH TELAH MENGGUNAKAN':^60}{Fore.CYAN}║")
                print(f"{Fore.CYAN}║{Fore.WHITE}{'OBSIDIAN CHIPER TOOLS v5':^60}{Fore.CYAN}║")
                print(f"{Fore.CYAN}╠{'═'*60}╣")
                print(f"{Fore.CYAN}║ {Fore.YELLOW}Contact untuk support & license:        {Fore.CYAN}║")
                print(f"{Fore.CYAN}║ {Fore.WHITE}Telegram: @Zxxtirwd                   {Fore.CYAN}║")
                print(f"{Fore.CYAN}║ {Fore.WHITE}WhatsApp: +62 812-XXXX-XXXX           {Fore.CYAN}║")
                print(f"{Fore.CYAN}╚{'═'*60}╝")
                time.sleep(3)
                return False
                
            else:
                print(f"{Fore.RED}[!] Pilihan tidak valid!")
                time.sleep(1)

# ==================== MAIN TOOLS SYSTEM ====================
class ObsidianTools:
    """Main tools system after login"""
    
    def __init__(self, username, session_data):
        self.username = username
        self.session_data = session_data
        self.modules = {
            'ddos': self.ddos_module,
            'dorking': self.dorking_module,
            'iptracker': self.ip_tracker_module,
            'vulnscan': self.vuln_scan_module,
            'pentest': self.pentest_module
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_main_tools(self):
        """Display main tools menu"""
        self.clear_screen()
        
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        lines = MAIN_ASCII.strip().split('\n')
        
        for i, line in enumerate(lines):
            color = colors[i % len(colors)]
            print(color + line)
            time.sleep(0.01)
        
        session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'OBSIDIAN CHIPER TOOLS v5 - MAIN DASHBOARD':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═'*70}╣")
        print(f"{Fore.CYAN}║ {Fore.GREEN}User:{Fore.WHITE} {self.username:<58} {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.GREEN}License:{Fore.WHITE} {self.session_data['license_key']:<56} {Fore.CYAN}║")
        print(f"{Fore.CYAN}║ {Fore.GREEN}Session:{Fore.WHITE} {session_time:<54} {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
    
    def show_tools_menu(self):
        """Display tools selection menu"""
        menu = f"""
{Fore.YELLOW}[+] PILIH TOOLS YANG MAU DIPAKAI:

{Fore.CYAN}[1] {Fore.WHITE}⚡ DDoS PROTECTION TESTER
{Fore.GREEN}    • Test ketahanan server terhadap serangan DDoS
{Fore.GREEN}    • HTTP Load Testing dengan proxy rotation
{Fore.GREEN}    • Slowloris attack simulation
{Fore.GREEN}    • Professional reporting system

{Fore.CYAN}[2] {Fore.WHITE}🔍 ADVANCED DORKING TOOLS
{Fore.GREEN}    • Google Dork Search real-time
{Fore.GREEN}    • Automated vulnerability scanning
{Fore.GREEN}    • Multiple dork patterns database
{Fore.GREEN}    • Results export to JSON/CSV

{Fore.CYAN}[3] {Fore.WHITE}📍 IP ADDRESS TRACKER
{Fore.GREEN}    • IP geolocation with multiple APIs
{Fore.GREEN}    • Deep analysis & port scanning
{Fore.GREEN}    • WHOIS information lookup
{Fore.GREEN}    • Reputation checking system

{Fore.CYAN}[4] {Fore.WHITE}🛡️ VULNERABILITY SCANNER
{Fore.GREEN}    • Website security scanning
{Fore.GREEN}    • SQL Injection & XSS detection
{Fore.GREEN}    • Security headers analysis
{Fore.GREEN}    • SSL certificate checking

{Fore.CYAN}[5] {Fore.WHITE}🔧 NETWORK PENTEST TOOLS
{Fore.GREEN}    • Port scanning & service detection
{Fore.GREEN}    • Network reconnaissance
{Fore.GREEN}    • Packet crafting utilities
{Fore.GREEN}    • Exploit database integration

{Fore.CYAN}[6] {Fore.WHITE}📊 ACCOUNT & SETTINGS
{Fore.GREEN}    • View account information
{Fore.GREEN}    • License management
{Fore.GREEN}    • System configuration
{Fore.GREEN}    • Update checking

{Fore.RED}[0] {Fore.WHITE}🚪 LOGOUT & KELUAR
"""
        print(menu)
    
    def run_tools(self):
        """Run main tools system"""
        while True:
            self.display_main_tools()
            self.show_tools_menu()
            
            choice = input(f"\n{Fore.YELLOW}[?] Pilih tools (0-6): {Fore.WHITE}").strip()
            
            if choice == "1":
                self.ddos_module()
            elif choice == "2":
                self.dorking_module()
            elif choice == "3":
                self.ip_tracker_module()
            elif choice == "4":
                self.vuln_scan_module()
            elif choice == "5":
                self.pentest_module()
            elif choice == "6":
                self.account_settings()
            elif choice == "0":
                print(f"\n{Fore.GREEN}[+] Logging out...")
                time.sleep(2)
                return
            else:
                print(f"{Fore.RED}[!] Pilihan tidak valid!")
                time.sleep(1)
    
    def ddos_module(self):
        """DDoS Protection Tester module"""
        self.clear_screen()
        print(f"{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'DDoS PROTECTION TESTER':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
        
        print(f"\n{Fore.YELLOW}[+] Fitur ini dalam pengembangan...")
        print(f"{Fore.CYAN}[+] Akan segera tersedia di update berikutnya")
        print(f"{Fore.GREEN}[+] Contact @Zxxtirwd untuk info update")
        
        input(f"\n{Fore.YELLOW}[!] Press Enter to continue...")
    
    def dorking_module(self):
        """Dorking Tools module"""
        self.clear_screen()
        print(f"{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'ADVANCED DORKING TOOLS':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
        
        print(f"\n{Fore.YELLOW}[+] Fitur ini dalam pengembangan...")
        print(f"{Fore.CYAN}[+] Akan segera tersedia di update berikutnya")
        print(f"{Fore.GREEN}[+] Contact @Zxxtirwd untuk info update")
        
        input(f"\n{Fore.YELLOW}[!] Press Enter to continue...")
    
    def ip_tracker_module(self):
        """IP Tracker module"""
        self.clear_screen()
        print(f"{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'IP ADDRESS TRACKER':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
        
        print(f"\n{Fore.YELLOW}[+] Fitur ini dalam pengembangan...")
        print(f"{Fore.CYAN}[+] Akan segera tersedia di update berikutnya")
        print(f"{Fore.GREEN}[+] Contact @Zxxtirwd untuk info update")
        
        input(f"\n{Fore.YELLOW}[!] Press Enter to continue...")
    
    def vuln_scan_module(self):
        """Vulnerability Scanner module"""
        self.clear_screen()
        print(f"{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'VULNERABILITY SCANNER':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
        
        print(f"\n{Fore.YELLOW}[+] Fitur ini dalam pengembangan...")
        print(f"{Fore.CYAN}[+] Akan segera tersedia di update berikutnya")
        print(f"{Fore.GREEN}[+] Contact @Zxxtirwd untuk info update")
        
        input(f"\n{Fore.YELLOW}[!] Press Enter to continue...")
    
    def pentest_module(self):
        """Pentest Tools module"""
        self.clear_screen()
        print(f"{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'NETWORK PENTEST TOOLS':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
        
        print(f"\n{Fore.YELLOW}[+] Fitur ini dalam pengembangan...")
        print(f"{Fore.CYAN}[+] Akan segera tersedia di update berikutnya")
        print(f"{Fore.GREEN}[+] Contact @Zxxtirwd untuk info update")
        
        input(f"\n{Fore.YELLOW}[!] Press Enter to continue...")
    
    def account_settings(self):
        """Account settings module"""
        self.clear_screen()
        print(f"{Fore.CYAN}╔{'═'*70}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'ACCOUNT SETTINGS':^70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚{'═'*70}╝")
        
        print(f"\n{Fore.YELLOW}[+] Informasi Akun:")
        print(f"{Fore.CYAN}   • Username: {self.username}")
        print(f"{Fore.CYAN}   • License Key: {self.session_data['license_key']}")
        print(f"{Fore.CYAN}   • User ID: {self.session_data['user_id']}")
        print(f"{Fore.CYAN}   • Session: {self.session_data['session_token'][:16]}...")
        
        print(f"\n{Fore.YELLOW}[+] Upgrade License:")
        print(f"{Fore.CYAN}   • License saat ini: Basic")
        print(f"{Fore.CYAN}   • Upgrade ke Premium: Rp 50.000")
        print(f"{Fore.CYAN}   • Fitur Premium:")
        print(f"{Fore.CYAN}     - Akses semua tools")
        print(f"{Fore.CYAN}     - Update lifetime")
        print(f"{Fore.CYAN}     - Priority support")
        print(f"{Fore.CYAN}     - Custom features")
        
        print(f"\n{Fore.YELLOW}[+] Contact untuk upgrade:")
        print(f"{Fore.CYAN}   • Telegram: @Zxxtirwd")
        print(f"{Fore.CYAN}   • WhatsApp: +62 812-XXXX-XXXX")
        
        input(f"\n{Fore.YELLOW}[!] Press Enter to continue...")

# ==================== MAIN APPLICATION ====================
def main():
    """Main application entry point"""
    print(f"{Fore.CYAN}[+] Starting Obsidian Chiper Tools v5...")
    time.sleep(1)
    
    # Create login system
    login_system = LoginSystem()
    
    # Run login system
    if login_system.run():
        # Login successful, start tools
        tools = ObsidianTools(
            login_system.current_user,
            login_system.session_data
        )
        tools.run_tools()
    
    print(f"\n{Fore.YELLOW}[+] Program selesai. Terima kasih!")
    time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Program dihentikan")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
        print(f"{Fore.YELLOW}[!] Contact @Zxxtirwd untuk support")
