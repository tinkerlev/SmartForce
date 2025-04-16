# SmartForce - AI-Assisted Web Login Bruteforcer

SmartForce is a lightweight and beginner-friendly tool that helps simulate automated login testing — for **educational, ethical, and research purposes only**.

It helps students, researchers, and ethical hackers understand how login mechanisms behave under realistic testing conditions.

⚠️ **This tool is strictly for learning and authorized security testing. Never use it on systems you don't have permission to test.**

---

## 🧠 What does SmartForce do?

1. You give it a website address.
2. It searches the site for names that could be usernames.
3. It creates smart password guesses based on those names.
4. It asks you for the login page URL.
5. You choose whether to test all usernames or just one.
6. You choose whether to test all passwords or just one.
7. You choose the form field names (by name or index).
8. It tests each combination and shows the result.
9. It saves all attempts and results to a JSON file.

---

## 📦 How to Install SmartForce

### Step 1: Download the project
Open your terminal and type:
```bash
git clone https://github.com/YOUR_USERNAME/smartforce.git
cd smartforce
```

### Step 2: Make sure Python 3 is installed
Type:
```bash
python3 --version
```
If it's not installed, get it from [https://www.python.org](https://www.python.org)

### Step 3: Install the required Python libraries
You can install the libraries one by one:
```bash
pip install requests bs4
```

Or install everything at once using:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file includes:
```
requests
bs4
```

---

## 🚀 How to Use SmartForce (Step-by-Step)

### Step 1: Run the tool
```bash
python3 smart_bruteforcer.py https://example.com
```
Replace `https://example.com` with the site you want to test (only if allowed).

### Step 2: The tool will crawl the site
Example output:
```
[+] Found usernames
[+] Found input fields:
[0] nombre
[1] pass
```

### Step 3: Provide the login form URL
If the login form is on another page:
```bash
🔗 Login URL: https://example.com/login
```

### Step 4: Choose username mode
```
Do you want to try ALL usernames? (y/n)
```
- Type `y` to test all scraped usernames
- Type `n` to enter one manually

### Step 5: Choose password mode
```
Do you want to try ALL passwords? (y/n)
```
- Type `y` to use the list in `passwords.txt`
- Type `n` to try one password

### Step 6: Choose field names
You can enter either a field **name** or **index** shown earlier:
```
Username field name or index: 4
Password field name or index: pass
```

### Step 7: View results
Example output:
```
[✓] SUCCESS: admin:admin2024
[✗] Failed: user:test123
```
Saved to:
```
smartforce_results.json
```

---

## 📁 Project Files Explained

| File                      | Description                          |
|---------------------------|--------------------------------------|
| `smart_bruteforcer.py`    | Main script                          |
| `usernames.txt`           | Usernames found on the site          |
| `passwords.txt`           | Auto-generated smart password list   |
| `smartforce_results.json` | Full result log                      |

---

## 🧩 Tips for Better Accuracy

- A successful login is usually detected by:
  - A word like `logout`, `dashboard`, `bienvenido`
  - A redirect (HTTP 302)
- Test on sites with real forms (not just marketing pages)
- If you're not getting results, try a more active page

You can also route traffic through TOR:
```bash
python3 smart_bruteforcer.py https://example.com --proxy
```
(Ensure the TOR service is running on port 9050)

---

## 🛠️ Troubleshooting

| Issue                             | Suggestion                                               |
|----------------------------------|----------------------------------------------------------|
| No usernames found               | Try scanning a more content-rich page                   |
| No input fields detected         | Check the URL — form may be on another subpage         |
| All attempts show SUCCESS        | Verify you used correct field names                     |
| Crashes on start                 | Ensure dependencies are installed (see install steps)   |

---

## 🧾 Be Responsible
SmartForce is here to help you learn and explore safely.
Only use it on websites and systems you’re allowed to test.
Use it for good.

---

## 🙋 About the Author

SmartForce was created by [Loai Deeb](https://www.linkedin.com/in/loai-deeb/), a cybersecurity teacher and ethical hacking enthusiast who builds practical tools for educational and research use.

GitHub repository: [SmartForce](https://github.com/tinkerlev/)

Feel free to connect or contribute.

---

## 📬 Questions or Feedback?
Open an issue on GitHub or contact the author.

---

Stay ethical — and keep learning 💻✨
