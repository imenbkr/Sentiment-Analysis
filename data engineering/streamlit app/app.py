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

# Establish connection to MySQL database
#db = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="reviews")

# Create a cursor to execute SQL queries
#cursor = db.cursor()

# Create a table to store user reviews if it doesn't exist


#create_table_query = 
#CREATE TABLE IF NOT EXISTS reviews (
#    id INT AUTO_INCREMENT PRIMARY KEY,
#    review_text TEXT,
#    sentiment VARCHAR(10),
#   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

#cursor.execute(create_table_query)
#db.commit()


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
                #insert_query = "INSERT INTO reviews (review_text, sentiment) VALUES (%s, %s)"
                #review_data = (review_input, prediction)
                #cursor.execute(insert_query, review_data)
                #db.commit()

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
    #cursor.close()
    #db.close()

# Function to classify the review
def classify_review(review):
    data = [review]

  
    #tokenizer.tokenize(data)
    #tokenizer.encode(data)
    #predict_input = tokenizer.encode(data,
    #           truncation=True,
    #            padding=True,
    #            return_tensors="tf")


    #tf_output = model.predict(predict_input)[0]
    #tf_prediction = tf.nn.softmax(tf_output, axis=1)

    #labels = ['Negative','Positive', 'Neutral'] #(0:negative, 1:positive, 2:neutral)
    #label = tf.argmax(tf_prediction, axis=1)
    #label = label.numpy()
    #prediction = model.predict(data)
    #return labels[label[0]]

# Function to generate a recommendation using colaboratif filtering
def generate_recommendation(user_input):
    """
    function still in development
    """
    return recommendation



if __name__ == '__main__':
    main()
