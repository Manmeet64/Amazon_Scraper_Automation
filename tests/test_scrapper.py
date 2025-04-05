from src.scraper import scrape_amazon_products
from main import configure_driver


def test_scrape_returns_data():
    driver = configure_driver()
    try:
        data = scrape_amazon_products(driver,"iPhone15",1)
        assert isinstance(data,list)
        assert len(data) > 0
    finally:
        driver.quit()

def test_scrape_product_data_not_empty():
    driver = configure_driver()
    try:
        products = scrape_amazon_products(driver,"iPhone15",1)
        product = products[0]
        assert "Title" in product
        assert "Rating" in product
        assert "Price" in product
        assert "Link" in product
    finally:
        driver.quit()

        
