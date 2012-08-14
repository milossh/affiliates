from django.conf import settings
from django.shortcuts import render
from django.utils.http import urlquote_plus
from django.utils.translation import get_language

from funfactory.urlresolvers import reverse
from session_csrf import anonymous_csrf
from tower import ugettext_lazy as _lazy

from badges.views import dashboard
from browserid.forms import RegisterForm as BrowserIDRegisterForm
from browserid.views import register as browserid_register
from shared.decorators import login_required
from shared.utils import absolutify, redirect
from users.forms import RegisterForm, LoginForm


TWEET_TEXT = _lazy(u'The Firefox Affiliates program is a great way to share '
                   'your love of Mozilla Firefox.')
BROWSERID_NO_ASSERTION = _lazy(u'There was an error during authentication. '
                               'Please try again.')
BROWSERID_VERIFY_FAIL = _lazy(u'BrowserID could not verify your identity. '
                              'Visit <a href="{url}">browserid.org</a> for '
                              'more information.')


@anonymous_csrf
def home(request, register_form=None, login_form=None):
    """Display the home page."""
    # Redirect logged-in users
    if request.user.is_authenticated():
        return redirect('badges.new.step1')

    # en-US users see the BrowserID view instead
    if get_language() in settings.BROWSERID_LOCALES:
        return browserid_home(request)

    if register_form is None:
        register_form = RegisterForm()
    if login_form is None:
        login_form = LoginForm()

    params = {'register_form': register_form,
              'login_form': login_form,
              'share_url': absolutify('/', https=True),
              'tweet_text': urlquote_plus(TWEET_TEXT)}
    return render(request, 'shared/home/normal.html', params)


def browserid_home(request):
    """Display the home page with a BrowserID login."""
    register_form = BrowserIDRegisterForm(request.POST or None)
    if request.method == 'POST':
        # Attempting to register
        response = browserid_register(request, register_form)
        if response is not None:
            return response

    params = {'browserid_verify': reverse('browserid.verify'),
              'register_form': register_form,
              'share_url': absolutify('/', https=True),
              'tweet_text': urlquote_plus(TWEET_TEXT),
              'browserid_no_assertion': BROWSERID_NO_ASSERTION,
              'browserid_verify_fail': BROWSERID_VERIFY_FAIL}
    return render(request, 'shared/home/browserid.html', params)


@login_required
def about(request):
    return dashboard(request, 'shared/about.html')


@login_required
def faq(request):
    return dashboard(request, 'shared/faq.html')
