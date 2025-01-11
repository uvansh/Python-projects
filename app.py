from flask import Flask, render_template, request
from textblob import TextBlob
import os
import openai
import plotly.graph_objs as go
from plotly.io import to_html
import logging

app = Flask(__name__)
sentiment_data = []

openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.DEBUG)

# Log the API key to ensure it's being set (do not do this in production)
logging.debug(f"OpenAI API Key: {openai.api_key}")

def generate_personalized_recommendation(sentiment, text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The user just analyzed a piece of text. The sentiment of the text is {sentiment}. Based on this sentiment, generate a personalized, positive, motivational or helpful message for the user. The text from the user is: '{text}'"}
    ]
    try:
        logging.debug(f"Calling OpenAI API with messages: {messages}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50
        )
        logging.debug(f"OpenAI response: {response}")
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Error generating recommendation"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    analysis = TextBlob(text)
    sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

    # Update sentiment data
    sentiment_data.append({"text": text, "sentiment": sentiment})
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for entry in sentiment_data:
        sentiment_counts[entry["sentiment"]] += 1

    # Generate the chart
    chart = generate_chart(sentiment_counts)

    # Generate personalized recommendation
    logging.debug(f"Generating recommendation for text: {text} with sentiment: {sentiment}")
    recommendation = generate_personalized_recommendation(sentiment, text)
    logging.debug(f"Generated recommendation: {recommendation}")

    return render_template('result.html', text=text, sentiment=sentiment, chart=chart, recommendation=recommendation)

def generate_chart(data):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [data.get('Positive', 0), data.get('Negative', 0), data.get('Neutral', 0)]
    colors = ['#36a2eb', '#ff6384', '#ffcd56']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    return to_html(fig, full_html=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=os.environ.get('DEBUG', 'False') == 'True')