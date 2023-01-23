from flask import Flask, render_template
from contentful import Client



app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route("/sobre")
def about():
    client = Client(
    'r0iojhtvlgr2',
    'RaUhiKQRQMFANqWuoS4DTiVZXUPpNiBtFhiEv_7o1iw',
    environment='master'  # Optional - it defaults to 'master'.
    )
    entries = client.entries()

    return render_template('sobre.html', members=entries)