import re
import pytest
from unittest.case import TestCase
from playwright.sync_api import Page, expect
from playwright.sync_api._generated import Locator


class AppTestCase(TestCase):
    @pytest.fixture(autouse=True)
    def _setup_fixtures(
        self,
        page: Page,
        page_timeout: int,
        frontend_url: str,
        auth0_url: str,
        account_email: str,
        account_password: str
    ) -> None:
        self.page = page
        self.page_timeout = page_timeout
        self.frontend_url = frontend_url
        self.auth0_url = auth0_url

        # Account pre-created agains Auth0 configured application
        self.account_email = account_email
        self.account_password = account_password
        self.language = 'en-US'

    def _check_url(self, url: str) -> None:
        expect(self.page).to_have_url(re.compile(url), timeout=self.page_timeout)

    def _navigate_to(self, path: str) -> None:
        self.page.goto(f'{self.frontend_url}/{self.language}/{path}')

    def _home_page_not_authenticated(self) -> Locator:
        self._navigate_to('')
        return self.page.get_by_role('link', name='Login')

    def _profile_page_not_authenticated(self) -> None:
        self._navigate_to('profile')
        self._check_url(self.auth0_url)

    def _login_page_not_authenticated(self) -> None:
        self._navigate_to('login')
        self._check_url(self.auth0_url)

    def _logout_page_not_authenticated(self) -> Locator:
        self._navigate_to('logout')
        return self.page.get_by_role('link', name='Login')

    def _home_page_authenticated(self) -> None:
        self._navigate_to('')
        profile_btn = self.page.get_by_role('link', name='Profile')
        profile_btn.click()
        self._check_url('/profile')

    def _profile_page_authenticated_home(self) -> None:
        self._navigate_to('profile')
        home_btn = self.page.get_by_role('link', name='Home')
        home_btn.click()
        self.page.get_by_role('link', name='Profile')

    def _profile_page_authenticated_logout(self) -> None:
        self._navigate_to('profile')
        home_btn = self.page.get_by_role('link', name='Logout')
        home_btn.click()
        self.page.get_by_role('link', name='Login')

    def _logout_page_authenticated(self) -> None:
        self._navigate_to('logout')
        self.page.get_by_role('link', name='Login')

    def _login_page_authenticated(self) -> None:
        self._navigate_to('login')
        self._check_url('/profile')

    def _login(self) -> None:
        login_btn = self._home_page_not_authenticated()
        login_btn.click()
        self._check_url(self.auth0_url)

        email_input = self.page.wait_for_selector('input[name="username"]')
        assert email_input
        email_input.fill(self.account_email)

        password_input = self.page.wait_for_selector('input[name="password"]')
        assert password_input
        password_input.fill(self.account_password)

        continue_btn = self.page.wait_for_selector('button[type="submit"]')
        assert continue_btn
        continue_btn.click()

        self._check_url('/profile')

    def _user_not_authenticated(self) -> None:
        self._home_page_not_authenticated()
        self._profile_page_not_authenticated()
        self._login_page_not_authenticated()
        self._logout_page_not_authenticated()

    def _user_authenticated(self) -> None:
        self._home_page_authenticated()
        self._profile_page_authenticated_home()
        self._login_page_authenticated()

    def test_app(self) -> None:
        self._user_not_authenticated()
        self._login()
        self._user_authenticated()
        self._profile_page_authenticated_logout()
        self._login()
        self._logout_page_authenticated()
