import feedparser
import json
import time
from datetime import datetime
from time import mktime

# Add your RSS feeds here
feeds = [
    {"source": "New York Times", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
    {"source": "The Atlantic", "url": "https://www.theatlantic.com/feed/all/"},
    {"source": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
    {"source": "The Verge", "url": "https://www.theverge.com/rss/index.xml"}
]

news_items = []

for feed in feeds:
    try:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries[:5]: # Get top 5 from each source
            
            # Handle timestamps carefully
            published_time = datetime.now().isoformat()
            if hasattr(entry, 'published_parsed'):
                published_time = datetime.fromtimestamp(mktime(entry.published_parsed)).isoformat()
            
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "source": feed["source"],
                "published": published_time
            })
    except Exception as e:
        print(f"Error parsing {feed['source']}: {e}")

# Sort by newest first
news_items.sort(key=lambda x: x['published'], reverse=True)

# Save to JSON
with open('news.json', 'w') as f:
    json.dump(news_items, f, indent=2)

print("News updated successfully.")
