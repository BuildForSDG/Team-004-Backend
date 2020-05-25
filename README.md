A one-liner phrase describing this project or app

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b18c2c51e3e3482e8c9d83d9f8601e57)](https://app.codacy.com/gh/BuildForSDG/Team-004-Backend?utm_source=github.com&utm_medium=referral&utm_content=BuildForSDG/Team-004-Backend&utm_campaign=Badge_Grade_Settings)


## About

This project aims to solve the problem of limited access to financing for SMEs. We understand that SMEs are a major backbone for developed countries; Therefore, to help grow the economy of Nigeria sustainably, SMEs must thrive.

The biggest limiting factor of SME growth in Nigeria is access to financing, so we are building a a platform to make financing decentralized and more accessible.

Welcome to WeFinance.


## Requirements

This is a simple python starter repo template for setting up your project. The setup contains:

- install: poetry via pip. poetry is a dependecy manager.

- poetry: configuration in pyproject.toml

- flake8: for linting and formatting

## Why

Talk about what problem this solves, what SDG(s) and SGD targets it addresses and why these are important

## Usage
How would someone use what you have built, include URLs to the deployed app, service e.t.c when you have it setup


## Setup
You should have **Python 3.5+** and **git** installed.

1. Clone the repo you've created from the template herein and change into the directory

    ``
    git clone <Your Repository>
    ``

2. Change into repo directory

    ``
    cd python-starter
    ``

3. Install poetry, a dependecy manager for python.

    On windows, you will need powershell to install it:

    ``
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
    ``

    After that you will need to restart the shell to make it operational.

    &nbsp;

    On linux and other posix systems (mac included):

    ``
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    ``

    &nbsp;

    To check that it is correctly installed, you can check the version:
    ``
    poetry --version
    ``

    May be the latest stable version is not installed with the installation script, to update poetry, you can run:

    ``
    poetry self update
    ``

4. With poetry installed, you should install project dependecies by running:

    ``
    poetry install
    ``

    This will install pytest for running tests and flake8, linter for your project.

#### To Note
`src/app.py` is the entry to the project and source code should go into the `src` folder.

All tests should be written in the `tests` folder. tests/test_src.py is a sample test file that shows how tests should like. Feel free to delete it.

#### Hints

- Lint: `poetry run flake8`
- Run tests using the command: `poetry run pytest`
- Install dependencies:
  `poetry add <dependency>`
- Install dev dependencies:
  `poetry add --dev <dev-dependency>`
- Run your project:
  `poetry run app`


## Authors

List the team behind this project. Their names linked to their Github, LinkedIn, or Twitter accounts should siffice. Ok to signify the role they play in the project, including the TTL and mentor

## Contributing
If this project sounds interesting to you and you'd like to contribute, thank you!
First, you can send a mail to buildforsdg@andela.com to indicate your interest, why you'd like to support and what forms of support you can bring to the table, but here are areas we think we'd need the most help in this project :
1.  area one (e.g this app is about human trafficking and you need feedback on your roadmap and feature list from the private sector / NGOs)
2.  area two (e.g you want people to opt-in and try using your staging app at staging.project-name.com and report any bugs via a form)
3.  area three (e.g here is the zoom link to our end-of sprint webinar, join and provide feedback as a stakeholder if you can)

## Acknowledgements

Did you use someone else’s code?
Do you want to thank someone explicitly?
Did someone’s blog post spark off a wonderful idea or give you a solution to nagging problem?

It's powerful to always give credit.

## LICENSE
MIT

## Important Commands

To create a new Django app:
- `poetry run python manage.py startapp <app_name>`

To create migrations:
- `poetry run python manage.py makemigrations <optional_app_name>`

To run migrations for an app:
- `poetry run python manage.py migrate`

To undo migrations for an app:
- `poetry run python manage.py migrate <required_app_name> zero`

To Run Tests:
- `poetry run python manage.py test <optional_test_folder>`

To delete all the db's data:
- `poetry run python manage.py flush`

To export to requirements file (for Heroku deployment):
- `poetry export -f requirements.txt > requirements.txt`