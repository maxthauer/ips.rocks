#!/usr/bin/python3
from flask import *

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
	if request.headers.getlist("X-Forwarded-For"):
		clientip = request.headers.getlist("X-Forwarded-For")[0]
		return clientip
	else:
		clientip = request.remote_addr
		return clientip
if __name__ == '__main__':
  app.run(debug=True, use_reloader=False, port=8080)
