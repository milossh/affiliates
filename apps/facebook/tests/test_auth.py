from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

from mock import Mock
from nose.tools import eq_, ok_

from facebook.auth import login
from facebook.models import FacebookUser
from facebook.tests import FacebookUserFactory
from shared.tests import TestCase


session_middleware = SessionMiddleware()


class LoginTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def request(self, url='/'):
        """
        Create a mock request object.
        """
        request = self.factory.get(url)
        session_middleware.process_request(request)
        return request

    def test_flush_session(self):
        """
        If a previous login session is found and logging in as a different user,
        flush the previous session.
        """
        request = self.request()
        user1 = FacebookUserFactory()
        login(request, user1)

        request.session['somedata'] = 1
        user2 = FacebookUserFactory()
        login(request, user2)
        ok_(not 'somedata' in request.session)

    def test_new_session_key(self):
        """
        If there is an existing, unauthenticated session, change the session
        key on the request.
        """
        request = self.request()
        old_key = request.session.session_key
        user = FacebookUserFactory()

        login(request, user)
        ok_(request.session.session_key != old_key)

    def test_request_user(self):
        """
        After a user is logged in, the user attribute should be set on the
        request object.
        """
        request = self.request()
        user = FacebookUserFactory()
        login(request, user)
        eq_(request.user, user)

    def test_user_logged_in_signal(self):
        mock_signal = Mock(spec=lambda x: x)
        user_logged_in.connect(mock_signal)

        request = self.request()
        user = FacebookUserFactory()
        login(request, user)

        mock_signal.assert_called_once_with(signal=user_logged_in,
                                            sender=FacebookUser,
                                            request=request, user=user)
        user_logged_in.disconnect(mock_signal)
