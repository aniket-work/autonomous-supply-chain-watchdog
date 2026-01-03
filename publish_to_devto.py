import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("DEVTO_API_KEY")
ARTICLE_PATH = "supply_chain_watchdog/article.md"

if not API_KEY:
    print("❌ Error: DEVTO_API_KEY not found in .env file.")
    sys.exit(1)

def publish_article():
    if not os.path.exists(ARTICLE_PATH):
        print(f"❌ Error: Article file not found at {ARTICLE_PATH}")
        sys.exit(1)
        
    with open(ARTICLE_PATH, "r") as f:
        article_content = f.read()
        
    # Check for frontmatter
    if "published: true" not in article_content:
        print("⚠️ Warning: 'published: true' not found in frontmatter. Article might be saved as draft.")
    
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "article": {
            "body_markdown": article_content
        }
    }
    
    print("🚀 Publishing article to Dev.to...")
    
    response = requests.post("https://dev.to/api/articles", json=payload, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Success! Article published.")
        print(f"🔗 URL: {data['url']}")
    else:
        print(f"❌ Failed to publish article. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    publish_article()
