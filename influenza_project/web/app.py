from flask import Flask, render_template
from flask import request
import pageviewapi
from pathlib import Path
from datetime import datetime, timedelta

app = Flask(__name__)

cases = {}
countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']



def get_features(country_name, current_date):

    prefix = {'austria':'de', 'belgium':'nl', 'germany':'de', 'italy':'it', 'netherlands':'nl'}

    project = prefix[country_name]+'.wikipedia'
    
    keywords_path = Path.cwd() / 'keywords'
    filepath = keywords_path / ('keywords_'+country_name+'.txt')

    current_date = current_date - timedelta(days=1)
    end = current_date.strftime('%Y%m%d')
    start_date = current_date - timedelta(days=6)
    start = start_date.strftime('%Y%m%d')

    features = []
    
    with filepath.open() as file:
        for line in file:
            count = 0
            res = pageviewapi.per_article(project, line.strip(), start, end, access='all-access', agent='all-agents', granularity='daily')
            for item in res['items']:
                count += int(item['views'])
            features.append(count)

    return features


def predict():
    for country in countries :
        cases[country] = 0.0
        # features =  get_features(country, datetime.now())
        #use model to predict values using the features vector and store in cases


                

@app.route('/')
def hello_world():
    # get_data('austria', 'happy')
    # res = pageviewapi.per_article('en.wikipedia', 'Paris', '20151106', '20151120', access='all-access',
                                   #agent='all-agents', granularity='daily')
    # for item in res['items']:
        # print(item['views'])
    # print(res['items'][0]['views'])

    # print(get_features('austria', datetime.now()))
    predict()
    return render_template('home.html', cases=cases)


if __name__ == '__main__':
    app.run(debug=True)
