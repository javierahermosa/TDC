import os 
from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for


app = Flask(__name__)

app.secret_key = "notemetaipo"
app.CSRF_ENABLED = True
app.WTF_CSRF_SECRET_KEY = '*YQUIHDHQYP#*p94uUOI'

app.config.update(
    DEBUG=True
)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

    
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)

