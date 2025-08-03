import requests
from typing import List
import base64

def scrape_github_data(username):
    base_url = "https://api.github.com"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    
    user_resp = requests.get(f"{base_url}/users/{username}")
    repos_resp = requests.get(f"{base_url}/users/{username}/repos")
    
    if user_resp.status_code != 200 or repos_resp.status_code != 200:
        return {"status": "error", "message": "User not found or API error"}

    user_data = user_resp.json()
    repos_data = repos_resp.json()
    top_repos = sorted(repos_data, key=lambda r: r.get('stargazers_count', 0), reverse=True)[:5]

    repos_info = []
    for repo in top_repos:
        readme_resp = requests.get(
            f"{base_url}/repos/{username}/{repo['name']}/readme", headers=headers
        )
        readme_content = readme_resp.text if readme_resp.status_code == 200 else "README not available"

        repos_info.append({
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "repo_url": repo["html_url"],
            "readme": readme_content
        })

    return {
        "status": "success",
        "data": {
            "profile": {
                "login": user_data["login"],
                "name": user_data.get("name"),
                "bio": user_data.get("bio"),
                "followers": user_data["followers"],
                "following": user_data["following"],
                "public_repos": user_data["public_repos"],
                "profile_url": user_data["html_url"],
                "avatar_url": user_data["avatar_url"]
            },
            "top_repositories": repos_info
        }
    }

def scrape_selected_repos(username: str, repo_names: List[str]) -> List[dict]:
    base_url = f"https://api.github.com/repos/{username}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    repo_data = []

    for repo in repo_names:
        repo_url = f"{base_url}/{repo}"
        readme_url = f"{repo_url}/readme"

        try:
            repo_resp = requests.get(repo_url, headers=headers)
            repo_resp.raise_for_status()
            repo_info = repo_resp.json()

            readme_resp = requests.get(readme_url, headers=headers)
            if readme_resp.status_code == 200:
                readme_content = readme_resp.json().get("content", "")
                readme_decoded = base64.b64decode(readme_content).decode("utf-8")

            else:
                readme_decoded = "README not available"

            repo_data.append({
                "name": repo_info.get("name"),
                "url": repo_info.get("html_url"),
                "stars": repo_info.get("stargazers_count"),
                "forks": repo_info.get("forks_count"),
                "language": repo_info.get("language"),
                "readme": readme_decoded
            })

        except requests.exceptions.RequestException as e:
            repo_data.append({
                "name": repo,
                "error": str(e)
            })

    return repo_data
