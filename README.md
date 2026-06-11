# Cyber Security Base Project I
OWASP Top 10 version used: 2021

## Installation instructions

### Clone the repository:
```
$ git clone git@github.com:Niria/csb-project1.git
```

### Create virtual environment and install dependencies:
```
$ cd csb-project1
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install Django
```

### Initialize the database:
```
$ python3 manage.py migrate
```

### Start the server:
```
$ python3 manage.py runserver
```
After starting the app it will be accessible at http://localhost:8000/message_board/