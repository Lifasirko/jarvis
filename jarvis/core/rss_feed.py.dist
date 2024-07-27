import feedparser


def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    # print("Fetched feed entries:", feed.entries)  
    news_items = []
    for entry in feed.entries:
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'published': entry.published
        })
    return news_items



rss_url = 'https://www.liga.net/news/all/rss.xml'
news_items = fetch_rss_feed(rss_url)
# print(news_items)  
