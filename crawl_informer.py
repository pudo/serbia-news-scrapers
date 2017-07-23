import requests
from lxml import html
import feedparser

from common import articles, selector_text, element_text


def scrape_article(url):
    res = requests.get(url)
    doc = html.fromstring(res.content)
    title = selector_text(doc, 'title')
    title, _ = title.rsplit(' - ', 1)
    dates = [element_text(d) for d in doc.cssselect('span.singlepost-hd-date')]
    author, date = None, None
    if len(dates) == 2:
        author, date = dates

    data = {
        'source': 'informer.rs',
        'url': url,
        'title': selector_text(doc, '.singlepost-title'),
        'teaser': selector_text(doc, '.singlepost-subtitle'),
        'date': date,
        'author': author,
        'text': selector_text(doc, '.singlepost-text')
    }
    if not data['text']:
        return
    articles.upsert(data, ['url'])



def scrape_feed():
    feed = feedparser.parse('http://informer.rs/rss/vesti')
    for entry in feed.entries:
        scrape_article(entry.get('link'))


if __name__ == '__main__':
    scrape_feed()
