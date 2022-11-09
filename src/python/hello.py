from flask import Flask
from flask import make_response
from flask import request
from flask import render_template
from flask import url_for, redirect
import os

app = Flask(__name__, template_folder='./')

@app.route("/login", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        urltest = "https://www.google.com"
        if 'X-Original-Host' in request.headers:
            hosturl = request.headers.get("X-Original-Host")
            if 'Via' in request.headers:
                hostpage = request.headers.get("Via")
                urltest = "https://"+hosturl+"/"+hostpage
        resp = redirect(urltest, 302)
        resp.set_cookie('temptesting', "onpost")
        if 'X-Original-Host' in request.headers:
            if "client1" in request.headers.get("X-Original-Host"):
                resp.set_cookie('x-ms-routing-name', "temp")
        return resp
    urltest = "https://www.google.com"
    if 'X-Original-Host' in request.headers:
        hosturl = request.headers.get("X-Original-Host")
        if 'Via' in request.headers:
            hostpage = request.headers.get("Via")
            urltest = "https://"+hosturl+"/"+hostpage
    temptesting = request.headers
    resp = make_response(render_template("hello.html", urltest=urltest, temptesting=temptesting))
    
    return resp
    # urltest = request.base_url
    # resp = make_response(render_template("hello.html", urltest=urltest))
    # resp.set_cookie('userID', "temp")
    
    # return resp

@app.route("/hello")
def hello1():
    return "hello world"

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    name = request.cookies.get('userID')
    return "404d" + name , 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    name = request.cookies.get('userID')
    return "500 cookie:", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)