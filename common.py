import dataset
from normality import collapse_spaces

engine = dataset.connect('sqlite:///articles.sqlite3')
articles = engine['articles']


def selector_text(el, selector):
    for match in el.cssselect(selector):
        return element_text(match)


def element_text(el):
    text = el.text_content().strip()
    return collapse_spaces(text)
