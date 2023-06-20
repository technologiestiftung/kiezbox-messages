# Kiezbox Backend

Tested with Python 3.11.4

## Installation guide

1. Move to the `/backend` directory.
2. Install the required libraries with the command line `pip install -r requirements.txt`
3. Run the server with the command line `uvicorn main:app --reload`
4. Your terminal should show something like: 

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open this URL with the `/docs` suffix in your server to access the Swagger documentation of the API. For this example: `http://127.0.0.1:8000/docs`