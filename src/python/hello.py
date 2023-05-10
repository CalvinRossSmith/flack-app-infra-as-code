from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(port)
    app.run(host='0.0.0.0',port=port,ssl_context=('cert.pem', 'key.pem'))