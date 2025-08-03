import cloudscraper
import logging
from lxml import html

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

def scrape_user(username: str) -> dict:
    url = f"https://leetcode.com/{username}/"
    logger.info(f"Scraping URL: {url}")

    try:
        scraper = cloudscraper.create_scraper()
        logger.debug("Cloudscraper instance created.")
        
        response = scraper.get(url)
        logger.info(f"Received response with status code: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Failed to fetch the page. Status code: {response.status_code}")
            raise Exception(f"Failed. Status code: {response.status_code}")

        tree = html.fromstring(response.content)
        title = tree.xpath('//title/text()')
        if not title:
            logger.warning("No <title> tag found.")
            raise Exception("Page title not found.")
        
        page_title = title[0].strip()
        logger.info(f"Page title: {page_title}")

        return {
            "url": url,
            "page_title": page_title
        }
    
    except Exception as e:
        logger.exception("An error occurred while scraping.")
        raise
