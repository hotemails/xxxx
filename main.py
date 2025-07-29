import subprocess
import sys
import importlib.util

def n():
    required_packages = [
        "requests",
        "bs4",
        "colorama",
        "fake_useragent",
        "urllib3",
        "concurrent.futures",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        import_name = package
        if package == "bs4":
            import_name = "bs4"
        elif package == "concurrent.futures":
            continue
        
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("All required packages have been installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            sys.exit(1)
    else:
        print("All required packages are already installed.")

if __name__ == "__main__":
    n()

    import requests
    import re
    import os
    import urllib3
    import datetime
    import threading
    import base64
    import time
    import random
    import json
    from bs4 import BeautifulSoup
    from colorama import Fore, init
    from fake_useragent import UserAgent
    from concurrent.futures import ThreadPoolExecutor, as_completed

    init(autoreset=True)

def set_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

config = {
    'domains': {
        'riotgames.com': False,
        'crunchyroll.com': False,
        'epicgames.com': False,
        'roblox.com': False,
        'instagram.com': False
    },
    'email_domains': {
        'hotmail.com': False,
        'gmail.com': False,
        'yahoo.com': False,
        'outlook.com': False
    },
    'scrape_mode': 'Gaming'
}

def load_config():
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                loaded = json.load(f)
                config.update(loaded)
    except:
        pass

def save_config():
    try:
        with open('settings.json', 'w') as f:
            json.dump(config, f, indent=4)
    except:
        pass

e = datetime.datetime.now()
current_date = e.strftime("%Y-%m-%d-%H-%M-%S")
urllib3.disable_warnings()
ua = UserAgent()
agent = {'User-Agent': ua.random}
pages = 0
scraped = 0
session = requests.Session()
target_domain = ""

start_time = None
last_update_time = None
last_scraped_count = 0
scraping_speed = 0

if not os.path.exists("results"): 
    os.makedirs("results/")

results_folder = f"results/result_{current_date}"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

checked_accounts = set()

def print_banner():
    banner = f"""
{Fore.CYAN}                    ██╗     ██╗   ██╗███╗   ██╗ █████╗ 
                    ██║     ██║   ██║████╗  ██║██╔══██╗
                    ██║     ██║   ██║██╔██╗ ██║███████║
                    ██║     ██║   ██║██║╚██╗██║██╔══██║
                    ███████╗╚██████╔╝██║ ╚████║██║  ██║
                    ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝{Fore.RESET}

{Fore.WHITE}                     Developed by: {Fore.CYAN}@cleanest{Fore.RESET}
{Fore.WHITE}                     Version: {Fore.CYAN}2.0.0{Fore.RESET}
"""
    print(banner)

def print_status(message, status_type="info"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    if status_type == "success":
        print(f"{Fore.WHITE}{Fore.CYAN}[ * ] {Fore.WHITE}{message}{Fore.RESET}")
    elif status_type == "error":
        print(f"{Fore.WHITE}{Fore.CYAN}{Fore.CYAN} [ * ] {Fore.WHITE}{message}{Fore.RESET}")
    elif status_type == "info":
        print(f"{Fore.WHITE}{Fore.CYAN}[ * ] {Fore.WHITE}{message}{Fore.RESET}")
    elif status_type == "debug":
        print(f"{Fore.WHITE}[{Fore.CYAN}{timestamp}{Fore.WHITE}] {Fore.MAGENTA}{message}{Fore.RESET}")

def is_target_account(username, password, url=None):
    if config['scrape_mode'] == 'Gaming':
        enabled_domains = [domain for domain, enabled in config['domains'].items() if enabled]
        
        if url:
            for domain in enabled_domains:
                if domain in url.lower():
                    return domain
        
        if '@' in username:
            email_domain = username.split('@')[1].split(':')[0].lower()
            for domain in enabled_domains:
                if domain in email_domain:
                    return domain
    else:
        enabled_email_domains = [domain for domain, enabled in config['email_domains'].items() if enabled]
        
        if '@' in username:
            email_domain = username.split('@')[1].lower()
            for domain in enabled_email_domains:
                if email_domain == domain:
                    return domain
    
    return None

def update_stats():
    global last_update_time, last_scraped_count, scraping_speed, start_time
    current_time = time.time()
    
    if last_update_time is None:
        last_update_time = current_time
        return
    
    time_diff = current_time - last_update_time
    if time_diff >= 1:
        accounts_diff = scraped - last_scraped_count
        scraping_speed = accounts_diff / time_diff
        last_scraped_count = scraped
        last_update_time = current_time
        
        elapsed_time = int(current_time - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        print('\033[2K\033[G', end='')
        
        print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}]{Fore.WHITE} Dumped: {Fore.CYAN}({scraped:,}){Fore.RESET} | Speed: {Fore.CYAN}{scraping_speed:.1f}/s{Fore.RESET} | Time: {Fore.CYAN}{minutes:02d}:{seconds:02d}{Fore.RESET}", end='\r', flush=True)

def get_banner(dump_type="", count=0):
    return f"""                      (
                       )
                      (
                /\\  .-\"\"\"-.  /\\
               //\\\\ /  _  _ \\//\\\\
               |\\||  (o) (o) ||/|
               \\_/    \\_/    \\_//
               /_/      _      \\_\\
              ( //\\    (_)    /\\ \\ )
             _/ /_/            \\_\\ \\_
            (___(              )___)
              (                )
               (              )
                `-.        .-`
                   `-.__.-`
                   _/ /  \\ \\_
                  /__/    \\__\\


        Luna v2.0.0 | By @cleanest

            Dumped > {dump_type}

"""

def save_account(account, original_line=""):
    try:
        global scraped
        username, password = account.split(':', 1)
        username = username.strip()
        password = password.strip()
        
        if "[not_saved]" in password.lower():
            return
        
        if "//" in username:
            return
        
        matching_domain = is_target_account(username, password, original_line)
        
        if matching_domain:
            account_str = f"{username}:{password}"
            if account_str not in checked_accounts:
                checked_accounts.add(account_str)
                scraped += 1
                
                accounts_file = f'{results_folder}/{matching_domain.replace(".", "_")}_accounts.txt'
                if not os.path.exists(accounts_file):
                    with open(accounts_file, 'w', encoding='utf-8') as f:
                        f.write(get_banner(matching_domain, scraped))
                        
                with open(accounts_file, 'a', encoding='utf-8') as f:
                    f.write(f"{account_str}\n")
                    f.flush()
                
                update_stats()
                
    except Exception as e:
        print_status("Error saving combo.", "error")

def login():
    try:
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://crackingx.com/'
        }
        
        response = session.get('https://crackingx.com/login', headers=headers, timeout=10)
        token_match = re.search(r'name="_xfToken" value="([^"]+)"', response.text)
        if not token_match:
            return False

        xf_token = token_match.group(1)

        login_data = {
            'login': 'qdqdqd11',
            'password': 'x9eaHyTWgRDK5LT',
            'remember': '1',
            '_xfRedirect': 'https://crackingx.com/',
            '_xfToken': xf_token
        }

        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Origin'] = 'https://crackingx.com'
        headers['Referer'] = 'https://crackingx.com/login'

        response = session.post(
            'https://crackingx.com/login/login',
            headers=headers,
            data=login_data,
            allow_redirects=False,
            timeout=10
        )

        if response.status_code in [302, 303] or 'location' in response.headers.keys():
            return True
        else:
            return False

    except:
        return False

class leech():
    @staticmethod
    def crackingx():
        try:
            print()
            for page in range(1, pages):
                try:
                    req = session.get(
                        f"https://crackingx.com/forums/5/page-{page}?prefix_id=2&order=post_date&direction=desc",
                        headers=agent,
                        timeout=10
                    )
                    soup = BeautifulSoup(req.text, 'html.parser')
                    thread_items = soup.find_all('div', class_='structItem--thread')
                    
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        futures = []
                        for item in thread_items:
                            try:
                                title_div = item.find('div', class_='structItem-title')
                                if title_div:
                                    title_link = title_div.find('a', {'data-tp-primary': 'on'})
                                    if title_link:
                                        thread_url = title_link.get('href')
                                        if thread_url:
                                            futures.append(
                                                executor.submit(leech.process_thread, thread_url)
                                            )
                            except:
                                continue
                        
                        for future in as_completed(futures):
                            try:
                                future.result()
                            except:
                                continue
                except:
                    continue
            print('\n')
        except:
            pass

    @staticmethod
    def process_thread(thread_url):
        try:
            accounts_found = []
            
            response = session.get(f"https://crackingx.com{thread_url}", headers=agent, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hidden_blocks = soup.find_all('div', {'class': ['bbCodeBlock--hidden', 'bbCodeSpoiler']})
            for block in hidden_blocks:
                content = block.get_text()
                if re.search(r'([^\s|]+[@][^\s|]+[.][^\s|]+[:][^\s|]+)', content):
                    accounts_found.append((content, thread_url, "direct_content"))
            
            for ele in soup.find_all('div', class_='bbWrapper'):
                content = ele.get_text()
                if re.search(r'([^\s|]+[@][^\s|]+[.][^\s|]+[:][^\s|]+)', content):
                    accounts_found.append((content, thread_url, "direct_content"))
                
                for url in ele.find_all('a', href=True):
                    href_url = url.get('href')
                    if href_url.startswith(('https://www.upload.ee/files/', 
                                          'https://www.mediafire.com/file/',
                                          'https://pixeldrain.com/u/',
                                          'https://gofile.io/d/')):
                        accounts_found.append((href_url, thread_url, "link"))
            
            random.shuffle(accounts_found)
            
            for content, thread, content_type in accounts_found:
                if content_type == "link":
                    leech.handle_link(content, thread)
                else:
                    leech.save(content, thread, content_type)
                    
        except:
            pass

    @staticmethod
    def process_ulp_thread(thread_url):
        try:
            response = session.get(f"https://crackingx.com{thread_url}", headers=agent, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for ele in soup.find_all('div', class_='bbWrapper'):
                for url in ele.find_all('a', href=True):
                    href_url = url.get('href')
                    if any(host in href_url.lower() for host in [
                        'upload.ee/files',
                        'mediafire.com/file',
                        'anonfiles.com',
                        'gofile.io',
                        'mega.nz',
                        'dropbox.com',
                        'pixeldrain.com',
                        'drive.google.com',
                        'anonfile.com',
                        'dropmefiles.com',
                        'sendspace.com',
                        'workupload.com',
                        'file.io',
                        'bayfiles.com',
                        'zippyshare.com'
                    ]):
                        leech.handle_ulp_link(href_url, thread_url)
        except:
            pass

    @staticmethod
    def handle_link(link, thread):
        try:
            if link.startswith('https://www.upload.ee/files/'):
                f = BeautifulSoup(session.get(link, headers=agent, timeout=10).text, 'html.parser')
                download = f.find('a', id='d_l')
                if download:
                    content = session.get(download.get('href'), headers=agent, timeout=10).text
                    leech.save(content, thread, "upload.ee")
            elif link.startswith('https://www.mediafire.com/file/'):
                f = BeautifulSoup(session.get(link, headers=agent, timeout=10).text, 'html.parser')
                download = f.find('a', id='downloadButton')
                if download:
                    content = session.get(download.get('href'), headers=agent, timeout=10).text
                    leech.save(content, thread, "mediafire.com")
            elif link.startswith('https://pixeldrain.com/u/'):
                download_url = link.replace("/u/", "/api/file/")+"?download"
                content = session.get(download_url, headers=agent, timeout=10).text
                leech.save(content, thread, "pixeldrain.com")
            elif link.startswith('https://gofile.io/d/'):
                token = session.post("https://api.gofile.io/accounts", timeout=10).json()["data"]["token"]
                wt = session.get("https://gofile.io/dist/js/alljs.js", timeout=10).text.split('wt: "')[1].split('"')[0]
                content_id = link.split("/")[-1]
                data = session.get(
                    f"https://api.gofile.io/contents/{content_id}?wt={wt}&cache=true",
                    headers={"Authorization": "Bearer " + token},
                    timeout=10
                ).json()
                if data["status"] == "ok":
                    if data["data"].get("passwordStatus", "passwordOk") == "passwordOk":
                        content = session.get(
                            data["data"]["link"],
                            headers={"Cookie": "accountToken=" + token},
                            timeout=10
                        ).text
                        leech.save(content, thread, "gofile.io")
        except:
            pass

    @staticmethod
    def handle_ulp_link(link, thread):
        try:
            if 'upload.ee/files' in link:
                f = BeautifulSoup(session.get(link, headers=agent, timeout=10).text, 'html.parser')
                download = f.find('a', id='d_l')
                if download:
                    download_url = download.get('href')
                    content = session.get(download_url, headers=agent, timeout=10).text
                    if content:
                        leech.save_ulp(content, thread, "upload.ee")
            
            elif 'mediafire.com/file' in link:
                f = BeautifulSoup(session.get(link, headers=agent, timeout=10).text, 'html.parser')
                download = f.find('a', id='downloadButton')
                if download:
                    content = session.get(download.get('href'), headers=agent, timeout=10).text
                    if content:
                        leech.save_ulp(content, thread, "mediafire.com")
            
            elif 'gofile.io' in link:
                try:
                    content_id = link.split("/")[-1]
                    token = session.get("https://api.gofile.io/createAccount", timeout=10).json()["data"]["token"]
                    data = session.get(
                        f"https://api.gofile.io/getContent?contentId={content_id}&token={token}",
                        headers={"Accept": "application/json"},
                        timeout=10
                    ).json()
                    if data.get("status") == "ok":
                        for _, file_info in data.get("data", {}).get("contents", {}).items():
                            if file_info.get("link"):
                                content = session.get(file_info["link"], headers=agent, timeout=10).text
                                if content:
                                    leech.save_ulp(content, thread, "gofile.io")
                except:
                    pass

            elif 'pixeldrain.com' in link:
                try:
                    file_id = link.split("/")[-1]
                    download_url = f"https://pixeldrain.com/api/file/{file_id}?download"
                    content = session.get(download_url, headers=agent, timeout=10).text
                    if content:
                        leech.save_ulp(content, thread, "pixeldrain.com")
                except:
                    pass

            elif 'anonfiles.com' in link or 'anonfile.com' in link:
                try:
                    f = BeautifulSoup(session.get(link, headers=agent, timeout=10).text, 'html.parser')
                    download = f.find('a', id='download-url')
                    if download:
                        content = session.get(download.get('href'), headers=agent, timeout=10).text
                        if content:
                            leech.save_ulp(content, thread, "anonfiles.com")
                except:
                    pass

            elif 'zippyshare.com' in link:
                try:
                    f = BeautifulSoup(session.get(link, headers=agent, timeout=10).text, 'html.parser')
                    download = f.find('a', id='dlbutton')
                    if download:
                        content = session.get(download.get('href'), headers=agent, timeout=10).text
                        if content:
                            leech.save_ulp(content, thread, "zippyshare.com")
                except:
                    pass

        except:
            pass

    @staticmethod 
    def save_ulp(output, thread, host):
        try:
            combos = set()
            lines = [line.strip() for line in output.split('\n') if line.strip()]
            
            for line in lines:
                if line and ':' in line:
                    if line.lower().startswith(('http://', 'https://')):
                        if line.count(':') >= 2:
                            if '[not_saved]' in line.lower():
                                continue
                            combos.add(line.strip())
            
            combos_list = list(combos)
            random.shuffle(combos_list)
            
            global scraped
            for combo in combos_list:
                if combo not in checked_accounts:
                    checked_accounts.add(combo)
                    scraped += 1
                    
                    ulp_file = f'{results_folder}/ulp_combos.txt'
                    if not os.path.exists(ulp_file):
                        with open(ulp_file, 'w', encoding='utf-8') as f:
                            f.write(get_banner("ULP", scraped))
                            
                    with open(ulp_file, 'a', encoding='utf-8') as f:
                        f.write(f"{combo}\n")
                        f.flush()
                    
                    update_stats()
        except:
            pass

    @staticmethod
    def crackingx_ulp():
        try:
            print()
            for page in range(1, pages):
                try:
                    req = session.get(
                        f"https://crackingx.com/forums/5/page-{page}",
                        headers=agent,
                        timeout=10
                    )
                    soup = BeautifulSoup(req.text, 'html.parser')
                    thread_items = soup.find_all('div', class_='structItem--thread')
                    
                    thread_items = list(thread_items)
                    random.shuffle(thread_items)
                    
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        futures = []
                        for item in thread_items:
                            try:
                                title_div = item.find('div', class_='structItem-title')
                                if title_div:
                                    title_link = title_div.find('a', {'data-tp-primary': 'on'})
                                    if title_link:
                                        thread_url = title_link.get('href')
                                        if thread_url:
                                            futures.append(
                                                executor.submit(leech.process_ulp_thread, thread_url)
                                            )
                            except:
                                continue
                        
                        random.shuffle(futures)
                        
                        for future in as_completed(futures):
                            try:
                                future.result()
                            except:
                                continue
                except:
                    continue
            print('\n')
        except:
            pass

    @staticmethod
    def save(output, thread, host, alr = False):
        patterns = [
            r'@?https?://[^:\s]+/[^:\s]+:([^:\s]+:[^:\s]+)$',
            r'@?https?://[^:\s]+:([^:\s]+:[^:\s]+)(?:\s|$)',
            r'([^:\s]+:[^:\s]+)$'
        ]
        
        if not alr:
            filtered = []
            lines = output.split('\n')
            
            random.shuffle(lines)
            
            for line in lines:
                line = line.strip()
                if len(line) > 0 and len(line) <= 200:
                    for pattern in patterns:
                        match = re.search(pattern, line)
                        if match:
                            login_pass = match.group(1)
                            if len(login_pass.split(':')) == 2:
                                filtered.append(login_pass)
                                save_account(login_pass, line)
                            break
        else:
            filtered = list(output)
            random.shuffle(filtered)
            for account in filtered:
                save_account(account)

def show_searcher_menu():
    while True:
        clear()
        print_banner()
        print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        print(f"{Fore.CYAN}                        SEARCHER MENU")
        print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")

        options = [
            ("TOOL SEARCHER", "Cracking Tools for crackers - bruteforce, checker, spam, parser and virology"),
            ("CONFIG SEARCHER", "Free configs for different services and sites"),
            ("WORDLIST SEARCHER", "Search and download wordlists"),
            ("TUTORIAL SEARCHER", "Cracking Tutorials and Guides for beginners"),
            ("MONEY METHODS", "Leaked tutorials and ways to earn money online"),
        ]

        for i, (option, desc) in enumerate(options, 1):
            print(f"{Fore.WHITE}  [{Fore.CYAN}{i}{Fore.WHITE}] {Fore.CYAN}{option:<18} {Fore.WHITE}• {desc}")

        print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to main menu")
        print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        
        choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Searcher{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}")
        
        if choice == '1':
            search_tools()
        elif choice == '2':
            search_configs()
        elif choice == '3':
            search_wordlists()
        elif choice == '4':
            search_tutorials()
        elif choice == '5':
            search_money_methods()
        elif choice.upper() == 'B':
            break

def show_main_menu():    
    options = [
        ("COMBO DUMPER", "Dump combos from various sources"),
        ("ULP DUMPER", "Dump ULP combos specifically"),
        ("SEARCHERS", "Access various search tools and resources"),
        ("Settings", "Configure dumping settings"),
        ("EXIT", "Exit the program")
    ]
    
    for i, (option, desc) in enumerate(options, 1):
        print(f"{Fore.WHITE}  [{Fore.CYAN}{i}{Fore.WHITE}] {Fore.CYAN}{option:<18} {Fore.WHITE}• {desc}")
    
    print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
    choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Menu{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}")
    return choice

def select_config_type():
    clear()
    print_banner()
    print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
    print(f"{Fore.CYAN}                     CONFIG TYPE SELECT")
    print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
    
    options = [
        ("LOLI CONFIGS", "Browse LOLI configurations"),
        ("SVB CONFIGS", "Browse SVB configurations"),
        ("ALL CONFIGS", "Browse all configurations")
    ]
    
    for i, (option, desc) in enumerate(options, 1):
        print(f"{Fore.WHITE}  [{Fore.CYAN}{i}{Fore.WHITE}] {Fore.CYAN}{option:<15} {Fore.WHITE}• {desc}")
    
    print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
    
    while True:
        choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Config{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}")
        
        if choice == '1':
            return ('LOLI', '?prefix_id=7')
        elif choice == '2':
            return ('SVB', '?prefix_id=12')
        elif choice == '3':
            return ('ALL', '')
        elif choice.upper() == 'B':
            return None

def search_configs():
    config_type = select_config_type()
    if not config_type:
        return
        
    type_name, type_query = config_type
    current_page = 1
    
    while True:
        try:
            clear()
            print_banner()
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"{Fore.CYAN}                    {type_name} CONFIG SEARCHER") 
            print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
            
            response = session.get(
                f"https://crackingx.com/forums/10/page-{current_page}{type_query}",
                headers=agent,
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            configs = []
            for item in soup.find_all('div', class_='structItem-cell structItem-cell--main'):
                title_div = item.find('div', class_='structItem-title')
                if title_div:
                    link = title_div.find('a', {'data-tp-primary': 'on'})
                    if link:
                        configs.append((link.text.strip(), link.get('href')))
            
            if not configs:
                print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No configs found on this page!")
                input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to go back...")
                break
            
            print(f"{Fore.CYAN}[{Fore.WHITE}i{Fore.CYAN}] {Fore.WHITE}Page {current_page}\n")
            
            for idx, (title, _) in enumerate(configs, 1):
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {Fore.CYAN}{title}")
            
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"  {Fore.WHITE}[{Fore.CYAN}N{Fore.WHITE}] Next Page {Fore.WHITE}• {Fore.CYAN}Go to next page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}P{Fore.WHITE}] Previous Page {Fore.WHITE}• {Fore.CYAN}Go to previous page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to config types")
            
            choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Configs{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
            
            if choice == 'B':
                break
            elif choice == 'N':
                current_page += 1
            elif choice == 'P' and current_page > 1:
                current_page -= 1
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(configs):
                    config_name, config_url = configs[idx-1]
                    show_tool_details(config_name, config_url)
        except:
            print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Error loading page!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to retry...")

def show_tool_details(tool_name, thread_url):
    try:
        clear()
        print_banner()
        
        print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        print(f"{Fore.CYAN}                        TOOL DETAILS")
        print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
        
        print(f"{Fore.CYAN}Tool: {Fore.WHITE}{tool_name}\n")
        
        response = session.get(f"https://crackingx.com{thread_url}", headers=agent, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        download_links = []
        description = ""
        
        for wrapper in soup.find_all('div', class_='bbWrapper'):
            description = wrapper.get_text().strip()
            for link in wrapper.find_all('a', href=True):
                href = link.get('href')
                if any(host in href.lower() for host in [
                    'mediafire.com',
                    'mega.nz',
                    'anonfiles.com',
                    'gofile.io',
                    'fex.net',
                    'sharefile.co',
                    'dropbox.com',
                    'pixeldrain.com',
                    'upload.ee'
                ]):
                    download_links.append(href)
        
        print(f"{Fore.WHITE}{description}\n")
        
        if download_links:
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"{Fore.CYAN}Download Links:\n")
            for idx, link in enumerate(download_links, 1):
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {Fore.CYAN}{link}")
        
        print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to tool list")
        
        while True:
            choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Tool{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
            
            if choice == 'B':
                return
    except:
        print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Error loading tool details!")
        input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to go back...")

def search_tools():
    clear()
    print_banner()
    
    current_page = 1
    
    while True:
        try:
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"{Fore.CYAN}                       TOOL SEARCHER")
            print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
            
            response = session.get(
                f"https://crackingx.com/forums/9/page-{current_page}",
                headers=agent,
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tools = []
            for item in soup.find_all('div', class_='structItem-cell structItem-cell--main'):
                title_div = item.find('div', class_='structItem-title')
                if title_div:
                    link = title_div.find('a', {'data-tp-primary': 'on'})
                    if link:
                        tools.append((link.text.strip(), link.get('href')))
            
            if not tools:
                print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No tools found on this page!")
                input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to go back...")
                break
            
            print(f"{Fore.CYAN}[{Fore.WHITE}i{Fore.CYAN}] {Fore.WHITE}Page {current_page}\n")
            
            for idx, (title, _) in enumerate(tools, 1):
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {Fore.CYAN}{title}")
            
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"  {Fore.WHITE}[{Fore.CYAN}N{Fore.WHITE}] Next Page {Fore.WHITE}• {Fore.CYAN}Go to next page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}P{Fore.WHITE}] Previous Page {Fore.WHITE}• {Fore.CYAN}Go to previous page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to main menu")
            
            choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Tools{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
            
            if choice == 'B':
                break
            elif choice == 'N':
                current_page += 1
                clear()
                print_banner()
            elif choice == 'P' and current_page > 1:
                current_page -= 1
                clear()
                print_banner()
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(tools):
                    tool_name, tool_url = tools[idx-1]
                    show_tool_details(tool_name, tool_url)
                    clear()
                    print_banner()
        except:
            print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Error loading page!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to retry...")
            clear()
            print_banner()

def search_wordlists():
    clear()
    print_banner()
    current_page = 1
    
    while True:
        try:
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"{Fore.CYAN}                     WORDLIST SEARCHER")
            print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
            
            response = session.get(
                f"https://crackingx.com/forums/5/page-{current_page}?prefix_id=3",
                headers=agent,
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            wordlists = []
            for item in soup.find_all('div', class_='structItem-cell structItem-cell--main'):
                title_div = item.find('div', class_='structItem-title')
                if title_div:
                    link = title_div.find('a', {'data-tp-primary': 'on'})
                    if link:
                        wordlists.append((link.text.strip(), link.get('href')))
            
            if not wordlists:
                print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No wordlists found on this page!")
                input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to go back...")
                break
            
            print(f"{Fore.CYAN}[{Fore.WHITE}i{Fore.CYAN}] {Fore.WHITE}Page {current_page}\n")
            
            for idx, (title, _) in enumerate(wordlists, 1):
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {Fore.CYAN}{title}")
            
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"  {Fore.WHITE}[{Fore.CYAN}N{Fore.WHITE}] Next Page {Fore.WHITE}• {Fore.CYAN}Go to next page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}P{Fore.WHITE}] Previous Page {Fore.WHITE}• {Fore.CYAN}Go to previous page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to main menu")
            
            choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Wordlists{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
            
            if choice == 'B':
                break
            elif choice == 'N':
                current_page += 1
                clear()
                print_banner()
            elif choice == 'P' and current_page > 1:
                current_page -= 1
                clear()
                print_banner()
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(wordlists):
                    wordlist_name, wordlist_url = wordlists[idx-1]
                    show_tool_details(wordlist_name, wordlist_url)
                    clear()
                    print_banner()
        except:
            print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Error loading page!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to retry...")
            clear()
            print_banner()

def search_tutorials():
    clear()
    print_banner()
    current_page = 1
    
    while True:
        try:
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"{Fore.CYAN}                   TUTORIALS & GUIDES")
            print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
            
            response = session.get(
                f"https://crackingx.com/forums/11/page-{current_page}",
                headers=agent,
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tutorials = []
            for item in soup.find_all('div', class_='structItem-cell structItem-cell--main'):
                title_div = item.find('div', class_='structItem-title')
                if title_div:
                    link = title_div.find('a', {'data-tp-primary': 'on'})
                    if link:
                        tutorials.append((link.text.strip(), link.get('href')))
            
            if not tutorials:
                print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No tutorials found on this page!")
                input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to go back...")
                break
            
            print(f"{Fore.CYAN}[{Fore.WHITE}i{Fore.CYAN}] {Fore.WHITE}Page {current_page}\n")
            
            for idx, (title, _) in enumerate(tutorials, 1):
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {Fore.CYAN}{title}")
            
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"  {Fore.WHITE}[{Fore.CYAN}N{Fore.WHITE}] Next Page {Fore.WHITE}• {Fore.CYAN}Go to next page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}P{Fore.WHITE}] Previous Page {Fore.WHITE}• {Fore.CYAN}Go to previous page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to main menu")
            
            choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Tutorials{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
            
            if choice == 'B':
                break
            elif choice == 'N':
                current_page += 1
                clear()
                print_banner()
            elif choice == 'P' and current_page > 1:
                current_page -= 1
                clear()
                print_banner()
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(tutorials):
                    tutorial_name, tutorial_url = tutorials[idx-1]
                    show_tool_details(tutorial_name, tutorial_url)
                    clear()
                    print_banner()
        except:
            print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Error loading page!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to retry...")
            clear()
            print_banner()

def search_money_methods():
    clear()
    print_banner()
    current_page = 1
    
    while True:
        try:
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"{Fore.CYAN}                   MONETIZING METHODS")
            print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
            
            response = session.get(
                f"https://crackingx.com/forums/4/page-{current_page}",
                headers=agent,
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            methods = []
            for item in soup.find_all('div', class_='structItem-cell structItem-cell--main'):
                title_div = item.find('div', class_='structItem-title')
                if title_div:
                    link = title_div.find('a', {'data-tp-primary': 'on'})
                    if link:
                        methods.append((link.text.strip(), link.get('href')))
            
            if not methods:
                print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No methods found on this page!")
                input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to go back...")
                break
            
            print(f"{Fore.CYAN}[{Fore.WHITE}i{Fore.CYAN}] {Fore.WHITE}Page {current_page}\n")
            
            for idx, (title, _) in enumerate(methods, 1):
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {Fore.CYAN}{title}")
            
            print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
            print(f"  {Fore.WHITE}[{Fore.CYAN}N{Fore.WHITE}] Next Page {Fore.WHITE}• {Fore.CYAN}Go to next page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}P{Fore.WHITE}] Previous Page {Fore.WHITE}• {Fore.CYAN}Go to previous page")
            print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to main menu")
            
            choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Methods{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
            
            if choice == 'B':
                break
            elif choice == 'N':
                current_page += 1
                clear()
                print_banner()
            elif choice == 'P' and current_page > 1:
                current_page -= 1
                clear()
                print_banner()
            elif choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(methods):
                    method_name, method_url = methods[idx-1]
                    show_tool_details(method_name, method_url)
                    clear()
                    print_banner()
        except:
            print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Error loading page!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to retry...")
            clear()
            print_banner()

def show_options_menu():
    while True:
        clear()
        print_banner()
        print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        print(f"{Fore.CYAN}                     SETTINGS & OPTIONS")
        print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════\n")
        
        print(f"{Fore.WHITE}Current Mode: {Fore.CYAN}{config['scrape_mode'].upper()}\n")
        
        if config['scrape_mode'] == 'Gaming':
            for idx, (domain, enabled) in enumerate(config['domains'].items(), 1):
                status = f"{Fore.GREEN}●" if enabled else f"{Fore.RED}●"
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {status} {Fore.CYAN}{domain}")
        else:
            for idx, (domain, enabled) in enumerate(config['email_domains'].items(), 1):
                status = f"{Fore.GREEN}●" if enabled else f"{Fore.RED}●"
                print(f"  {Fore.WHITE}[{Fore.CYAN}{idx}{Fore.WHITE}] {status} {Fore.CYAN}{domain}")
        
        print(f"\n{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        print(f"  {Fore.WHITE}[{Fore.CYAN}M{Fore.WHITE}] Switch Mode {Fore.WHITE}• {Fore.CYAN}Toggle between Gaming/Emails")
        print(f"  {Fore.WHITE}[{Fore.CYAN}A{Fore.WHITE}] Select All {Fore.WHITE}• {Fore.CYAN}Enable all domains")
        print(f"  {Fore.WHITE}[{Fore.CYAN}Q{Fore.WHITE}] Add Domain {Fore.WHITE}• {Fore.CYAN}Add new domain to list")
        print(f"  {Fore.WHITE}[{Fore.CYAN}Z{Fore.WHITE}] Remove Domain {Fore.WHITE}• {Fore.CYAN}Remove existing domain")
        print(f"  {Fore.WHITE}[{Fore.CYAN}B{Fore.WHITE}] Back {Fore.WHITE}• {Fore.CYAN}Return to main menu")
        print(f"{Fore.WHITE}═══════════════════════════════════════════════════════════════")
        
        choice = input(f"\n{Fore.CYAN}┌──({Fore.WHITE}LUNA{Fore.CYAN})─[{Fore.WHITE}Settings{Fore.CYAN}]\n└─{Fore.WHITE}$ {Fore.RESET}").upper()
        
        if choice == 'B':
            break
        elif choice == 'M':
            config['scrape_mode'] = 'Emails' if config['scrape_mode'] == 'Gaming' else 'Gaming'
            save_config()
        elif choice == 'A':
            if config['scrape_mode'] == 'Gaming':
                current_state = all(config['domains'].values())
                for domain in config['domains']:
                    config['domains'][domain] = not current_state
            else:
                current_state = all(config['email_domains'].values())
                for domain in config['email_domains']:
                    config['email_domains'][domain] = not current_state
            save_config()
        elif choice == 'Q':
            clear()
            print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}ADD DOMAIN\n")
            new_domain = input(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Enter domain (e.g. example.com): {Fore.RESET}").lower()
            if new_domain and '.' in new_domain:
                if config['scrape_mode'] == 'Gaming':
                    config['domains'][new_domain] = True
                else:
                    config['email_domains'][new_domain] = True
                save_config()
                print(f"\n{Fore.GREEN}Domain added successfully!")
                time.sleep(1)
        elif choice == 'Z':
            clear()
            print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}REMOVE DOMAIN\n")
            domains = list(config['domains'].keys()) if config['scrape_mode'] == 'Gaming' else list(config['email_domains'].keys())
            for i, domain in enumerate(domains, 1):
                print(f"{Fore.CYAN}[{Fore.WHITE}{i}{Fore.CYAN}] {Fore.WHITE}{domain}")
            try:
                idx = int(input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Enter domain number to remove: {Fore.RESET}"))
                if 1 <= idx <= len(domains):
                    if config['scrape_mode'] == 'Gaming':
                        del config['domains'][domains[idx-1]]
                    else:
                        del config['email_domains'][domains[idx-1]]
                    save_config()
                    print(f"\n{Fore.GREEN}Domain removed successfully!")
                    time.sleep(1)
            except:
                print(f"\n{Fore.CYAN}Invalid selection!")
                time.sleep(1)
        elif choice.isdigit():
            idx = int(choice)
            if config['scrape_mode'] == 'Gaming':
                domains = list(config['domains'].keys())
                if 1 <= idx <= len(domains):
                    domain = domains[idx-1]
                    config['domains'][domain] = not config['domains'][domain]
            else:
                domains = list(config['email_domains'].keys())
                if 1 <= idx <= len(domains):
                    domain = domains[idx-1]
                    config['email_domains'][domain] = not config['email_domains'][domain]
            save_config()

def start_dumper():
    global start_time, scraped, pages
    
    clear()
    print_banner()
    
    if config['scrape_mode'] == 'Gaming':
        enabled_domains = [domain for domain, enabled in config['domains'].items() if enabled]
        if not enabled_domains:
            print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No gaming domains enabled in settings!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to continue...")
            return
    else:
        enabled_domains = [domain for domain, enabled in config['email_domains'].items() if enabled]
        if not enabled_domains:
            print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}No email domains enabled in settings!")
            input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to continue...")
            return
    
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Starting dumper...")
    
    if not login():
        print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Login failed!")
        input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to continue...")
        return
    
    start_time = time.time()
    scraped = 0
    checked_accounts.clear()
    pages = 51
    
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Dumping accounts...")
    print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Mode: {Fore.CYAN}{config['scrape_mode'].upper()}")
    print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Enabled domains: {Fore.CYAN}{', '.join(enabled_domains)}{Fore.WHITE}")
    print()
    
    if config['scrape_mode'] == 'Gaming':
        leech.crackingx()
    else:
        leech.crackingx_email()
    
    print('\n' * 3)
    
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    avg_speed = scraped / elapsed_time if elapsed_time > 0 else 0
    
    clear()
    print_banner()
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Operation completed!")
    print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Results saved in: {Fore.CYAN}{results_folder}")
    print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Results:")
    
    for domain in enabled_domains:
        file_path = f'{results_folder}/{domain.replace(".", "_")}_accounts.txt'
        count = 0
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                count = sum(1 for _ in f)
        print(f"    {Fore.CYAN}{domain}: {Fore.GREEN}{count:,} accounts")
    
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Summary:")
    print(f"    Total accounts: {Fore.GREEN}{scraped:,}")
    print(f"    Average speed: {Fore.CYAN}{avg_speed:.1f}/s")
    print(f"    Time elapsed: {Fore.YELLOW}{minutes:02d}:{seconds:02d}")
    
    input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to continue...")

def ulp_dumper():
    global start_time, scraped, pages
    
    clear()
    print_banner()
    
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Starting ULP dumper...")
    
    if not login():
        print(f"\n{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] {Fore.WHITE}Login failed!")
        input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to continue...")
        return
    
    start_time = time.time()
    scraped = 0
    checked_accounts.clear()
    pages = 51
    
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Dumping ULP links...")
    print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Mode: {Fore.CYAN}ULP DUMPER")
    print()
    
    leech.crackingx_ulp()
    
    print('\n' * 3)
    
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    avg_speed = scraped / elapsed_time if elapsed_time > 0 else 0
    
    clear()
    print_banner()
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Operation completed!")
    print(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Results saved in: {Fore.CYAN}{results_folder}")
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Summary:")
    print(f"    Total ULP combos: {Fore.GREEN}{scraped:,}")
    print(f"    Average speed: {Fore.CYAN}{avg_speed:.1f}/s")
    print(f"    Time elapsed: {Fore.YELLOW}{minutes:02d}:{seconds:02d}")
    
    input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to continue...")

def verify_login(username, password):
    try:
        i = base64.b64decode("cmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbQ==").decode('utf-8')
        j = [
            "emVkeHg3",
            "eHh4cQ==",
            "cmVmcw==",
            "aGVhZHM=",
            "bWFpbg==",
            "cXdkcXc="
        ]
        
        p = [base64.b64decode(part).decode('utf-8') for part in j]
        
        m = f"https://{i}/{'/'.join(p)}"
        
        response = requests.get(m)
        if response.status_code == 200:
            users = json.loads(response.text)
            for user in users:
                if user["user"] == username and user["pass"] == password:
                    return True
        return False
    except Exception as e:
        return False

def show_login():
    clear()
    print_banner()
    
    username = input(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Username: {Fore.RESET}")
    password = input(f"{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Password: {Fore.RESET}")
    
    print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Verifying credentials...")
    
    if verify_login(username, password):
        print(f"\n{Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}] {Fore.WHITE}Login successful!")
        time.sleep(1)
        return True
    else:
        print(f"\n{Fore.RED}[{Fore.WHITE}!{Fore.RED}] {Fore.WHITE}Invalid credentials!")
        input(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Press Enter to try again...")
        return False

def main():
    load_config()
    set_title(f"LUNA - By @cleanest")
    
    while not show_login():
        pass
        
    while True:
        clear()
        print_banner()
        choice = show_main_menu()
        
        if choice == '1':
            start_dumper()
        elif choice == '2':
            ulp_dumper()
        elif choice == '3':
            show_searcher_menu()
        elif choice == '4':
            show_options_menu()
        elif choice == '5':
            clear()
            print(f"\n{Fore.CYAN}[{Fore.WHITE}>{Fore.CYAN}] {Fore.WHITE}Thanks for using LUNA!")
            sys.exit()

if __name__ == "__main__":
    main()
