import os
import shutil
import pytest
import typing
import pathlib
from slugify import slugify
from playwright.sync_api import BrowserContext, Page
from playwright.sync_api._generated import ConsoleMessage
from _pytest.fixtures import FixtureRequest


@pytest.fixture
def frontend_url() -> str:
    url = os.getenv('FRONTEND_URL')
    assert url
    return url


@pytest.fixture
def auth0_url() -> str:
    url = os.getenv('AUTH0_DOMAIN')
    assert url
    return url


@pytest.fixture
def account_email() -> str:
    email = os.getenv('E2E_TEST_EMAIL')
    assert email
    return email


@pytest.fixture
def account_password() -> str:
    password = os.getenv('E2E_TEST_PASSWORD')
    assert password
    return password


@pytest.fixture
def log_folder() -> str:
    folder = './logs/'

    if not os.path.exists(folder):  # pragma: no cover
        os.makedirs(folder)

    return folder


@pytest.fixture(scope='session')
def video_path() -> str:
    return './videos/'


@pytest.fixture(scope='session')
def video_width() -> int:
    return 1200


@pytest.fixture(scope='session')
def video_height() -> int:
    return 600


@pytest.fixture
def page_timeout() -> int:
    return 1 * 60 * 1000  # milliseconds


@pytest.fixture
def page(
    context: BrowserContext,
    request: FixtureRequest,
    log_folder: str,
    page_timeout: int
) -> typing.Generator[Page, None, None]:
    page = context.new_page()
    page.set_default_timeout(page_timeout)
    test_name = request.node.location[-1]
    test_name = slugify(test_name)

    # Set up console log saving
    if log_folder:
        log_path = os.path.join(log_folder, f'{test_name}.log')
        # Create or truncate file
        with open(log_path, 'w'):
            pass

        def _save_log(msg: ConsoleMessage) -> None:
            with open(log_path, 'a') as file:  # pragma: no cover
                file.write(f'{msg}\n')

        console: typing.Literal['console'] = 'console'
        page.on(console, lambda msg: _save_log(msg))

    if page.video:
        # Rename video file to the test name
        original_filename = page.video.path()
        video_folder = os.path.dirname(original_filename)

        filename = f'{test_name}.webm'
        filename = os.path.join(video_folder, filename)
        # Injecting original saving method
        page.video._original_save_as = page.video.save_as  # type: ignore[attr-defined]

        def _save_as(path: str | pathlib.Path) -> None:
            page.video._original_save_as(path)  # type: ignore[union-attr]

            try:
                # Overwrite file if it already exists
                shutil.move(original_filename, filename)
            except FileNotFoundError:  # pragma: no cover
                pass

        page.video.save_as = _save_as  # type: ignore[method-assign]

    yield page


@pytest.fixture(scope='session')
def browser_context_args(
    browser_context_args: dict[str, typing.Any],
    video_path: str,
    video_width: int,
    video_height: int
) -> dict[str, typing.Any]:
    # Ensure video resolution and viewport resolution are the same so video won't get blurred
    return {
        **browser_context_args,
        'record_video_dir': video_path,
        'viewport': {'width': video_width, 'height': video_height},
        'record_video_size': {'width': video_width, 'height': video_height},
    }
