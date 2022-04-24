from os import environ
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import request

# Here we added .env file and that provides database password in connecting string to backend
load_dotenv('.env')
password = environ['PASSWORD']


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Here we have backend connection with database MongoDB Atlas using pyMongo ODM

CONNECTION_STRING = f'mongodb+srv://sai1975d:{password}@text-highlighter.umhna.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(CONNECTION_STRING)

mydb = client["mydb"]
textdata = mydb.Textfiledata


@app.route('/api/deletehighlight/<num>', methods=['POST'])
def deletehightlight(num):
    '''
    Here we delete the highlighted texts that user doesn't want to see
    '''
    try:
        request_data = request.get_json()
        deletedstart = request_data["deletedstart"]
        deletedend = request_data["deletedend"]
        textdata.update_one(
            {'sno': num}, {"$pull": {"highlights": {
                "start": deletedstart, "end": deletedend}}})

        return "success", 200
    except Exception as e:
        print('Exception ', e)
        return "Internal server error", 500


@app.route("/api/addHighlight", methods=['POST'])
def addhighlight():
    '''
    Here we store all posted Highlights from frontend to database
    '''
    try:
        request_data = request.get_json()
        sno = request_data["sno"]
        highlight = request_data["highlight"]
        start = request_data["start"]
        end = request_data["end"]
        textdata.update_one({'sno': sno}, {"$push": {"highlights": {
            "highlight": highlight, "start": start, "end": end}}})
        return "success", 200
    except Exception as e:
        print('Exception ', e)
        return "Internal server error", 500


@app.route("/api/getallhighlights/<num>")
def gethighlights(num):
    '''
    Here we send all highlighted texts to frontend 
    '''
    try:
        highlights = []
        for doc in textdata.find({'sno': num}):
            for i in doc['highlights']:
                highlights.append(i)

        return jsonify(highlights), 200
    except Exception as e:
        print('Exception ', e)
        return "Internal server error", 500


@app.route("/api/posttextdata")
def posttext():
    '''
    Here we insert text documents into database
    For example uncomment the below one to insert text
    '''
    # textdata.insert_one({'text': 'A robust weather application to provide current and 24 hour 7-day weather forecast for any city in the world built with ❤️ using React. Weather forecast data is powered by Dark Sky and city search Learning JavaScript Data Structures and Algorithms (Third Edition), published by Packt'})
    # textdata.update_many({"text": {"$exists": True}},
    #                      {"$set": {"highlights": []}})
    return "<p>Thanks for pushing new text</p>", 200


@ app.route("/api/gettextdata", methods=['GET'])
def gettext():
    '''
    Here we send all text documents available with database via backend to frontend
    '''
    try:
        textfiles = []
        for file in textdata.find({}):
            textfiles.append(file["text"])
        textfiles.reverse()
        return jsonify(textfiles), 200
    except Exception as e:
        print(e)
        return "Internal server error", 500


@ app.route("/")
def hello_world():
    return "<p>Hello from backend Flask. Go to the <a href='http://localhost:3000/'>frontend</a></p>"


if __name__ == "__main__":
    app.run(debug=True)
