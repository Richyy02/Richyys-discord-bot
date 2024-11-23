from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from random import randrange

def handle_response(user_query):
    product_info = main(user_query)
    return product_info

def get_content_from_url(user_query):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    random_page = randrange(3)
    driver.get(f"https://www.marktplaats.nl/q/{user_query}/p/{random_page}/")
    print(random_page)
    page_content = driver.page_source
    driver.quit()
    return page_content

def parse_image_url(content, classes, location, price_class):
    soup = BeautifulSoup(content, features="html.parser")
    result = []
    for element in soup.find_all(attrs={"class": classes}):
        title = element.find('h3', class_="hz-Listing-title").text.strip()
        src = element.find(location).get("src")
        raw_price = element.find("p", class_=price_class).text.strip()
        description = element.find("p", class_="hz-Listing-description hz-text-paragraph").text.strip()

        price = raw_price.replace('\xa0', ' ')
        
        info = {
            "title": title,
            "src": src,
            "price": price,
            "description": description
        }
        result.append(info)
    chosen_one = result[randrange(4, len(result) -1)]
    return chosen_one

def main(user_query):
    content = get_content_from_url(user_query)
    image_urls = parse_image_url(content= content, classes="hz-Listing hz-Listing--list-item hz-Listing--list-item-BNL16952", location="img", price_class="hz-Listing-price hz-Listing-price--mobile hz-text-price-label")
    print(image_urls)
    return image_urls