## Description

Flgaz-riz is an application to post some messages, we can post and read the message from another user we don't need some account to use is.

## Global prerequisites

You will need to have python 3.7, the data is sqlite.

## Installation

Clone the Git repository on the develop branch for development environment:

```bash
$ git clone https://github.com/so-mouga/flask-project-school.git
```

Very simple, only a few steps to execute from your terminal:

1. create an environment python 3 : `virtualenv -ppython3 venv`
2. activate the environment :
  - mac/linux: `source venv/bin/activate`
  - windows: `venv\Scripts\activate`
3. install the dependencies :`pip install -r requirements.txt`
4. run the application: `flask run`

## The project:

- Flgaz is a web application written with Python, the entry point of the application is app.py.
- In the file app.py we can see several librairies in order to run the application, like flask
- We can list several routes with different method (GET, POST)
- Each route call a function and use methods from flask to render a response
- We can save a new post on the route /gaz method (GET) with to return on a formulaire. Once we create a message this will be saved in a CSV without check anything on the message etc ….
- This is not a good thing to save in a CSV we have to change the implementation in order to save in a database
- And we need to a some check in order to avoid some attack in the database like (injection SQL), and the top 10 from owasp

## Flask:

Flask is a micro-framework web written with Python, It can to build some solid professionnel application. Flask doesn't provide by default several element like (ORM). In contrary in Django, wich is another web Framework written with python.
the philosophy of Flask is less is more.

## PythonAnywhere:

PythonAnywhere is an online Integrated Development Environment based on the Python. It provides in-browser access to server-based Python and Bash Command-line interfaces, along with a code editor with Syntax highlighting. Program files can be transferred to and from the service using our favorite browser. Web applications hosted by the service can be written using any WSGI-based application framework.
