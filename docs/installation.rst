##################
Setup and run
##################


To setup the project locally follow the instructions:

*********
Getting Up and Running Locally
*********



Make sure to have the following on your host:

- Python 3.9
- PostgreSQL
- `Redis <https://redis.io/download>`_, if using Celery
- `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_

First things first.

1. Create a virtualenv:

  .. code-block:: python

   $ python3.9 -m venv <virtual env path>

2. Activate the virtualenv you have just created: 

  .. code-block:: python

   $ source <virtual env path>/bin/activate

3. Install cookiecutter-django:

  .. code-block:: python

   $ cookiecutter gh:pydanny/cookiecutter-django

4. Install development requirements:

  .. code-block:: python
  
   $ pip install -r requirements/local.txt
   $ git init # A git repo is required for pre-commit to install
   $ pre-commit install

5.Create a new PostgreSQL database using `createdb <https://www.postgresql.org/docs/current/static/app-createdb.html>`_
:


  .. code-block:: bash

   $ createdb <what you have entered as the project_slug at setup stage> -U postgres --password <password>


  .. note::
   if this is the first time a database is created on your machine you might need an `initial PostgreSQL set up <http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html>`_ to allow local connections & set a password for the postgres user. The `postgres documentation <https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html>`_ explains the syntax of the config file that you need to change

6.Set the environment variables for your database(s):

  .. code-block:: bash

   $ export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/<DB name given to createdb>
   # Optional: set broker URL if using Celery
   $ export CELERY_BROKER_URL=redis://localhost:6379/0
   

  .. note::
   
   Check out the `Settings <https://cookiecutter-django.readthedocs.io/en/latest/settings.html#settings>`_ page for a comprehensive list of the environments variables.
   
  .. note::
   
   To help setting up your environment variables, you have a few options:

    - create an *.env* file in the root of your project and define all the variables you need in it. Then you just need to have *DJANGO_READ_DOT_ENV_FILE=True* in your machine and all the variables will be read.
    - Use a local environment manager like `direnv <https://direnv.net/>`_

7.Apply migrations:

  .. code-block:: python

   $ python manage.py migrate

8.If you’re running synchronously, see the application being served through Django development server:

  .. code-block:: python
   
   $ python manage.py runserver 0.0.0.0:8000

or if you’re running asynchronously:

  .. code-block:: python

   $ uvicorn config.asgi:application --host 0.0.0.0 --reload



*********
Getting Up and Running Locally with Docker
*********



The steps below will get you up and running with a local development environment. All of these commands assume you are in the root of your generated project.

**Prerequisites**

    - Docker; if you don’t have it yet, follow the `installation instructions <https://docs.docker.com/install/#supported-platforms>`_

    - Docker Compose; refer to the official documentation for the `installation guide <https://docs.docker.com/compose/install/>`_

**Build the Stack**

This can take a while, especially the first time you run this particular command on your development system:

  .. code-block:: python

   $ docker-compose -f local.yml build

Generally, if you want to emulate production environment use *production.yml* instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!


**Run the Stack**

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development:

  .. code-block:: python

   $ docker-compose -f local.yml up

You can also set the environment variable *COMPOSE_FILE* pointing to *local.yml* like this:

  .. code-block:: python

   $ export COMPOSE_FILE=local.yml

And then run:

  .. code-block:: python

   $ docker-compose up

To run in a detached (background) mode, just:  


  .. code-block:: python

   $ docker-compose up -d

**Execute Management Commands**

As with any shell command that we wish to run in our container, this is done using the *docker-compose -f local.yml run --rm* command:

  .. code-block:: python
     
   $ docker-compose -f local.yml run --rm django python manage.py migrate
   $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

Here, django is the target service we are executing the commands against.

**(Optionally) Designate your Docker Development Server IP**


When DEBUG is set to True, the host is validated against ['localhost', '127.0.0.1', '[::1]']. This is adequate when running a virtualenv. For Docker, in the config.settings.local, add your host development server IP to INTERNAL_IPS or ALLOWED_HOSTS if the variable exists.

**Configuring the Environment**

This is the excerpt from your project’s local.yml:



  .. code-block:: yml

   # ...
  
   postgres:
     build:
       context: .
       dockerfile: ./compose/production/postgres/Dockerfile
     volumes:
       - local_postgres_data:/var/lib/postgresql/data
       - local_postgres_data_backups:/backups
     env_file:
       - ./.envs/.local/.postgres

   # ..

The most important thing for us here now is env_file section enlisting ./.envs/.local/.postgres. Generally, the stack’s behavior is governed by a number of environment variables (env(s), for short) residing in envs/, for instance, this is what we generate for you:

  .. code-block:: yml

   .envs
   ├── .local
   │   ├── .django
   │   └── .postgres
   └── .production
       ├── .django
       └── .postgres

By convention, for any service sI in environment e (you know someenv is an environment when there is a someenv.yml file in the project root), given sI requires configuration, a .envs/.e/.sI service configuration file exists.

Consider the aforementioned .envs/.local/.postgres:

  .. code-block:: yml

   # PostgreSQL
   # ------------------------------------------------------------------------------
   POSTGRES_HOST=postgres
   POSTGRES_DB=<your project slug>
   POSTGRES_USER=XgOWtQtJecsAbaIyslwGvFvPawftNaqO
   POSTGRES_PASSWORD=jSljDz4whHuwO3aJIgVBrqEml5Ycbghorep4uVJ4xjDYQu0LfuTZdctj7y0YcCLu

The three envs we are presented with here are POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD (by the way, their values have also been generated for you). You might have figured out already where these definitions will end up; it’s all the same with django service container envs.

One final touch: should you ever need to merge *.envs/.production/* in a single .env run the merge_production_dotenvs_in_dotenv.py:


  .. code-block:: python

   $ python merge_production_dotenvs_in_dotenv.py

The .env file will then be created, with all your production envs residing beside each other.
