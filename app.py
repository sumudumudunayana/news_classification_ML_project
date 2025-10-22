from flask import Flask,render_template,request,redirect,session
from prediction import preprocessing, vectorizer, get_prediction

app = Flask(__name__)
app.secret_key = "key"

data = dict()

news = ['He won the championship!', 
        'New technology trends in 2024.', 
        'Local team wins big game.', 
        'Community event draws large crowd.', 
        'New cafe opens downtown.',
        'stock markets reach all-time high.',
        'scientists discover new species in the Amazon.']

world = 2
sports = 2
business = 1
scienceTechnology = 2

        

@app.route("/")
def index():
    data['news'] = news
    data['world'] = world
    data['sports'] = sports
    data['business'] = business
    data['science & technology'] = scienceTechnology
    prediction = session.pop('prediction', None) 
    return render_template('index.html', data=data, prediction=prediction)



@app.route("/", methods=['post'])
def my_post():
    text = request.form['headingInput']
    preprocessed_text = preprocessing(text)
    vectorized_text = vectorizer(preprocessed_text)
    prediction = get_prediction(vectorized_text)

    session['prediction'] = prediction

    if prediction == 'world':
        data['world'] += 1
    elif prediction == 'sports':
        data['sports'] += 1
    elif prediction == 'business':
        data['business'] += 1
    elif prediction == 'science & technology':
        data['science & technology'] += 1
    
    news.insert(0, text)

    return redirect(request.url)


if __name__ == "__main__":
    app.run()