import requests

def scrape_github_data(username):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"
    
    user_resp = requests.get(user_url)
    repos_resp = requests.get(repos_url)
    
    if user_resp.status_code != 200 or repos_resp.status_code != 200:
        return {"status": "error", "message": "User not found or API error"}

    user_data = user_resp.json()
    repos_data = repos_resp.json()

    top_repos = sorted(repos_data, key=lambda r: r.get('stargazers_count', 0), reverse=True)

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
            "top_repositories": [{
                "name": repo["name"],
                "description": repo["description"],
                "language": repo["language"],
                "stars": repo["stargazers_count"],
                "repo_url": repo["html_url"]
            } for repo in top_repos[:5]]
        }
    }
