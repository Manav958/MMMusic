import json
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_fscore_support
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

# Assuming you have a separate test set
# X_test_tfidf = tfidf_vectorizer.transform(test_texts)
# y_true = true_labels_for_test_set
# Make predictions on the test set
y_pred = clf.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_true, y_pred)
confusion_mat = confusion_matrix(y_true, y_pred)
precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
classification_rep = classification_report(y_true, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Confusion Matrix:\n{confusion_mat}')
print(f'Precision: {precision}\nRecall: {recall}\nF1-Score: {f1_score}')
print(f'Classification Report:\n{classification_rep}')

# Flask API endpoint for prediction
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
