# HAS ISSSUES !!!!!!!

# Problem with driver (fix)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time
import shutil

def scrape_leetcode_profile(username):
    url = f"https://leetcode.com/{username}/"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Ensure chromedriver is found
    chromedriver_path = shutil.which("chromedriver")
    if not chromedriver_path:
        raise FileNotFoundError("Chromedriver not found. Ensure it is installed and added to PATH.")
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Allow some time for the page to load
        
        script_tag = driver.find_element(By.XPATH, "//script[contains(text(), 'window.__APOLLO_STATE__')]")
        json_text = script_tag.get_attribute("innerHTML").split("=", 1)[1].strip().rstrip(";")
        data = json.loads(json_text)
        
        # Extract key stats
        user_stats = None
        for key, value in data.items():
            if key.startswith("UserPublicProfileNode"):  # Finding user stats key
                user_stats = value
                break
        
        if not user_stats:
            return {"error": "Could not find user stats."}
        
        problem_counts = {
            "total_solved": user_stats.get("submitStats", {}).get("acSubmissionNum", [{}])[0].get("count", 0),
            "easy_solved": user_stats.get("submitStats", {}).get("acSubmissionNum", [{}])[1].get("count", 0),
            "medium_solved": user_stats.get("submitStats", {}).get("acSubmissionNum", [{}])[2].get("count", 0),
            "hard_solved": user_stats.get("submitStats", {}).get("acSubmissionNum", [{}])[3].get("count", 0)
        }
        
        skill_info = user_stats.get("skills", [])
        language_info = user_stats.get("languageProblemCount", [])
        
        return {
            "username": username,
            "problem_counts": problem_counts,
            "skills": skill_info,
            "languages": language_info
        }
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    username = "abhiramkaranth700"
    response = scrape_leetcode_profile(username)
    print(json.dumps(response, indent=4))