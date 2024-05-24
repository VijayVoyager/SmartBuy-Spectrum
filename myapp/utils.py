import imp
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
from .url_parser import UrlParseSe


headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'}


def flipkart(name):
    try:
        name1 = name.replace(" ","+")
        flipkart_link = f'https://www.flipkart.com/search?q={name1}'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'}
        res = requests.get(flipkart_link, headers=headers)

        print("\nSearching on Flipkart....")
        soup = BeautifulSoup(res.text, 'html.parser')

        flipkart_price = '0'
        flipkart_name = 'N/A'
        flipkart_image = 'N/A'

        if soup.select('.tUxRFH'):
            flipkart_name = soup.select('.KzDlHZ')[0].getText().strip().upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('.Nx9bqj _4b5DiR')[0].getText().strip()
                flipkart_image = soup.select('.DByuf4')[0]['src']
        elif soup.select('.s1Q9rs'):
            flipkart_name = soup.select('.s1Q9rs')[0].getText().strip().upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                flipkart_image = soup.select('._396cs4._3exPp9')[0]['src']

        return flipkart_price, flipkart_name[0:50], flipkart_image, flipkart_link

    except Exception as e:
        print("Error:", e)
        return '0', 'N/A', 'N/A', 'N/A'


def amazon(name):
    try:
        global amazon
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon=f'https://www.amazon.in/{name1}/s?k={name2}'
        amazon_link = amazon 
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
        print("\nSearching in amazon...")
        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_images = soup.select('.a-section.aok-relative.s-image-fixed-height')
                amazon_image = amazon_images[0].find_all('img', class_='s-image')[0]
                amazon_image = amazon_image['src']
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                print("Amazon:")
                print(amazon_name)
                print("₹"+amazon_price)
                print("---------------------------------")
                break
            else:
                i+=1
                i=int(i)
                if i==amazon_page_length:
                    amazon_price = '0'
                    print("amazon : No product found!")
                    print("-----------------------------")
                    break

        return amazon_price, amazon_name[0:50], amazon_image, amazon_link
    except:
        print("Amazon: No product found!")
        print("---------------------------------")
        amazon_price = '0'
        amazon_name = 'N/A'
        amazon_link = 'N/A'
        amazon_image = 'N/A'
    return amazon_price, amazon_name[0:50], amazon_image, amazon_link




def gadgetsnow(name):
    try:
        global gadgetsnow
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        gadgetsnow=f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={name2}'
        gadgetsnow_link = gadgetsnow
        res = requests.get(f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={name2}',headers=headers)
        print("\nSearching in gadgetsnow...")
        soup = BeautifulSoup(res.text,'html.parser')
        gadgetsnow_page = soup.select('.product-name')
        gadgetsnow_page_length = int(len(gadgetsnow_page))

        for i in range(0,gadgetsnow_page_length):
            name = name.upper()
            gadgetsnow_name = soup.select('.product-name')[i].getText().strip().upper()
            if name in gadgetsnow_name:
                gadgetsnow_name = soup.select('.product-name')[i].getText().strip()
                images = soup.select('.product-img-align')[i]
                image = images.select('.lazy')[0]
                gadgetsnow_image = image['data-original']
                gadgetsnow_price = soup.select('.offerprice')[i].getText().strip().upper()
                gadgetsnow_price = "".join(gadgetsnow_price)
                gadgetsnow_price = gadgetsnow_price[1:]
                print("GadgetSnow:")
                print(gadgetsnow_name)
                gadgetsnow_price = "₹"+gadgetsnow_price
                print("---------------------------------")
                break
            else:
                i+=1
                i=int(i)
                if i==gadgetsnow_page_length:
                    gadgetsnow_price = '0'
                    print("GadgetSnow : No product found!")
                    print("-----------------------------")
                    break

        return gadgetsnow_price, gadgetsnow_name[0:50], gadgetsnow_image, gadgetsnow_link
    except:
        print("GadgetSnow: No product found!")
        print("---------------------------------")
        gadgetsnow_price = '0'
        gadgetsnow_name = 'N/A'
        gadgetsnow_image = 'N/A'
        gadgetsnow_link = 'N/A'
    return gadgetsnow_price, gadgetsnow_name[0:50], gadgetsnow_image, gadgetsnow_link


def croma(name):
    try:
        global croma
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        croma= f"https://www.croma.com/searchB?q={name1}%3Arelevance&text={name2}"
        source = croma
        croma_link = croma
        wait_imp = 10
        CO = webdriver.ChromeOptions()
        CO.add_experimental_option('useAutomationExtension', False)
        CO.add_argument('--ignore-certificate-errors')
        CO.add_argument('--start-maximized')
        print("Driver path", str(settings.BASE_DIR)+'\chromedriver.exe')
        wd = webdriver.Chrome(r''+str(settings.BASE_DIR)+'\chromedriver.exe', options=CO)


        wd.get(source)
        wd.implicitly_wait(wait_imp)
        
        try:
            elementname = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.product-title.plp-prod-title"))
            )
            elementprice = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.amount"))
            )
            imgelement = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-img.plp-card-thumbnail img"))
            )
        except:
            wd.quit()
            

        croma_name = elementname.text
        croma_price = elementprice.text
        croma_image = imgelement.get_attribute("src")
        return croma_price, croma_name[0:50], croma_image, croma_link
    except:
        print("Croma: No product found!")
        print("---------------------------------")
        croma_price = '0'
        croma_name = 'N/A'
        croma_image = 'N/A'
        croma_link = 'N/A'
    return croma_price, croma_name[0:50], croma_image, croma_link
    

    
    
def reliance(name):
    try:
        global reliance
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        reliance=f'https://www.reliancedigital.in/search?q={name2}:relevance'
        reliance_link = reliance
        res = requests.get(f'https://www.reliancedigital.in/search?q={name2}:relevance',headers=headers)
        print("\nSearching in reliance...")
        soup = BeautifulSoup(res.text,'html.parser')
        reliance_page = soup.select('.sp__name')
        article_block = soup.find_all('div',class_='slider-text')
        reliance_data = article_block[0].getText().strip()[article_block[0].getText().strip().index('₹')+1:]
        reliance_price = ""
        for i in reliance_data:
            if i.isnumeric() or i == ',':
                reliance_price += i
            else:
                break
        images = soup.find_all('img', class_='img-responsive')
        reliance_image = "https://www.reliancedigital.in/"+images[0]['data-srcset']
        reliance_page_length = int(len(reliance_page))
        for i in range(0,reliance_page_length):
            name = name.upper()
            reliance_name = soup.select('.sp__name')[i].getText().strip().upper()
            if name in reliance_name:
                reliance_name = soup.select('.sp__name')[i].getText().strip()
                print("Reliance:", reliance_price)
                print(reliance_name)
                print(reliance_image)
                print("₹"+reliance_price)
                print("---------------------------------")
                break
            else:
                i+=1
                i=int(i)
                if i==reliance_page_length:
                    reliance_price = '0'
                    print("reliance : No product found!")
                    print("-----------------------------")
                    break

        return reliance_price, reliance_name[0:50], reliance_image, reliance_link
    except:
        print("Reliance: No product found!")
        print("---------------------------------")
        reliance_price = '0'
        reliance_image = 'N/A'
        reliance_name = 'N/A'
        reliance_link = 'N/A'
    return reliance_price, reliance_name[0:50], reliance_image, reliance_link

def convert(a):
    b=a.replace(" ",'')
    c=b.replace("INR",'')
    d=c.replace(",",'')
    d=d.replace("`",'')
    f=d.replace("₹",'')
    g=int(float(f))
    return g