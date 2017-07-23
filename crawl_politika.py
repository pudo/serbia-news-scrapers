import requests
from lxml import html
import feedparser

from common import articles, selector_text, element_text, emit_article


def scrape_article(url):
    # url = url.replace('/scc/', '/sr/')
    res = requests.get(url)
    doc = html.fromstring(res.content)
    article = doc.find('.//article')

    if article is None:
        return

    data = {
        'source': 'politika.rs',
        'url': url,
        'title': selector_text(article, 'h1'),
        'teaser': selector_text(article, '.h4'),
        'text': selector_text(article, '.article-content'),
    }

    for h6 in article.cssselect('.h6.gray'):
        byline = element_text(h6)
        if ', ' in byline:
            data['author'], data['date'] = byline.rsplit(', ', 1)

    emit_article(data)


def scrape_feed():
    feed = feedparser.parse('http://www.politika.rs/rss/')
    article_id = 0
    for entry in feed.entries:
        link = entry.get('link')
        _, part = link.split('/clanak/', 1)
        part, _ = part.split('/', 1)
        article_id = int(part)
        break

    for i in range(article_id, article_id - 2000, -1):
        link = 'http://www.politika.rs/sr/clanak/%s/' % i
        scrape_article(link)


if __name__ == '__main__':
    scrape_feed()
