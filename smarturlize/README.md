smart-urlize
============

smart-urlize is licensed under [MIT license](LICENSE.md).

The purpose of this django app is to provide an easy way to detect and handle urls in texts.
Different urls are handled in different ways. For instance, an image url is wrapped in a html img tag and a youtube url is replaced by an embedded youtube player.
Urls that are not known how to handle and email addresses are replaced by actual html links.

# Usage
First, add `smarturlize` to your installed apps.

The easies way to use this app is to simply add the template filter `smarturlize` to a text in your template.
```django
{% load smarturlize %}

{{ text|smarturlize }}

```
Just be aware that the `smarturlize` template filter marks the text as safe.
It is therefore important to make sure that your text is
[escaped](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-escape)
if it comes from user input to prevent XSS attacks.

# Url handlers
The following url handlers are registered by default 
- *ClickableLinks* replaces all urls in the text, that are not handled by other url handlers, with clickable html links.
- *DisplayImages* replaces all image urls with html `img` tags.
- *EmailLinks* replaces all email addresses with clickable email links.
- *YoutubeEmbed* replaces all youtube urls with an embedded Youtube player.

### Writing your own url handlers
Adding your own url handler is very easy.  
You do that by writing a custom transformer class that represents your url handler and should be a subclass of
[`transformers.BaseTransformer`](smarturlize/transformers.py#L5-L28).
You can then register your url handler with the `@transformer` decorator.

```python
from smarturlize.transformers import BaseTransformer, transformer


@transformer
class MakeRedditLinksGreen(BaseTransformer):

    def match(self, word):
        return word.url.hostname in ('reddit.com', 'www.reddit.com')

    def transform(self, word):
        return '<a style="color: green;" href="%s">Reddit link</a>' % word.word
```

```python
>>> from smarturlize import SmartUrlize
>>> urlizer = SmartUrlize()
>>> print urlizer('This contains a reddit link http://www.reddit.com/r/programming')
This contains a reddit link <a style="color: green;" href="http://www.reddit.com/r/programming">Reddit link</a>
```

### Handling non urls

By default, smart-urlize will check each word if it is an url before trying to transform it.
This is done for performance reasons so the non urls in your text, won't be parsed through all of the url handlers.

However, you can also create a transformer that works on non urls if you want to.
This is done by adding the `is_url_handler = False` property to your transformer class.
Let's say you wan't to correct all misspellings of the word 'belive' to 'believe'.
In that case your transformer class would look something like this.

```python
from smarturlize.transformers import BaseTransformer, transformer


@transformer
class CorrectTypoBelive(BaseTransformer):

    is_url_handler = False
    
    def match(self, word):
        return word.word == 'belive'
        
    def transform(self, word):
        return 'believe'
```

### Including and excluding url handlers
By the term *including* , I more specifically mean, *limiting*.
It's the same idea as including and excluding form fields in django forms.

Let's say you want include the *ClicableLinks* url handler,
that is call the smarturlize templatefilter with *ClickableLinks* as the only url handler.
```django
{% load smarturlize %}

{{ text|smarturlize:'ClicableLinks' }}
```

Or you want to exclude *YoutubeEmbed* and *DisplayImages*,
that is call smarturlize with all registered url handlers, except *YoutubeEmbed* and *DisplayImages*.
```django
{% load smarturlize %}

{{ text|smarturlize:'-DisplayImages,YoutubeEmbed' }}
```
In this example you can see that multiple handlers are seperated by comma and a leading minus `-` is used to exclude fields.

### Unregistering url handlers
To unregister an url handler, call `smarturlize.registry.unregister` with the transformer's class name as an argument.
```python
from smarturlize import registry

registry.unregister('DisplayImages')
```
