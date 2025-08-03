import logging
from fastapi import FastAPI, HTTPException
from .leetcode_scraper import scrape_user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),    
        logging.StreamHandler()             
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    return {"message": "LeetCode Scraper API is running!"}

@app.get("/leetcode/{username}")
def get_user_data(username: str):
    logger.info(f"Request received for LeetCode user: {username}")
    try:
        data = scrape_user(username)
        logger.info(f"Successfully fetched data for {username}")
        return {"status": "success", "data": data}
    except Exception as e:
        logger.error(f"Error fetching data for {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

logger.info("main.py loaded and FastAPI app initialized")
