from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random
import requests
import time

def handle_response(message):
    p_message = message.lower()

    if p_message == "movie":
        title_code = random_title()
        url = scrape_status(title_code)
        return url

def random_title():
    i = 0
    while i < 1:
        result = ""
        code_size = random.choice([7,8])
        for _ in range(code_size):
            result += str(random.randint(0,9))
        i += 1
    return result

def scrape_status(title_code):
    url = f"https://www.imdb.com/title/tt{title_code}"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    print(url)
    status = requests.get(url, headers=header).status_code
    print(status)
    if status == 404:
        return None
    elif status == 200:
        return url

def get_content_from_url(url):
    print(f"GETTING URL FROM {url}")
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    current_scroll = 0
    scroll_amount = 350 
    
    while current_scroll < 300000:
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        current_scroll += scroll_amount
    time.sleep(1)
    page_content = driver.page_source
    driver.quit()
    return page_content

def parse_content(content, classes, location):
    soup = BeautifulSoup(content, features="html.parser")
    result = []
    series_title = "sc-2a168135-0 bTLVGY"
    movie_title = "sc-d8941411-0 dxeMrU"
    episode = "sc-d8941411-0 khgJYk"
    episode2 = "sc-d8941411-0 eXnKZM"
    image = "ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img"
    story_line = "ipc-html-content ipc-html-content--base sc-9eebdf80-1 cGAJeq"
    
    for element in soup.find_all(attrs={"class": classes}):
        try:
            print("I hit the loop!")
            if element.find("div", class_=series_title) != None:
                if element.find('h1', class_=movie_title) == None:
                    if element.find('h1', class_=episode) == None:
                        episode = element.find('h1', class_=episode2).text.strip()
                    else:
                        episode = element.find('h1', class_=episode).text.strip()
                else:
                    episode = element.find('h1', class_=movie_title).text.strip()
                
                title = element.find("div", class_=series_title).text.strip()

            else:
                if element.find('h1', class_=movie_title) == None:
                    title = element.find('h1', class_=episode).text.strip()
                else:
                    title = element.find('h1', class_=movie_title).text.strip()
                
                episode = ""

            #PICTURE
            if element.find("div", class_=image) == None:
                src = ""
            else:
                src = element.find("div", class_=image).find(location).get("src")
            #DESCRIPTION        
            if element.find("div", class_=story_line) == None:
                description = ""
            else:
                description = element.find("div", class_=story_line).text.strip()    
                    
            info = {
                "title": title,
                "episode": episode,
                "src": src,
                "story_line": description
            }
            print("I added the info data to result")

            result.append(info)
            print(f"RESULT IN PARSE_CONTENT FUNCTION IS: {result}")
        except Exception as e:
            print(f"Idk what happend but this happend: {e}")
    return result
    

def main(url):
    content = get_content_from_url(url)
    movie_info = parse_content(content=content, classes="ipc-page-wrapper ipc-page-wrapper--base", location="img")
    return movie_info

