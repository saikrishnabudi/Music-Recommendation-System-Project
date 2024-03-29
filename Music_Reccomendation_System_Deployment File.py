# -*- coding: utf-8 -*-
"""Music reccomendation system -Deployment

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_PUGl2otsFe4BhKSbWUUD-xO2QhyIHXD

# **Model Deployment**
"""

df = pd.read_csv("/content/universal_top_spotify_songs.csv",encoding="unicode_escape")

# Load data into Surprise Dataset
reader = Reader(rating_scale=(0, 1000))
data = Dataset.load_from_df(df1[['name', 'artists', 'popularity']], reader)

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.4, random_state=25000)

# Build a collaborative filtering model (using SVD as an example)
model = SVD()
model.fit(trainset)

# Make predictions on the test set
predictions = model.test(testset)

# Evaluate the model
rmse = accuracy.rmse(predictions)
print(f'RMSE: {rmse}')

!pip install streamlit

# app.py
import streamlit as st
import joblib

# Load the trained model
model = joblib.load('collaborative_model.pkl')

# Streamlit app header
st.title('Music Recommendation App')

# Input form to get user preferences
danceability = st.slider('Danceability', 0.0, 1.0, 0.5)
energy = st.slider('Energy', 0.0, 1.0, 0.5)
loudness = st.slider('Loudness', -20.0, 0.0, -10.0)

# Button to trigger recommendations
if st.button('Get Recommendations'):
    # User preferences
    user_input = {'danceability': danceability, 'energy': energy, 'loudness': loudness}

    # Make recommendations using the model
    recommendations = model.predict(user_input)

    # Display recommendations
    st.success(f'Recommended Songs: {recommendations.tolist()}')

from flask import Flask, jsonify, request

app = Flask(__name__)

# Load collaborative model
model_filename = 'collaborative_model.pkl'
_, loaded_model = dump.load(model_filename)

# Load TF-IDF vectorizer and tfidf_matrix for content-based filtering
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df1['text_features'])

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Get user ID from request
    user_id = request.json['user_id']

    # Generate collaborative recommendations
    collaborative_recommendations = get_collaborative_recommendations(user_id)

    # Generate content-based recommendations
    content_based_recommendations = get_content_based_recommendations()

    return jsonify({
        'collaborative_recommendations': collaborative_recommendations,
        'content_based_recommendations': content_based_recommendations
    })

def get_collaborative_recommendations(user_id):
    recommendations = get_recommendations(user_id, loaded_model, df1)
    return recommendations

def get_content_based_recommendations():
    # Choose a list of indices for which you want recommendations
    song_indices = [1, 90, 180, 360, 450, 540, 630, 720, 810, 900]
    content_based_results = []

    for song_index in song_indices:
        cosine_similarities = linear_kernel(tfidf_matrix[song_index], tfidf_matrix).flatten()
        similar_songs = cosine_similarities.argsort()[:-1][::-1]
        top_recommendations = df1.iloc[similar_songs[:1]][['name', 'artists', 'popularity']].to_dict()
        content_based_results.append(top_recommendations)

    return content_based_results

if __name__ == '__main__':
    app.run(debug=True)