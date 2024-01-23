# tictactoe

A Tic-tac-toe game

# Features

* Full-featured framework for fast, easy, and documented API with [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
* Swagger Documentation (Part of Flask-RESTX).
* Unit Testing.
* Database ORM with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* Database Migrations using [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
* Object serialization/deserialization with [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* Data validations with Marshmallow [Marshmallow](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation)

## Flask CLI help command output:
```sh
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=tictactoe.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
  test    Run unit tests
```

# Pre-requisites

`Poetry` is recommended to help manage the dependencies and virtualenv.

You can also use other DBs like `PostGreSQL`, make sure you have it setup and update your `DATABASE_URL` in your configs.
Read more at [Flask-SQLAlchemy's](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) documentations.

It uses [Black](https://github.com/psf/black) for code styling/formatting.

# Usage

## Notes

The rest of the resources are found in `/api` (This is the docs route by default, this can be changed easily).

## Installing with Poetry
```sh
# Install packages with poetry
$ poetry install
```

## Running
Please specify your app's environment variables in a `.env` file, otherwise Flask CLI wouldn't find your app.

```sh
# .env file example
export FLASK_APP=tictactoe

# configs: production, testing, development, and default (uses DevelopmentConfig)
export FLASK_CONFIG=development

# Another way of assigning environment variables is:
FLASK_APP=tictactoe
FLASK_CONFIG=development

# Read more at https://github.com/theskumar/python-dotenv
```

```sh
# Enter the virtualenv
$ poetry shell

# (Optional for development, recommended)
$ flask db init # Creates a new migration repository
$ flask db upgrade # Upgrade to a later version

# Run the app
$ flask run
```

## Unit testing

```sh
# Unit testing
$ flask test

# Run specific unit test(s)
$ flask test test tests.test_models.TestModels.test_game_finished_winner ...
```
