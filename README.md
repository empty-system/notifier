# 🔔 Torrent Watcher – Automatic Link Monitoring with Windows Notifications

A simple Python script that monitors web pages (e.g., torrent or VR release pages) for new `<a class="overlay">` links, sends grouped Windows notifications when something new appears, and tracks changes for up to 3 days.

---

## 📦 Features

- 🔍 Scrapes pages listed in `urls.txt` and detects new `<a class="overlay">` links
- 🧠 Remembers previously seen links (`last_content/`)
- 🔔 Sends a clean Windows toast notification when new content is detected
- 📊 Tracks how many new links were found per URL over the last 3 days (`stats.json`)
- 🔁 Automatically resets stats every 3 days
- 🚀 Optionally launches automatically at Windows startup

---

## 🗂️ Project Structure

```text
your-folder/
├── notifier.py            # Main script
├── urls.txt               # List of URLs to monitor (one per line)
├── last_content/          # Stores previously detected links (per URL)
├── stats.json             # Stats per URL and last notification
├── stats_reset.txt        # Last stats reset date
```

---

## ✏️ Setup

1. **Install dependencies** (you can use a virtual environment if desired):

Clone the repository
> git clone https://github.com/empty-system/notifier

Install the requirements
> pip install -r fdownloader/requirements.txt

2. **Config**:

Fill in `urls.txt` by adding one link per line

2. **Run**:

Double click run.bat
