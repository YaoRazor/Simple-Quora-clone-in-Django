from unittest import TestCase
from urlparse import ParseResult

from . import SmartUrlize, registry
from .smarturlize import Word


class TestWord(TestCase):

    def setUp(self):
        self.valid_url_with_subdomain = Word('http://docs.djangoproject.com')
        self.valid_url_with_subdomain_www = Word('http://www.djangoproject.com')
        self.valid_url_without_subdomain = Word('http://djangoproject.com')
        self.invalid_url = Word('www.djangoproject.com')
        self.non_url = Word('django')

    def test_identify_url(self):
        self.assertTrue(self.valid_url_with_subdomain.is_url,
                        'Failed to identify url')

        self.assertTrue(self.valid_url_with_subdomain_www.is_url,
                        'Failed to identify url')

        self.assertTrue(self.valid_url_without_subdomain.is_url,
                        'Failed to identify url')

        self.assertFalse(self.invalid_url.is_url, 'Identified non url as url')
        self.assertFalse(self.non_url.is_url, 'Identified non url as url')

    def test_url_type(self):
        self.assertIsInstance(self.valid_url_with_subdomain.url, ParseResult,
                              'Url object is not of right type')

        self.assertIsNone(self.non_url.url,
                          'Url object of non url should be None')


class TestSmartUrlize(TestCase):

    def setUp(self):
        self.urlizer = SmartUrlize()
        self.text_with_url = 'This is a link http://www.djangoproject.com'
        self.text_with_img_url = (
            'The django logo can be seen here https://docs.djangoproject.com'
            '/s/img/site/hdr_logo.b19c5e60269d.gif and this is a relative img '
            'path hdr_logo.b19c5e60269d.gif'
        )

    def test_transforming_urls(self):
        text = self.text_with_url
        expected_results = ('This is a link <a href="http://www.djangoproject.com">'
                            'http://www.djangoproject.com</a>')

        actual_results = self.urlizer(text)
        self.assertEqual(actual_results, expected_results,
                         'Link is not transformed correctly')

    def test_transforming_images(self):
        text = self.text_with_img_url
        transformed_text = self.urlizer(text)

        expected_img_link = (
            '<img src="https://docs.djangoproject.com'
            '/s/img/site/hdr_logo.b19c5e60269d.gif" />'
        )
        self.assertIn(expected_img_link, transformed_text,
                      'Expected img tag missing in text')

        not_expected_img_url = (
            '<a href="https://docs.djangoproject.com/s/img/site/'
            'hdr_logo.b19c5e60269d.gif">https://docs.djangoproject.com/s/img/'
            'site/hdr_logo.b19c5e60269d.gif</a>'
        )
        self.assertNotIn(not_expected_img_url, transformed_text,
                         'Unwanted link to image found in text')
        not_expected_img_tag = '<img src="hdr_logo.b19c5e60269d.gif" />'
        self.assertNotIn(not_expected_img_tag, transformed_text,
                         'Unwanted img tag found in text')

    def test_unregistering_transformer(self):
        text = self.text_with_img_url

        registry.unregister('DisplayImages')
        transformed_text = self.urlizer(text)

        self.assertNotIn('<img', transformed_text, 'Unwanted img tag in text')
        self.assertIn('</a>', transformed_text, 'link missing in text')

        registry.unregister('ClickableLinks')
        transformed_text = self.urlizer(text)

        self.assertNotIn('<img', transformed_text, 'Unwanted img tag in text')
        self.assertNotIn('</a>', transformed_text, 'Unwanted link in text')

    def test_include_exclude_transformers(self):
        # Don't include or exclude anything
        self.urlizer('')
        expected_results = ['YoutubeEmbed', 'EmailLinks', 'DisplayImages',
                            'ClickableLinks']
        actual_results = [t.__class__.__name__
                          for t in self.urlizer.transformers]
        self.assertListEqual(actual_results, expected_results,
                             'Not getting expected transformers when calling '
                             'urlizer with no include/exclude kwargs.')

        # Include YoutubeEmbed and EmailLinks transformers
        self.urlizer('', include=['YoutubeEmbed', 'EmailLinks'])
        expected_results = ['YoutubeEmbed', 'EmailLinks']
        actual_results = [t.__class__.__name__
                          for t in self.urlizer.transformers]
        self.assertListEqual(actual_results, expected_results,
                             'Not getting expected transformers when '
                             'including YoutubeEmbed and EmailLinks.')

        # Exclude YoutubeEmbed transformer
        self.urlizer('', exclude=['YoutubeEmbed'])
        expected_results = ['EmailLinks', 'DisplayImages', 'ClickableLinks']
        actual_results = [t.__class__.__name__
                          for t in self.urlizer.transformers]
        self.assertListEqual(actual_results, expected_results,
                             'Not getting expected transformers when '
                             'excluding YoutubeEmbed.')

        # Call urlize again with no transformers included or excluded
        self.urlizer('')
        expected_results = ['YoutubeEmbed', 'EmailLinks', 'DisplayImages',
                            'ClickableLinks']
        actual_results = [t.__class__.__name__
                          for t in self.urlizer.transformers]
        self.assertListEqual(actual_results, expected_results,
                             'Not getting expected transformers when calling '
                             'urlizer again with no include/exclude kwarg.')
