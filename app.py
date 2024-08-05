from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:jungle@cluster0.sgh4pki.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.assignment
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')
