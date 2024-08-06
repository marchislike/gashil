from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://kimwatson2026:HjvFSFwKAWPehGmd@gashil.yhejgv0.mongodb.net/?retryWrites=true&w=majority&appName=Gashil')
db = client.gashil
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('./pages/join.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)