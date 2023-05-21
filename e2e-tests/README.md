# About

The end-to-end tests service is meant to test the following behaviors:
- Interaction between backend, frontend, database, and Auth0 using dev credentials;
- Frontend navigation.

It's not meant to test frontend rendering behavior so, for this reason, it doesn't test dark mode and language switching.

It uses the following technologies:
- Pytest-playwright: a framework for automated tests with browser interactions. I chose it instead of Selenium because it's faster, less flaky, and has better support to setting up video recording, although a little hard to customize;
- Pytest + pytest-cov: to run all tests. Coverage is set to 100% (with omissions).

The `/bin` folder contains bash files meant to be used with CI/CD pipelines. It consists of:
- `check_linting.sh`: runs flake8;
- `check_types.sh`: runs mypy;
- `run_tests.sh`: runs pytest tests.
