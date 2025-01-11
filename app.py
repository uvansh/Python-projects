from flask import Flask,render_template,request
from textblob import TextBlob
import os

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/analyze',methods=['POST'])
def analyze():
    text = request.form['text']
    analysis = TextBlob(text)
    sentiment="Positive " if analysis.sentiment.polarity>0 else "Negative" if analysis.sentiment.polarity<0 else "Neutral"
    return render_template('result.html',text=text,sentiment=sentiment)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=os.environ.get('DEBUG', 'False') == 'True')