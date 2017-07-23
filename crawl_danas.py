import requests
from lxml import html
import feedparser

from common import articles, selector_text, element_text, emit_article


def scrape_article(url):
    res = requests.get(url)
    doc = html.fromstring(res.content.decode('utf-8'))
    article = doc.cssselect('.articleBox')
    if not len(article):
        return
    article = article[0]

    data = {
        'source': 'danas.rs',
        'url': url,
        'title': selector_text(article, 'h1.title'),
        'teaser': selector_text(article, 'p.lead'),
        'author': selector_text(article, 'div.author'),
        'date': selector_text(article, 'div.published'),
        'text': selector_text(doc, '.articleBox'),
    }
    emit_article(data)


def scrape_feed():
    feed = feedparser.parse('http://www.danas.rs/aspx/rss/rss.aspx')
    article_id = 0
    for entry in feed.entries:
        link = entry.get('link')
        _, news_id = link.rsplit('news_id=', 1)
        news_id, _ = news_id.split('&', 1)
        article_id = int(news_id)
        # break

    for i in range(article_id, article_id - 1000, -1):
        link = 'http://www.danas.rs/drustvo.55.html?news_id=%s&title=' % i
        scrape_article(link)


if __name__ == '__main__':
    scrape_feed()
