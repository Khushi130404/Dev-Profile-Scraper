import cloudscraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_leetcode_data(username: str) -> dict:
    url = "https://leetcode.com/graphql"
    logger.info(f"Querying profile for: {username}")

    payload = {
        "operationName": "getUserProfile",
        "variables": {"username": username},
        "query": """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
                profile {
                    ranking
                    reputation
                    realName
                }
                tagProblemCounts {
                    advanced {
                        tagName
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        problemsSolved
                    }
                }
            }
        }
        """
    }

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url, json=payload)
        logger.info(f"Response status code: {response.status_code}")

        if response.status_code != 200:
            logger.error("Failed to get data")
            raise Exception("GraphQL API error")

        data = response.json()["data"]["matchedUser"]

        result = {
            "username": data["username"],
            "ranking": data["profile"]["ranking"],
            "reputation": data["profile"]["reputation"],
            "submission_stats": data["submitStatsGlobal"]["acSubmissionNum"],
            "topics_practiced": {
                "fundamental": data["tagProblemCounts"]["fundamental"],
                "intermediate": data["tagProblemCounts"]["intermediate"],
                "advanced": data["tagProblemCounts"]["advanced"]
            }
        }

        return result

    except Exception as e:
        logger.exception("Error fetching user profile")
        raise
