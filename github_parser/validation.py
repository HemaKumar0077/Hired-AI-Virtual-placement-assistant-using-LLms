import requests
from bs4 import BeautifulSoup

def get_user_repositories(username):
    repos = []
    page = 1

    while True:
        url = f"https://github.com/{username}?page={page}&tab=repositories"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        repo_elements = soup.find_all('a', itemprop='name codeRepository')

        if not repo_elements:
            break

        for repo in repo_elements:
            repo_name = repo.text.strip()
            repos.append(repo_name)

        page += 1

    return repos



