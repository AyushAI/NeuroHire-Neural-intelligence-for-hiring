from playwright.sync_api import sync_playwright
import time

def scrape_linkedin_profile(profile_url: str) -> str:
    user_data_dir = "playwright_user_data"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=True)
        page = browser.new_page()
        page.goto(profile_url, timeout=30000)
        page.wait_for_timeout(5000)
        page.mouse.wheel(0, 3000)
        time.sleep(2)

        data = []

        try:
            name = page.locator("h1").first.inner_text()
            data.append(f"Name: {name}")
        except:
            pass

        try:
            headline = page.locator("div.text-body-medium").first.inner_text()
            data.append(f"Headline: {headline}")
        except:
            pass

        try:
            about = page.locator("section:has(h2:has-text('About')) div.inline-show-more-text").inner_text()
            data.append("About:\n" + about.strip())
        except:
            pass

        try:
            data.append("Experience:")
            exp = page.locator("section:has(h2:has-text('Experience')) li")
            for i in range(exp.count()):
                t = exp.nth(i).inner_text().strip()
                if t:
                    data.append(t)
        except:
            pass

        try:
            data.append("Education:")
            edu = page.locator("section:has(h2:has-text('Education')) li")
            for i in range(edu.count()):
                t = edu.nth(i).inner_text().strip()
                if t:
                    data.append(t)
        except:
            pass

        browser.close()
        return "\n\n".join(data)