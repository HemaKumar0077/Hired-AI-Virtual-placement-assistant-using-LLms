import requests
from bs4 import BeautifulSoup

def scrape_readme_from_blob(username, repository, branch):
    """
    Scrape the README.md content from the GitHub blob page for a given branch.
    """
    url = f"https://github.com/{username}/{repository}/blob/{branch}/README.md"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/115.0.0.0 Safari/537.36")
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page for branch '{branch}' (status code: {response.status_code}).")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Try to find the rendered markdown content inside an <article> tag.
    article = soup.find("article", class_="markdown-body")
    if article:
        return article.get_text(separator="\n", strip=True)
    
    # Fallback: sometimes GitHub displays file contents in a table.
    table = soup.find("table", class_="js-file-line-container")
    if table:
        lines = table.find_all("td", class_="blob-code blob-code-inner")
        return "\n".join(line.get_text() for line in lines)
    
    print(f"Couldn't locate README content on the page for branch '{branch}'.")
    return None

def scrape_readme(username, repository):
    """
    Try scraping the README.md content from both 'main' and 'master' branches.
    """
    for branch in ["main", "master"]:
        print(f"Trying branch: {branch}")
        readme_content = scrape_readme_from_blob(username, repository, branch)
        if readme_content:
            return branch, readme_content
    return None, None


