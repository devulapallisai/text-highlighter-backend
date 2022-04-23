from os import environ
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv

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


@app.route("/api/addHighlight")
def addhighlight():
    '''
    Here we store all posted Highlights from frontend to database
    '''
    pass


@app.route("/api/getallhighlights", methods=['GET'])
def gethighlights():
    '''
    Here we send all highlighted texts to frontend 
    '''
    pass


@app.route("/api/posttextdata", methods=['POST'])
def posttext():
    '''
    Here we insert text documents into database
    '''

    pass


@ app.route("/api/gettextdata", methods=['GET'])
def gettext():
    '''
    Here we send all text documents available with database via backend to frontend
    '''
    try:
        textdata = mydb.Textfiledata
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
