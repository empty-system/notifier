import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import time
import os
import hashlib
import json
from datetime import datetime, timedelta

# Setup
URL_FILE = "C:/Users/Shenmue/Desktop/desktop/coding vite fait/change/urls.txt" # Input
STORAGE_DIR = "C:/Users/Shenmue/Desktop/desktop/coding vite fait/change/last_content" # Output
CHECK_INTERVAL = 300  # 300 sec = 5 min
CLASS_NAME = "overlay"

os.makedirs(STORAGE_DIR, exist_ok=True)
notifier = ToastNotifier()

def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()

def fetch_overlay_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", class_=CLASS_NAME)
        return [link.get_text(strip=True) + " -> " + link['href'] for link in links]
    except Exception as e:
        print(f"Error while fetching {url} : {e}")
        return []

def read_previous(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except Exception as e:
        print(f"Error while reading {filepath}: {e}")
        return []

def write_current(filepath, content_lines):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content_lines))
    except Exception as e:
        print(f"Error while writing {filepath}: {e}")

def notify(title, messages):
    full_msg = "\n".join(messages)
    if len(full_msg) > 500:
        full_msg = full_msg[:490] + "\n[...]"
    notifier.show_toast(title, full_msg, duration=10)

STATS_FILE = "C:/Users/Shenmue/Desktop/desktop/coding vite fait/change/stats.json"
RESET_FILE = "C:/Users/Shenmue/Desktop/desktop/coding vite fait/change/stats_reset.txt"

def load_reset_date():
    if not os.path.exists(RESET_FILE):
        return datetime.today().date()
    try:
        with open(RESET_FILE, "r") as f:
            return datetime.fromisoformat(f.read().strip()).date()
    except:
        return datetime.today().date()

def save_reset_date(date_obj):
    with open(RESET_FILE, "w") as f:
        f.write(date_obj.isoformat())

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def write_stats(stats_dict):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats_dict, f, indent=2, ensure_ascii=False)

def check_and_reset_stats():
    last_reset = load_reset_date()
    today = datetime.today().date()
    if (today - last_reset).days >= 3:
        write_stats({})
        save_reset_date(today)
        return {}
    return load_stats()

def main():
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found.")
        return

    with open(URL_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    stats = check_and_reset_stats()

    while True:
        for url in urls:
            current_links = fetch_overlay_links(url)
            filename = os.path.join(STORAGE_DIR, f"{hash_url(url)}.txt")
            previous_links = read_previous(filename)

            new_items = [link for link in current_links if link not in previous_links]
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checked {url}, found {len(current_links)} links.")

            if new_items:
                count_new = len(new_items)

                if not isinstance(stats.get(url), dict):
                    stats[url] = {
                        "total": 0,
                        "last_notif": []
                    }


                stats[url]["total"] += count_new

                notif_text = [
                    f"{count_new} new torrent(s) :",
                    url,
                    f"Total over 3 days: {stats[url]['total']}"
                ]

                stats[url]["last_notif"] = notif_text

                notify("New torrents detected", notif_text)
                write_current(filename, current_links)

        write_stats(stats)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
