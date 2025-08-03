import logging
from fastapi import FastAPI, HTTPException, Query
from typing import List
from .leetcode_scraper import scrape_leetcode_data
from .github_scraper import scrape_github_data, scrape_selected_repos

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
def get_leetcode_data(username: str):
    logger.info(f"Request received for LeetCode user: {username}")
    try:
        data = scrape_leetcode_data(username)
        logger.info(f"Successfully fetched data for {username}")
        return {"status": "success", "data": data}
    except Exception as e:
        logger.error(f"Error fetching data for {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/gitbub/{username}")
def get_github_data(username: str):
    logger.info(f"Request received for GitHub user: {username}")
    try:
        data = scrape_github_data(username)
        logger.info(f"Successfully fetched data for {username}")
        return {"status": "success", "data": data}
    except Exception as e:
        logger.error(f"Error fetching data for {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/gitbub/{username}")
def get_github_data(username: str):
    logger.info(f"Request received for GitHub user: {username}")
    try:
        data = scrape_github_data(username)
        logger.info(f"Successfully fetched data for {username}")
        return {"status": "success", "data": data}
    except Exception as e:
        logger.error(f"Error fetching data for {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/github/{username}/repos")
def get_selected_github_repos(username: str, repos: List[str] = Query(...)):
    logger.info(f"Request received for GitHub user: {username} with selected repos: {repos}")
    try:
        data = scrape_selected_repos(username, repos)
        logger.info(f"Successfully fetched selected repos for {username}")
        return {"status": "success", "data": data}
    except Exception as e:
        logger.error(f"Error fetching selected repos for {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

logger.info("main.py loaded and FastAPI app initialized")
