from flask import Flask, request, render_template, jsonify, send_from_directory
from pymongo import MongoClient
from html import escape
import NLPmodel
import pandas as pd

new_events_data = pd.read_csv('csv_files/ub_events.csv')
new_campus_living_data = pd.read_csv('csv_files/campus_living_info.csv')
new_school_data = pd.read_csv('csv_files/ub_campus.csv')

events_data = new_events_data[new_events_data['Event Name'].notna()]
campus_living_data = new_campus_living_data[new_campus_living_data['Link Text'].notna()]
school_data = new_school_data[new_school_data['School/College Name'].notna()]

events_data.columns = events_data.columns.str.strip()
campus_living_data.columns = campus_living_data.columns.str.strip()
school_data.columns = school_data.columns.str.strip()


app = Flask(__name__)
# mongo_clinet = MongoClient('mongo') #creating total message database (will be used to respond to the AI bot)
# db = mongo_clinet["message"]
# collection= db["message"]
# **to run server locally do: python server.py**
first = True
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/message_sent',methods=['POST'])
def message_handler():
    global first
    if(request.method == 'POST'):
        message = request.get_json() 
        user_message = message["message"] 
        bot_response = bot_message_handler(user_message)
    
        return jsonify([{"name":"user", "message":message["message"]}, {"name":"bot","message":f"{bot_response}\n"}])
    else:
        return ('', 403) 

def bot_message_handler(user_message):
    
    return NLPmodel.answer_query(user_message.lower(),events_data,campus_living_data,school_data)

if __name__ == "__main__":
    #** to run server locally do: python server.py, go to http://localhost:8080/ **
    app.run(host='0.0.0.0', port=8080, debug=True)