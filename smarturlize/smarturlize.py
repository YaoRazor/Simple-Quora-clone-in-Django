import re
import urlparse

from .transformers import registry


class Word(object):

    def __init__(self, word):
        self.word = word
        self.get_url()

    def get_url(self):
        self.is_url = bool(re.match(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]'
            '[0-9a-fA-F]))+', self.word
        ))
        self.url = self.is_url and urlparse.urlparse(self.word) or None


class SmartUrlize(object):

    def get_transformers(self):
        if self.include:
            # If include is specified then exclude will be ignored
            transformers = dict((t.__name__, t) for t in registry)
            return [transformers[n]() for n in self.include]
        return [t() for t in registry if t.__name__ not in self.exclude]

    def transform_word(self, word):
        for t in self.transformers:
            if (word.is_url or not t.is_url_handler) and t.match(word):
                return t.transform(word)
        return word.word

    def transform(self):
        self.words = [Word(w) for w in self.text.split(' ')]
        self.transformers = self.get_transformers()
        for i, w in enumerate(self.words):
            self.words[i] = self.transform_word(w)

    def __call__(self, text, exclude=None, include=None):
        self.exclude = exclude or []
        self.include = include or []
        self.text = text
        self.transform()
        return ' '.join(self.words)
