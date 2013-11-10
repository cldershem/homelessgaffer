#!venv/bin/python
from app import app
from config import DEBUG

if __name__ == '__main__':
    app.run(debug=DEBUG)
