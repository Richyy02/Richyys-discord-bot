import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random
import string
import requests
import io
from PIL import Image
from pathlib import Path
import hashlib

all_letters = string.ascii_letters

def random_prntscr_code():
    i = 0
    while i < 1:
        result = ""
        code_size = random.choice([5,6,7])
        if code_size == 5:
            if random.choice([True, False]):
                for _ in range(code_size):
                    if random.choice([True, False]):
                        result += str(random.randint(0,9))
                    else:
                        result += chr(random.randint(97,122))
                i += 1
            else:
                for _ in range(code_size):
                    if random.choice([True, False]):
                        result += str(random.randint(0,9))
                    else:
                        result += random.choice(all_letters)
                i += 1
        elif code_size == 6:
            for _ in range(code_size):
                    if random.choice([True, False]):
                        result += str(random.randint(0,9))
                    else:
                        result += chr(random.randint(97,122))
            i += 1
        else:
            for _ in range(code_size):
                    if random.choice([True, False]):
                        result += str(random.randint(0,9))
                    else:
                        result += random.choice(all_letters)
            i += 1
        print(result)
    return result
              
def get_content_from_url(code):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(f"https://prnt.sc/{code}")
    if driver.current_url == "https://prnt.sc/":
        print("Got 302, retrying...")
        return None
    page_content = driver.page_source
    driver.quit()
    return page_content

def parse_image_url(content, classes, location, source):
    soup = BeautifulSoup(content, features="html.parser")
    result = []
    for a in soup.find_all(attrs={"class": classes}):
        name = a.find(location)
        
        if name not in result:
            if(name.get(source)[:2]).startswith("//"):
                return None
            else:
                result.append(name.get(source))
            return result

def save_image_url_to_csv(image_urls):
    if isinstance(image_urls, list):
        df = pd.DataFrame({"links": image_urls})
    else:
        df = pd.DataFrame({"links": [image_urls]})
    df.to_csv("links.csv", index=False, encoding="utf-8")

def get_and_save_image_to_file(image_url, output_dir):
    try:
        response = requests.get(image_url)
        print(f'status code: {response.status_code}')
        print(f'response url: {response.url}')
        
        if response.url == "https://i.imgur.com/removed.png" or response.url == "https://imgur.com/error/404":
            print("Got removed picture, retrying...")
            return None
        
        image_content = response.content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        file_name = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
        file_path = output_dir / file_name
        image.save(file_path, "PNG", quality=80)

        return file_name
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
        return None
    
    except Exception:
        print("Got 404, retrying...")
        return None


def handle_response(message) -> str or None:
    p_message = message.lower()

    if p_message == 'random':
        file_name = main()
        if file_name is not None:
            print(f"Successfully returned something: {file_name}")
            return file_name[0]
        else:
            return None
    


def main():
    print("Searching for a picture...")
    code = random_prntscr_code()
    imgur = [f'https://i.imgur.com/{code}.png']
    if len(code) == 5:
        uppercase_count = 0
        for letter in code:
            if letter.isupper():
                uppercase_count += 1
        if uppercase_count == 0:
            content = get_content_from_url(code)
            image_urls = parse_image_url(content= content, classes="image-container image__pic js-image-pic", location="img",source="src")
            print("Doing the big scrape")
        else:
            image_urls = imgur
            print("No big scrape")
    elif len(code) == 6:
        content = get_content_from_url(code)
        image_urls = parse_image_url(content= content, classes="image-container image__pic js-image-pic", location="img",source="src")
        print("Doing the big scrape")
    else:
        image_urls = imgur
        print("No big scrape")
    
    if image_urls == None:
        return None
    print(f'IMG URLS IS: {image_urls}')
    save_image_url_to_csv(image_urls)

    file_names = []

    for image_url in image_urls:
        print("Processing image:", image_url)
        file_name = get_and_save_image_to_file(image_url, output_dir=Path("Images"))
        if file_name == None:
            return None
        file_names.append(file_name)

    return file_names