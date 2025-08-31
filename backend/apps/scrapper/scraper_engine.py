import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import lxml
import statistics
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service

os.environ['SELENIUM_CACHE_PATH'] = '/tmp/selenium-cache'

logger = logging.getLogger('django')

class ScrapperEngine:

    
    def __init__(self, max_depth=1, delay=1):
        self.max_depth = max_depth
        self.delay = delay
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        })
    
    def setup_selenium_driver(self):
        """Configure Chrome driver for dynamic Booking scraping"""
        if not self.driver:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            chrome_options.add_argument('--user-data-dir=/tmp/chrome-user-data')
            chrome_options.add_argument('--cache-dir=/tmp/chrome-cache')
            
            chrome_options.binary_location = '/usr/bin/chromium'
            
            try:
                driver_path = '/usr/bin/chromedriver'
                service = None
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info(f"Successfully initialized driver with {driver_path}")
                    
            except Exception as e:
                logger.error(f"Error setting up Chromium driver: {e}")
                try:
                    self.driver = webdriver.Chrome(options=chrome_options)
                except Exception as e2:
                    logger.error(f"Error with fallback: {e2}")
                    raise Exception("Could not initialize Chrome/Chromium driver")
        
        return self.driver
    
    def close_selenium_driver(self):
        """Close the Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_booking_images(self, hotel_url, wait_seconds=10):
        """Specific scraping for hotel images on Booking"""
        try:
            driver = self.setup_selenium_driver()
            driver.get(hotel_url)
            
            WebDriverWait(driver, wait_seconds).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            images = []
            
            try:
                 
                gallery_button = None
                gallery_button= WebDriverWait(driver,wait_seconds).until(EC.element_to_be_clickable((By.XPATH,"//span[contains(@class,'e7addce19e') and contains(@class,'f77a73f1ba') and contains(@class,'fab9d44163') and contains(@class,'a8a1bbacc0') and contains(@class,'f6845188a6')]/parent::div/button")))

                if gallery_button:
                    driver.execute_script("arguments[0].click();", gallery_button)
                else:
                    raise TimeoutException("No se encontró botón de galería")
                
                WebDriverWait(driver, wait_seconds).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img.f6c12c77eb.c0e44985a8.c09abd8a52.ca3dad4476'))
                )
                
                image_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="gallery-modal-grid"] img.f6c12c77eb.c0e44985a8.c09abd8a52.ca3dad4476')
                
            except Exception as e:
                raise (e)

            for img_element in image_elements:
                try:
                    src = img_element.get_attribute('src')
                    if src and ('cf.bstatic.com' in src or 'booking.com' in src):
                        high_quality_url = src.replace('max300', 'max1024x768').replace('max500', 'max1024x768')
                        images.append(high_quality_url)
                    elif src:
                        images.append(src)
                        
                except Exception as e:
                    logger.warning(f"Error extracting image: {e}")
                    continue
            
            return images  
            
        except Exception as e:
            logger.error(f"Error en scraping de imágenes con Selenium: {e}")
            return []
        finally:
            self.close_selenium_driver()

    def scrape_url(self, url, depth=1):

        try:
            logger.info(f"Scrapping URL: {url} (depth: {depth})")
            
            response_soup = self._get_response_soup(url)

            first_hotel_link = response_soup.find('div', role="listitem").find('a', class_="bd77474a8e").get('href') # type: ignore

            first_page_soup = self._get_response_soup(first_hotel_link)

            data = {
                'name': self._extract_hotel_name(first_page_soup),
                'location': self._extract_hotel_localtion(first_page_soup),
                'average_price': self._extract_hotel_average_price(first_page_soup),
                'description': self._extract_hotel_description(first_page_soup),
                'review_mark': self._extract_hotel_review_mark(first_page_soup),
                'photo_urls': self.scrape_booking_images(first_hotel_link),
                'comments': self._extract_hotel_number_of_comments(first_page_soup),
                'amenities': self._extract_hotel_amenities(first_page_soup),
            }
            
            logger.info(f"Successfully scraped {url}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error scrapping {url}: {e}")
            raise Exception(f"Error accessing URL: {e}")
        except Exception as e:
            logger.error(f"Unexpected error scrapping {url}: {e}")
            raise
    
    
    def _get_response_soup(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Error scrapping {url}: {e}")
            raise Exception(f"Error accessing or scrapping URL: {e}")
        
    def _extract_hotel_name(self, soup):
        """Extract page title"""
        h2_tag = soup.find('h2', class_="ddb12f4f86 pp-header__title")
        return h2_tag.get_text().strip() if h2_tag else ''

    def _extract_hotel_localtion(self, soup):
        """Extract hotel location"""
        div_location_tag = soup.find('div', class_="b99b6ef58f cb4b7a25d9 b06461926f")
        return div_location_tag.find(text=True, recursive=False).strip() if div_location_tag else ''

    def _extract_hotel_description(self, soup):
        """Extract hotel description"""
        p_description_tag = soup.find('p',class_="b99b6ef58f f1152bae71")
        return p_description_tag.get_text().strip() if p_description_tag else ''
    
    def _extract_hotel_review_mark(self, soup):
        """Extract hotel review rating"""
        review_mark_tag = soup.find('div', class_='f63b14ab7a dff2e52086')
        if review_mark_tag:
            return round(float(review_mark_tag.get_text().strip().replace(',','.')),2)
        return ''
    
    def _extract_hotel_number_of_comments(self, soup):
        """Extract number of comments"""
        comments = soup.find('div', class_='fff1944c52 fb14de7f14 eaa8455879')
        if comments:
            return int(comments.get_text().strip().split()[0].replace('.',''))
        return ''

    
    def _extract_hotel_amenities(self, soup):
        """Extract hotel amenities"""
        amenities = []
        for amenitie in soup.find_all('div', class_='b99b6ef58f b2b0196c65'):
            amenitie_text = amenitie.get_text().strip()
            amenities.append(amenitie_text)
        return amenities
        
    def _extract_hotel_average_price(self, soup):
        """Extract hotel average price"""
        prices = []
        for price in soup.find_all('span', class_='prco-valign-middle-helper'):
            price_text = re.findall(r'\d+',price.get_text())
            price = float(price_text[0].replace(',','.')) if price_text else 0.00
            prices.append(price)
        return round(statistics.mean(prices),2) if prices else 0.00
