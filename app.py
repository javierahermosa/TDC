import os 
from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for
from flask.ext.basicauth import BasicAuth

app = Flask(__name__)

app.secret_key = "notemetaipo"
app.CSRF_ENABLED = True
app.WTF_CSRF_SECRET_KEY = '*YQUIHDHQYP#*p94uUOI'

app.config.update(
    DEBUG=True
)

app.config['BASIC_AUTH_USERNAME'] = 'teralytics'
app.config['BASIC_AUTH_PASSWORD'] = 'dataimpact'
basic_auth = BasicAuth(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

    
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route("/basics", methods=['GET', 'POST'])
@basic_auth.required
def basics():
    return render_template('basics.html')

@app.route("/challenge")
@basic_auth.required
def challenge():
    return render_template('challenge.html')
    
@app.route("/beyond")
@basic_auth.required
def beyond():
    return render_template('beyond.html')
    
@app.route("/onsite")
@basic_auth.required
def onsite():
    return render_template('onsite.html')

    
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)

