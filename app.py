from flask import Flask
from flask import Flask, render_template,url_for,request,session,redirect
from flask_session import Session

import sys
sys.path.append('../')

from bseapi import BSEDailyStockQuotes 


app = Flask(__name__)
sess=Session()


@app.route("/")
def main():
	return render_template('index.html')

@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/panel")
def panel():
	return render_template('panel.html')



if __name__ == "__main__":
	app.secret_key = 'sma_interiit'
	app.config['SESSION_TYPE'] = 'filesystem'
	sess.init_app(app)
	app.debug = True
	app.run()