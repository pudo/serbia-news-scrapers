import dataset
from normality import collapse_spaces, ascii_text

engine = dataset.connect('sqlite:///articles.sqlite3')
articles = engine['articles']


def selector_text(el, selector):
    if el is None:
        return
    for match in el.cssselect(selector):
        return element_text(match)


def element_text(el):
    text = el.text_content().strip()
    return collapse_spaces(text)


def emit_article(data):
    texts = (data.get('title'),
             data.get('teaser'),
             data.get('text'))
    norm_text = '; '.join([t for t in texts if t is not None])
    data['norm_text'] = collapse_spaces(norm_text.lower())
    print data.get('source'), data.get('title')
    articles.upsert(data, ['url'])
