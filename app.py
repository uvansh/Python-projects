from flask import Flask,render_template,request
from textblob import TextBlob
import os
import plotly.graph_objs as go
from plotly.io import to_html

app=Flask(__name__)
sentiment_data = []

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

    return render_template('result.html', text=text, sentiment=sentiment, chart=chart)

def generate_chart(data):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [data.get('Positive', 0), data.get('Negative', 0), data.get('Neutral', 0)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return to_html(fig, full_html=False)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=os.environ.get('DEBUG', 'False') == 'True')