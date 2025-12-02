import feedparser
import json
from datetime import datetime, timedelta, timezone
# We no longer need mktime or time

# Add your RSS feeds here
# Note: Some feeds might be unreliable with times. These generally work well.
feeds = [
    {"source": "The Business Standard", "url": "https://www.tbsnews.net/bangladesh/rss.xml"},
    {"source": "New York Times", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
    {"source": "The Atlantic", "url": "https://www.theatlantic.com/feed/all/"},
    {"source": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml"},
    {"source": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
    {"source": "NPR", "url": "https://feeds.npr.org/1001/rss.xml"}
]

news_items = []

# Define "now" in UTC timezone
utc_now = datetime.now(timezone.utc)
# Define the cutoff point (24 hours ago)
twenty_four_hours_ago = utc_now - timedelta(hours=24)

print(f"Fetching news newer than: {twenty_four_hours_ago.isoformat()}")

for feed in feeds:
    print(f"Checking {feed['source']}...")
    try:
        # Use a custom User-Agent to avoid being blocked by some sites
        parsed = feedparser.parse(feed["url"], agent="Mozilla/5.0 (compatible; NewsAggregator/1.0)")
        
        # We check more entries now since we are filtering by time later
        for entry in parsed.entries[:30]: 
            
            published_dt = None

            # 1. Try parsing the published date correctly into UTC
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                # feedparser returns a time struct in UTC. Convert to timezone-aware datetime.
                published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                # Fallback to updated time if published time fails
                 published_dt = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

            # 2. Filter: Check if date exists AND is newer than 24 hours ago
            if published_dt and published_dt > twenty_four_hours_ago:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": feed["source"],
                    # Save as ISO format string, which JS can parse easily
                    "published": published_dt.isoformat()
                })

    except Exception as e:
        print(f"Error parsing {feed['source']}: {e}")

# Sort by newest first based on the ISO string comparison
news_items.sort(key=lambda x: x['published'], reverse=True)

print(f"Found {len(news_items)} articles from the last 24 hours.")

# Save to JSON
with open('news.json', 'w') as f:
    json.dump(news_items, f, indent=2)

