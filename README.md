# About

Demo project for learning and portfolio purposes. It consists of a backend and frontend application that uses Auth0 for user authentication and displays the user data returned by Auth0 in the profile page.

It uses a monorepo structure, which is easier to develop, maintain, and deploy.

At the root, there are three `.yml` files used for setting up the application services in their respective containers using `docker-compose` commands, all extending common configuration from `base.yml`. Their main features are:
- `dev.yml`:
  - Install apps with dev-packages;
  - Doesn't make services interdependent, so they can run individually;
  - Maps each service folder to container, so changes are reflected immediately;
  - Meant for local environments;
- `test.yml`:
  - Install apps with dev-packages;
  - As close from production environment as possible, except for the presence of dev-packages and different environment variables;
  - Meant for unit tests on pipelines;
- `prod.yml`:
  - Doesn't install apps with dev-packages;
  - Meant for:
    - Running end-to-end tests with the `e2etests` service, but still not using production environment variables;
    - Production deploy.

More details about each service can be found in their readmes.

# Continuation

Possible future improvements might include:
- Set up a CI/CD pipeline with GitHub Actions, AWS Free Tier, or another;
- Set up [sops](https://github.com/mozilla/sops) to manage and encrypt multiple environment variables files, with at least one for dev/test/end-to-end test and one for production;
- Add structured logging to backend;
- Add security check for dependencies using [safety](https://github.com/pyupio/safety), `npm audit`, or GitHub's Dependabot.
