from playwright.sync_api import sync_playwright
import json
import os
import time

ARTICLE_JSON = "data_part_12.json"
HTML_DIR = "NS_rendered_html_dp12"
AUTH_STATE = "NS_login_state.json"
os.makedirs(HTML_DIR, exist_ok=True)

# STEP 1 – Run Once to Manually Login and Save Session
def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        print("Please log in manually...")
        page.goto("https://www.newscientist.com/login/")
        input("After login, press ENTER to save session...")
        context.storage_state(path=AUTH_STATE)
        print("Session saved to", AUTH_STATE)
        browser.close()

# STEP 2 – Use Saved Auth State to Access All Articles
def scrape_articles_with_auth():
    with open(ARTICLE_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=AUTH_STATE)
        page = context.new_page()

        for idx, article in enumerate(articles, 1):
            try:
                print(f"[{idx}/{len(articles)}] {article['url']}")
                page.goto(article["url"], wait_until="load", timeout=120000)
                time.sleep(3)  # extra time for paywall content to render
                html = page.content()

                file_path = os.path.join(HTML_DIR, f"ns_article_{idx:04d}.html")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)

            except Exception as e:
                print(f"Error fetching {article['url']}: {e}")


                browser.close()

# === Run One-Time Login and Save Session (only once)
# save_login_state()

# === Run the scraper using saved login state
scrape_articles_with_auth()
