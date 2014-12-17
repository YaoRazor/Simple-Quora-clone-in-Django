import re
import urlparse


class BaseTransformer(object):

    is_url_handler = True

    def match(self, word):
        ''' Word matcher

        Args:
            word (smarturlize.smarturlize.Word)
        Returns:
            (bool): Indicates wheather the given word object should be handled
            by this transformer or not.
        '''
        raise NotImplementedError

    def transform(self, word):
        ''' Word transformer

        Args:
            word (smarturlize.smarturlize.Word)
        Returns:
            (str) The string you want to replace the given word with.
        '''
        raise NotImplementedError


class Registry(list):

    def register(self, transformer):
        '''Register transformer

        Attrs:
            transformer (BaseTransformer): Any subclass of BaseTransformer
        Raises:
            ValueError if transformer is already registered
            AssertionError if transformer is not a subclass of BaseTransformer
        '''

        assert (isinstance(transformer, BaseTransformer),
                '%s is not a subclass of BaseTransformer' % transformer)

        if transformer.__name__ in (t.__name__ for t in self):
            raise ValueError('Transformer %s is already registered.'
                             % transformer.__name__)
        self.insert(0, transformer)
        return transformer

    def unregister(self, transformer_name):
        '''Unregister transformer

        Attrs:
            transformer (str): Classname of a transformer
        Raises:
            ValueError if no transformer with the provided classname exists.
        '''

        for t in self:
            if t.__name__ == transformer_name:
                self.remove(t)
                return
        raise ValueError('Transformer %s is not registered' % transformer_name)


registry = Registry()
transformer = registry.register


@transformer
class ClickableLinks(BaseTransformer):
    '''Converts urls to clickable links'''

    def match(self, word):
        return True

    def transform(self, word):
        return '<a href="%s">%s</a>' % (word.word, word.word)


@transformer
class DisplayImages(BaseTransformer):
    '''Wraps urls in html img tags'''

    def match(self, word):
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        for ext in image_extensions:
            if word.word.lower().endswith('.%s' % ext):
                return True
        return False

    def transform(self, word):
        return '<img src="%s" height="100"/>' % word.word


@transformer
class EmailLinks(BaseTransformer):
    '''Makes email addresses clickable'''

    is_url_handler = False

    def match(self, word):
        return re.match('[\w\.-]+@[\w\.-]+\.\w{2,4}', word.word)

    def transform(self, word):
        return '<a href="mailto:%s">%s</a>' % (word.word, word.word)


@transformer
class YoutubeEmbed(BaseTransformer):
    '''Converts youtube links to embedded youtube frames'''

    width = '640px'
    height = '390px'

    def match(self, word):
        return word.url.netloc.endswith('youtube.com')

    def transform(self, word):
        youtube_id = urlparse.parse_qs(word.url.query).get('v', '')[0]
        params = {
            'type': 'text/html',
            'src': 'http://www.youtube.com/embed/%s' % youtube_id,
            'height': self.height,
            'width': self.width,
            'frameBorder': '0',
        }
        params_string = ['%s="%s"' % (k, v) for k, v in params.iteritems()]
        return '<iframe %s></iframe>' % ' '.join(params_string)
