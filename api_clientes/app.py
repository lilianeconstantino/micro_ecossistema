from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=5002, debug=True, host='0.0.0.0')