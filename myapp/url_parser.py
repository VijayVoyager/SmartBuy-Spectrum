from requests import get
from requests.exceptions import ConnectionError
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from django.conf import settings
from pathlib import Path


class UrlParseSe:
    def __init__(self, url: str) -> None:
        self.url = url
    
    def urlopen(self):
        try:
            var = "NoError"
            read = get(self.url)
            # requests.sessions().close()
        except HTTPError as e:
            var = "HTTPError"
        except URLError as e:
            var = "URLError"
        except ConnectionError as e:
            var = "ConnectionError"
        if var == "NoError":
            return read.status_code, True 
        else:
            return var, False
    
    def parse(self):
        status, error = self.urlopen()
        if error:
            try:
                driver = webdriver.Firefox()
            except WebDriverException as e:
                print("Firefox Driver not installed properly\nCustom Driver Setted up\n> Driver: mozilla/geckodriver\n> version:0.30.0\n")
                exec_path = str(Path(settings.BASE_DIR / 'myapp' / 'Drivers'/ 'geckodriver'))
                options = Options()
                print(exec_path)
                driver = webdriver.Firefox(executable_path=exec_path, options=options)
            except:
                return "Firefox Driver Not installed"
            driver.get(self.url)
            source = driver.page_source
            driver.quit()
            return BeautifulSoup(source, 'lxml')
        else:
            return "Error while occuring with code "+status
 
# products = soup.select('.tUxRFH')
# title = soup.select('.KzDlHZ')[0].text
# price = soup.select('.Nx9bqj _4b5DiR')[0].text
# rating = soup.select('.XQDdHH')[0].text
# picture = soup.select('.DByuf4')[0]['src']

#def flipkart(name):
 #   result = []
 #   try:
 #       url = f'https://www.flipkart.com/search?q={name}'
 #       url_parser = UrlParseSe(url)
 #       soup = url_parser.parse()
 #       products = soup.select('.tUxRFH')
 #       for i in products: 
 #           data = {}
 #           if (len(soup.select('.KzDlHZ'))):
 #               data['title'] = soup.select('.KzDlHZ')[i].getText().strip().upper()
 #           else:
 #               data['title'] = 'Unknown'
 #           
 #           if (len(soup.select('._4b5DiR'))):
 #               data['price'] = soup.select('._4b5DiR')[i].getText().strip()
 #           else:
 #               data['price'] = 'Unknown'
 #               
 #           if (len(soup.select('.XQDdHH'))):
 #               data['rating'] = soup.select('.XQDdHH')[i].getText().strip()
 #           else:
 #               data['rating'] = 'Unknown'
 #           
 #           if (len(soup.select('._4WELSP'))):
 #               fk_images = soup.select('._4WELSP') #keep edit
 #               fk_image = fk_images[0].find_all('img', class_='DByuf4')[0]
 #               data['image'] = fk_image['src']
 #               #data['image'] = soup.select('.DByuf4')[i]['src']
 #           else:
 #               data['image'] = 'Unknown'
 #       
 #           result.append(data)
 #       print(result)
 #    except Exception as error:
 #       print(error)
 #       print('Flipkart parse fail')
        
 #   return result

