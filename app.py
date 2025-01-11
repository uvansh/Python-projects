from flask import Flask,render_template,request
from textblob import TextBlob
import os
import openai
import plotly.graph_objs as go
from plotly.io import to_html

app=Flask(__name__)
sentiment_data = []


openai.api_key = os.getenv("OPENAI_api_key")

def generate_personalized_recommendation(sentiment, text):
    prompt = f"""
    The user just analyzed a piece of text. The sentiment of the text is {sentiment}. Based on this sentiment, 
    generate a personalized, positive, motivational or helpful message for the user. 
    The text from the user is: "{text}".
    Respond in a friendly, conversational tone.
    """
    
    # Call OpenAI API for response
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines like "gpt-3.5-turbo"
        prompt=prompt,
        max_tokens=100,  # Limit the response length
        temperature=0.7  # Controls the randomness of the response
    )
    
    # Extract and return the recommendation
    return response.choices[0].text.strip()

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
    colors = ['#36a2eb', '#ff6384', '#ffcd56']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,marker=dict(colors=colors))])
    return to_html(fig, full_html=False)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=os.environ.get('DEBUG', 'False') == 'True')