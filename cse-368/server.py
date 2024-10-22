from flask import Flask, request, render_template, jsonify, send_from_directory
from pymongo import MongoClient
from html import escape

""""""
app = Flask(__name__)
# mongo_clinet = MongoClient('mongo') #creating total message database (will be used to respond to the AI bot)
# db = mongo_clinet["message"]
# collection= db["message"]
# **to run server locally do: python server.py**
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/message_sent',methods=['POST'])
def message_handler():
    if(request.method == 'POST'):
        message = request.get_json() #get message dict
        """ The bot message will be dealt with in another function"""

        # collection.insert_one({"user":"user", "message":message["message"]}) #insert object into db
        return jsonify([{"name":"user", "message":message["message"]}, {"name":"bot","message":"placeholder"}])
    else: #return forbidden if not a post request 
        return ('', 403) 

def bot_message_hander():
    pass
if __name__ == "__main__":
    #** to run server locally do: python server.py, go to http://localhost:8080/ **
    app.run(host='0.0.0.0', port=8080, debug=True)