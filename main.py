from config.config import ShoppingOnlineLocation
from bs4 import BeautifulSoup
from driver.driver import create_web_driver
import tiki.tiki_scraper as tiki_scraper
import lazada.lazada_scraper as lazada_scraper
import shopee.shopee_scraper as shopee_scraper
import amazon.amazon_scraper as amazon_scraper
import fahasa.fahasa_scraper as fahasa_scraper
from config.input import input_initial_value
from config.input import add_to_cart

def shopping_online_run(location: str, keyword: str, keyword1: str, keyword2: str, keyword3: str, page: str):
    # location, keyword, page = input_initial_value()

    shopping_online_info = ShoppingOnlineLocation(
        location=location, 
        keyword=keyword,
        keyword1 =keyword1,
        keyword2 =keyword2, 
        keyword3= keyword3,
        page=page,
    )

    base_url = shopping_online_info.get_base_url()
    print(base_url)
    browser = create_web_driver(base_url, location)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    match location:
        case "tiki":
            product_info = tiki_scraper.get_product_info(soup=soup)
            shopping_online_info.add_product_to_csv(product_info)
        case "lazada":
            product_info = lazada_scraper.get_product_info(soup=soup)
            shopping_online_info.add_product_to_csv(product_info)
        case "fahasa":
            product_info = fahasa_scraper.get_product_info(soup=soup)
            shopping_online_info.add_product_to_csv(product_info)
        case "amazon":
            product_info = amazon_scraper.get_product_info(soup=soup)
            shopping_online_info.add_product_to_csv(product_info)
        case "shopee":
            is_choose = add_to_cart()
            if is_choose:
                index_item = int(input("Please fill item's index you want to add it in cart: "))
                shopee_scraper.add_product_to_cart(browser, soup, index_item)
            else:
                product_info = shopee_scraper.get_product_info(soup=soup)
                shopping_online_info.add_product_to_csv(product_info)
