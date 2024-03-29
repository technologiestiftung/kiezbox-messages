![PyPI - Version](https://img.shields.io/pypi/v/kiezbox-messages)
![](https://img.shields.io/badge/Built%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiestiftung%20Berlin-blue)

# Kiezbox Notruf-App

Tested with Python 3.11

## Architecture

One main driver was the will to have something minimalistic while still modern.
A first try to have a separate frontend using react and dynamic routes has proven to be problematic
as installing node modules and having a running node instance on IoT devices isn't great.
Thus we have server-side template rendering for the frontend.
In these templates we use HTMX to handle the interactivity.

The backend is fastapi, using sqlmodel to unite sqlalchemy and pydantic. FastAPI is serving some static files as well as the Jinja2 templates using uvicorn. 
We use a HTML form to send the emergency calls.
We use server-sent events (SSE) to trigger reloads on the inbox.

## Installation guide

You need Python 3.11 and we recommend you use a virtualenv. The install the app and its dependencies via:

`pip install kiezbox-messages`

You can then start a server from the terminal via `uvicorn main:app [-h 0.0.0.0] [-p 80]`.

To use it in production, we recommend that you a service control tool like systemd or upstart.

## Development guide

### Set your virtual environment

The following steps are not required but recommended. This will allow you to install packages in your isolated virtual environment instead of globally, reducing the risk of breaking system tools or other projects.

1. Install [pyenv](https://github.com/pyenv/pyenv) and the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin.
2. Download the appropriate Python version with `pyenv install 3.11` in the command line.
3. Create a virtual environment with the appropriate Python version and name for your environment, for example `pyenv virtualenv 3.11 kiezbox`
4. Activate the environment with `pyenv activate kiezbox`

### Run the App

1. Install the required libraries with the command line `pip install -r requirements.txt`
2. Run the server with the command line `uvicorn main:app --reload`
3. Your terminal should show something like: 

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open this URL with the `/docs` suffix in your server to access the Swagger documentation of the API. For this example: `http://127.0.0.1:8000/docs

### Update the model

If you want to run an updated version of the API which introduces changes in the database models (for example, a new field), you will have to wipe the database clean first. To do this, simply delete the `backend.db` file.

## Frontend

On the JS side, the interactivity is handled by HTMX, which is shipped locally as we are in a case where phones have no internet connectivity. Currently v1.9.10 is included. See https://github.com/bigskysoftware/htmx/releases.

We have a second JS file which is the SSE extension for HTMX. You can get the latest version from https://github.com/bigskysoftware/htmx/tree/master/dist/ext.

The frontend is simple Jinja2 server-rendered templates styled with TailwindCSS.

Run `npm install`.

To watch CSS updates, you may run `npm run dev`

## Release a new version

Update the version string in `pyproject.toml`. Then build running `python -m build`.

To upload the data to pypi, you need `pip install twine` and then run `twine upload dist/*` having set the proper credentials in `~/.pypirc`.


## TODO

One could automate the publishing of versions to PyPi, using:
 * dynamic versioning from git tags through [setuptools-scm](https://setuptools-scm.readthedocs.io/en/latest/)
 * [Github Actions Pypi-Publish](https://github.com/marketplace/actions/pypi-publish) following the [Python Packaging Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
