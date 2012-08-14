from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import get_language

from babel.core import Locale
from mock import patch
from nose.tools import eq_
from tower import activate

from shared.tests import TestCase
from shared.utils import (absolutify, current_locale, redirect,
                          ugettext_locale as _locale)


class TestAbsolutify(TestCase):
    fixtures = ['sites']

    def setUp(self):
        self.patcher = patch.object(Site.objects, 'get_current')
        self.mock = self.patcher.start()
        self.mock.return_value = Site(domain='badge.mo.com', name='test')

    def tearDown(self):
        self.patcher.stop()

    def test_basic(self):
        url = absolutify('/some/url')
        eq_(url, '//badge.mo.com/some/url')

    def test_https(self):
        """Test that https=True forces an https url."""
        url = absolutify('/some/url', https=True)
        eq_(url, 'https://badge.mo.com/some/url')

    def test_cdn(self):
        with patch.object(settings, 'CDN_DOMAIN', None):
            url = absolutify('/some/url', cdn=True)
            eq_(url, '//badge.mo.com/some/url')

        with patch.object(settings, 'CDN_DOMAIN', 'cdn.badge.mo.com'):
            url = absolutify('/some/url', cdn=True)
            eq_(url, '//cdn.badge.mo.com/some/url')


class TestRedirect(TestCase):
    urls = 'shared.tests.urls'

    def test_basic(self):
        with self.activate('en-US'):
            response = redirect('mock_view')
        eq_(response.status_code, 302)
        eq_(response['Location'], '/en-US/mock_view')

    def test_permanent(self):
        with self.activate('en-US'):
            response = redirect('mock_view', permanent=True)
        eq_(response.status_code, 301)
        eq_(response['Location'], '/en-US/mock_view')


class TestCurrentLocale(TestCase):
    def test_basic(self):
        """Test that the currently locale is correctly returned."""
        activate('fr')
        eq_(Locale('fr'), current_locale())

    def test_unknown(self):
        """
        Test that when the current locale is not supported by Babel, it
        defaults to en-US.
        """
        activate('fy')
        eq_(Locale('en', 'US'), current_locale())


def mock_ugettext(message, context=None):
    if (get_language() == 'xxx'):
        return 'translated'
    else:
        return 'untranslated'


@patch('shared.utils.tower.ugettext', mock_ugettext)
class TestUGetTextLocale(TestCase):
    def test_basic(self):
        """
        Test that translating a string works and doesn't change the current
        locale.
        """
        activate('fr')
        eq_(_locale('message', 'xxx'), 'translated')
        eq_(get_language(), 'fr')
