import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load and preprocess the JSON dataset
with open('C:\MMMusic\ds.json', 'r') as json_file:
    data = json.load(json_file)

# Extract keywords and corresponding moods
keywords = [entry['keywords'] for entry in data]
labels = [entry['mood'] for entry in data]

# Encode mood labels
label_to_id = {
    'happy': 0,
    'sad': 1,
    'angry': 2,
    'romantic': 3,
    'energetic': 4
}

# Flatten the list of keywords into a single list of strings
texts = [' '.join(keyword) for keyword in keywords]

# Vectorize the text using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(texts)

# Train a Multinomial Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_tfidf, labels)

# Continuous prediction loop
while True:
    user_input = input("Enter text (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    # Vectorize the user input and make a prediction
    user_input_tfidf = tfidf_vectorizer.transform([user_input])
    predicted_mood = clf.predict(user_input_tfidf)[0]
    print("Predicted Mood:", predicted_mood)
