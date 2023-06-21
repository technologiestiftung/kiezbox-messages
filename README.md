# Kiezbox Backend

Tested with Python 3.11.4

## Installation guide

### Set your virtual environment

The following steps are not required but recommended. This will allow you to install packages in your isolated virtual environment instead of globally, reducing the risk of breaking system tools or other projects.

1. Install [pyenv](https://github.com/pyenv/pyenv) and the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin.
2. Download the appropriate Python version with `pyenv install 3.11.4` in the command line.
3. Create a virtual environment with the appropriate Python version and name for your environment, for example `pyenv virtualenv 3.11.4 kiezbox`
4. Activate the environment with `pyenv activate kiezbox`

### Run the API

1. Move to the `/backend` directory.
2. Install the required libraries with the command line `pip install -r requirements.txt`
3. Run the server with the command line `uvicorn main:app --reload`
4. Your terminal should show something like: 

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open this URL with the `/docs` suffix in your server to access the Swagger documentation of the API. For this example: `http://127.0.0.1:8000/docs

### Update the API

If you want to run an updated version of the API which introduces changes in the database models (for example, a new field), you will have to wipe the database clean first. To do this, simply delete the `backend.db` file.
