from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.scraper import scrape_amazon_products
from src.utils import save_screenshot, save_logs
from src.config import SEARCH_QUERY, MAX_PAGES, OUTPUT_FILE
import csv

def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    return webdriver.Chrome(options=chrome_options)

def main():
    driver = configure_driver()
    try:
        data = scrape_amazon_products(driver, query=SEARCH_QUERY, max_pages=MAX_PAGES)


        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Rating", "Link"])
            writer.writeheader()
            writer.writerows(data)
        print(f"✅ CSV written to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
