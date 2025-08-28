"""
Motor de scrapping - Lógica principal del scrapeado
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)


class ScrapperEngine:
    """
    Clase principal para hacer scrapping de sitios web
    """
    
    def __init__(self, max_depth=1, delay=1):
        self.max_depth = max_depth
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_url(self, url, depth=1):
        """
        Scrapeado principal de una URL
        
        Args:
            url (str): URL a scrapear
            depth (int): Profundidad del scrapeado
            
        Returns:
            dict: Datos extraídos de la página
        """
        try:
            logger.info(f"Scrapping URL: {url} (depth: {depth})")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'url': url,
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'headings': self._extract_headings(soup),
                'links': self._extract_links(soup, url),
                'images': self._extract_images(soup, url),
                'text_content': self._extract_text(soup),
                'status_code': response.status_code,
                'scraped_at': str(response.headers.get('Date', ''))
            }
            
            logger.info(f"Successfully scraped {url}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error scrapping {url}: {e}")
            raise Exception(f"Error accessing URL: {e}")
        except Exception as e:
            logger.error(f"Unexpected error scrapping {url}: {e}")
            raise
    
    def _extract_title(self, soup):
        """Extraer título de la página"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ''
    
    def _extract_description(self, soup):
        """Extraer descripción meta"""
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            return desc_tag.get('content', '').strip()
        return ''
    
    def _extract_headings(self, soup):
        """Extraer todos los headings (h1, h2, h3, etc.)"""
        headings = []
        for i in range(1, 7):  
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
        return headings
    
    def _extract_links(self, soup, base_url):
        """Extraer todos los enlaces"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            links.append({
                'url': full_url,
                'text': link.get_text().strip(),
                'is_external': self._is_external_link(full_url, base_url)
            })
        return links[:50]  
    
    def _extract_images(self, soup, base_url):
        """Extraer todas las imágenes"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            full_url = urljoin(base_url, src)
            images.append({
                'url': full_url,
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return images[:20]  
    
    def _extract_text(self, soup):
        """Extraer texto plano de la página"""
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        text = ' '.join(line for line in lines if line)
        
        return text[:2000]  
    
    def _is_external_link(self, url, base_url):
        """Verificar si un enlace es externo"""
        return urlparse(url).netloc != urlparse(base_url).netloc