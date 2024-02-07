import json
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# Load and preprocess the JSON dataset
with open('C:/MMMusic/ds.json', 'r') as json_file:
    data = json.load(json_file)

# Extract keywords and corresponding moods
keywords = [entry['keywords'] for entry in data]
labels = [entry['mood'] for entry in data]

# Encode mood labels
label_to_id = {
    'Happy': 0,
    'Sad': 1,
    'Angry': 2,
    'Romantic': 3,
    'Energetic': 4
}

# Flatten the list of keywords into a single list of strings
texts = [' '.join(keyword) for keyword in keywords]

# Vectorize the text using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(texts)

# Train a Multinomial Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_tfidf, labels)




@app.route('/predict', methods=['POST'])
def predict_mood():
    user_input = request.json['message']

    # Vectorize the user input and make a prediction
    user_input_tfidf = tfidf_vectorizer.transform([user_input])
    predicted_mood = clf.predict(user_input_tfidf)[0]
    print(predicted_mood)
    return jsonify({'predicted_mood': predicted_mood})

if __name__ == '__main__':
    app.run(debug=True)
