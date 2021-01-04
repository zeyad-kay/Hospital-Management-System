## Setup

1. Install [python](https://www.python.org/downloads)

2. open the terminal and create a virtual environment

Windows:
```sh
    > python -m venv venv
    > venv\Scripts\activate
```
Linux:
```sh
    $ python3 -m venv venv
    $ source venv/bin/activate
```
Your command prompt will change to show the name of the activated environment (venv).

3. Install project dependencies
```sh
    > pip install -r requirements.txt
```
4. Set environment variables

Windows:
```sh
    > set FLASK_APP=app
    > set FLASK_ENV=development
```
Linux:
```sh
    $ export FLASK_APP=app
    $ export FLASK_ENV=development
```
5. Setup sqlite database
```sh
    > flask init-db
```
should output "Initialized the database".

6. Run the app
```sh
    > flask run
```

Visit: http://127.0.0.1:5000/