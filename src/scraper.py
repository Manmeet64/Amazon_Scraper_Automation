from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
def scrape_amazon_products(driver, search_term, num_pages):
    driver.get("https://www.amazon.in")
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
    except TimeoutException:
        driver.save_screenshot("timeout_error.png")
        print("Timeout occurred. Screenshot saved as timeout_error.png")
        raise

from src.utils import save_screenshot, save_logs

def scrape_amazon_products(driver, query="iPhone 15", max_pages=3):
    driver.get("https://www.amazon.in")
    print("Opened the browser")

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
    except TimeoutException:
        driver.save_screenshot("timeout_error.png")
        print("Timeout occurred. Screenshot saved as timeout_error.png")
        raise
    # # Search for the query
    # search_box = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    # )
    search_box.send_keys(query)

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))
    )
    search_button.click()

    current_page = 1
    striped_data = []

    while current_page <= max_pages:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-asin and @data-component-type='s-search-result']")
            )
        )
        print(f"[Page {current_page}] Products found: {len(products)}")
        save_screenshot(driver,folder="screenshots")

        for product in products:
            try:
                title = product.find_element(By.XPATH, ".//h2//span").text
            except:
                title = "N/A"
            try:
                price = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text.replace(",", "")
            except:
                price = "N/A"
            try:
                rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']").get_attribute("innerHTML").strip()
            except:
                rating = "N/A"
            try:
                link = product.find_element(By.XPATH, ".//a").get_attribute("href")
            except:
                link = "N/A"

            striped_data.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Link": link
            })

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'s-pagination-strip')]//li//a[text()='Next']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            save_logs(driver)
            next_button.click()
            WebDriverWait(driver, 5).until(EC.staleness_of(products[0]))
            current_page += 1
        except:
            print("No more pages or Next button not found.")
            break

    return striped_data