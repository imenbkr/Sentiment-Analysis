import streamlit as st
import pickle
import openai
import numpy as np
#import transformers
#from transformers import BertTokenizer,TFBertForSequenceClassification
#import tensorflow as tf

#from tensorflow.keras.models import Model
#from tensorflow.keras.layers import Activation, Dense, Input


# Load the Logistic Regression model
#model = pickle.load(open('Logistic_Regression_model.pkl', 'rb'))
#model = pickle.load(open())

#tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')




# Configure OpenAI GPT-3
openai.api_key = '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'
chatbot_model = 'gpt-3.5-turbo'

# Establish connection to MySQL database

# Create a cursor to execute SQL queries
#cursor = db.cursor()

# Create a table to store user reviews if it doesn't exist


# Streamlit app
def main():
    st.title("Review Classification and Recommendation")

    # Sidebar navigation
    option = st.sidebar.radio("Select an option", ('Review Classification', 'Recommendation'))

    if option == 'Review Classification':
        st.subheader("Review Classification")

        # Input form for reviews
        review_input = st.text_area("Enter your review", height=200)
        if st.button("Predict"):
            if review_input:
                prediction = classify_review(review_input)

                # Insert review and prediction into the database
                

                st.write("Prediction:", prediction)
            else:
                st.warning("Please enter a review.")
                

    elif option == 'Recommendation':
        st.subheader("Recommendation")

        # Input form for user input
        user_input = st.text_area("Ask for a recommendation")
        if st.button("Get Recommendation"):
            if user_input:
                recommendation = generate_recommendation(user_input)
                st.write("Recommendation:", recommendation)
            else:
                st.warning("Please enter your request.")
# Close the database connection


# Function to classify the review
def classify_review(review):
    data = [review]

    """
    tokenizer.tokenize(data)
    tokenizer.encode(data)
    predict_input = tokenizer.encode(data,
                truncation=True,
                padding=True,
                return_tensors="tf")


    tf_output = model.predict(predict_input)[0]
    tf_prediction = tf.nn.softmax(tf_output, axis=1)

    labels = ['Negative','Positive', 'Neutral'] #(0:negative, 1:positive, 2:neutral)
    label = tf.argmax(tf_prediction, axis=1)
    label = label.numpy()
    #prediction = model.predict(data)
    return labels[label[0]]
    """

# Function to generate a recommendation using OpenAI GPT-3
def generate_recommendation(user_input):
    response = openai.Completion.create(
        engine=chatbot_model,
        prompt=user_input,
        max_tokens=50,
        temperature=0.7
    )
    recommendation = response.choices[0].text.strip()
    return recommendation



if __name__ == '__main__':
    main()
