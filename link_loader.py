# from playwright.sync_api import sync_playwright
# import time

# PROFILE_URL = "https://www.linkedin.com/in/ayushwase/"
# OUTPUT_FILE = "linkedin_profile.txt"

# def scrape_linkedin_profile(profile_url):
#     user_data_dir = "playwright_user_data"

#     with sync_playwright() as p:
#         browser = p.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=False)
#         page = browser.new_page()

#         print(f"Opening: {profile_url}")
#         page.goto(profile_url, timeout=30000)
#         page.wait_for_timeout(5000)  # wait for dynamic content

#         # Scroll to bottom to load experience, education
#         page.mouse.wheel(0, 3000)
#         time.sleep(2)

#         data = []

#         # --- Name & Headline ---
#         try:
#             name = page.locator("h1").first.inner_text()
#             data.append(f"Name: {name}")
#         except:
#             data.append("Name: Not found")

#         try:
#             headline = page.locator("div.text-body-medium").first.inner_text()
#             data.append(f"Headline: {headline}")
#         except:
#             data.append("Headline: Not found")

#         # --- About Section ---
#         try:
#             about_section = page.locator("section:has(h2:has-text('About')) div.inline-show-more-text").inner_text()
#             data.append("\n--- About ---")
#             data.append(about_section.strip())
#         except:
#             data.append("\n--- About section not found ---")

#         # --- Experience Section ---
#         try:
#             data.append("\n--- Experience ---")
#             experience_items = page.locator("section:has(h2:has-text('Experience')) li")
#             count = experience_items.count()
#             for i in range(count):
#                 text = experience_items.nth(i).inner_text().strip()
#                 if text:
#                     data.append(text)
#         except:
#             data.append("\n--- Experience not found ---")

#         # --- Education Section ---
#         try:
#             data.append("\n--- Education ---")
#             edu_items = page.locator("section:has(h2:has-text('Education')) li")
#             count = edu_items.count()
#             for i in range(count):
#                 text = edu_items.nth(i).inner_text().strip()
#                 if text:
#                     data.append(text)
#         except:
#             data.append("\n--- Education not found ---")

#         # Save output
#         with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#             f.write("\n\n".join(data))

#         print(f"\n[+] Data saved to {OUTPUT_FILE}")
#         browser.close()

# if __name__ == "__main__":
#     scrape_linkedin_profile(PROFILE_URL)

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