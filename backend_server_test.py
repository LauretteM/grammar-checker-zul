from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy storage
sentences = []
suggestions = []
reports = []
edits = []

# POST request to store 
@app.route('/api/store-sentence', methods=['POST'])
def store_sentence():
    data = request.get_json()
    sentence = data.get('sentence')
    sentences.append(sentence)
    return jsonify({'message':'Sentence stored successfully'})

# POST request to store rejected suggestion
@app.route('/api/reject-suggestion', methods=['POST'])
def reject_suggestion():
    data = request.get_json()
    incorrect_sentence = data.get('incorrect_sentence') # Assuming we store the sentence as incorrect
    suggestions.append({'type': 'reject', 'sentence': incorrect_sentence})
    return jsonify({'message': 'Rejection stored successfully'})

# POST request to store reason for report along with sentence
@app.route('/api/store-report', methods=['POST'])
def store_report():
    data = request.get_json()
    reason = data.get('reason')
    sentence = data.get('sentence')
    reports.append({'reason': reason, 'sentence': sentence})
    return jsonify({'message': 'Report stored successfully'})

# POST request to store edited sentences [WIP]
@app.route('/api/store-edit', methods=['POST'])
def store_edit():
    data = request.get_json()
    incorrect_sentence = data.get('incorrect_sentence')
    correct_sentence = data.get('correct_sentence')
    edits.append({'incorrect_sentence': incorrect_sentence, 'correct_sentence': correct_sentence})
    return jsonify({'message': 'Edit stored successfully'})

if __name__ == '__main__':
    app.run(debug=True)