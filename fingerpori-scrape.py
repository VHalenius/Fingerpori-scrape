from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import time
from pathlib import Path
import os

DEFAULT = 'https://www.hs.fi/fingerpori/car-2000008287224.html'

def fingerpori_download():
    # Session headers for requests
    HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    # Default download dir:
    SAVE_DIR = Path.home() / "Fingerpori"

    # Ask for save location
    print('Mihin tallennetaan? Oletus = ' + str(SAVE_DIR))
    dir_input = input()
    if dir_input == "":
        save_dir = str(SAVE_DIR)
    else:
        save_dir = dir_input
    print(save_dir)

    if os.path.exists(save_dir):
        print('Hakemisto löytyy')
    else:
        print('hakemistoa ei löydy, luodaan')
        os.mkdir(save_dir)

    print('Syötä ensimmäisen sarjakuvan url:')
    print('Oletus=' + DEFAULT)
    url = input()
    if url == "":
        url = DEFAULT
    else:
        url = url

    print('Montako sarjakuvaa ladataan?')  
    comic_count = int(input())+1

    for i in range(1, comic_count):
        # create a soup object
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        
        # Get the title (name for images)
        title = soup.find('title')
        title = str(title).split(' - ')
        title = title[1]
        title = title.split('.')
        title = str(title[2]).zfill(4) + str(title[1]).zfill(2) + str(title[0].zfill(2))
        
        # Get link to previous comic
        img_url = 'https://www.hs.fi'
        for nested_soup in soup.find_all(class_="cartoon-container"):
            links = nested_soup.find_all(class_='article-navlink prev')
            links = str(links).split('href=')[-1].split('>')[0].split('\"')[1]
        previous = img_url + links
        
        # Get the comic url on current page
        for nested_soup in soup.find_all('figure', class_="cartoon image scroller"):   
            a = nested_soup.find_all('img', lambda tag:'data-simple-src')
        for image in a:
            return_image = image['data-srcset']
        return_image = 'https:' + str(return_image).split(' ')[0]
        
        # Show current task
        print('Päiväys: ', title)
        print('Sivun url: ', url)
        print('Sarjakuvan url:', return_image)
        
        # Try to download the comic
        session = requests.session()
        response = session.get(return_image, headers=HEADERS)
        print(response.status_code)
        save_file = os.path.join(save_dir, title + '.jpg')
        print(save_file)
        open(save_file, 'wb').write(response.content)
        
        # Set next url
        url = previous
        time.sleep(3)
        i+=1

if __name__ == "__main__":
    fingerpori_download()