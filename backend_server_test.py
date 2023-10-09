from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy storage
sentences = []
suggestions = []
reports = []
edits = []

