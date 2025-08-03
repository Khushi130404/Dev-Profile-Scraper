# Dev-Profile-Scraper

- .\venv\Scripts\Activate.ps1
- pip freeze > requirements.txtpip install -r requirements.txt
- uvicorn app.main:app --reload
- http://127.0.0.1:8000/docs

### File Structure :

DevProfileScraper/
├── app/ # All app logic here
│ ├── **init**.py
│ ├── main.py # FastAPI app entry point
│ ├── github_scraper.py # GitHub profile scraping logic
│ ├── leetcode_scraper.py # LeetCode scraping logic
│ ├── models.py # Pydantic models for responses
│ └── utils.py # Optional: helper functions
│
├── venv/ # Your virtual environment (ignored)
│
├── requirements.txt # Python dependencies
├── .gitignore # Ignore venv, pycache, etc.
├── README.md # Project description
