#''' Deploy user recomender model using flask framework'''

# Import Relevant Modules
try:
    import pickle
    import joblib
    from flask import request, render_template
    import pandas as pd

except ImportError as i_error:
    print(i_error)

# Load the datasets needed for deployment
CAC_DB = pd.read_csv('used_data/cac_db.csv')
CAC_DB['name'] = CAC_DB.name.str.lower()

import pandas as pd
from difflib import get_close_matches
​
cac_db = pd.read_csv(r'data\cac_db.csv')
​
​
def search(word):
    word = word.upper()
​
    def start(x):
        if x.startswith(word):
            return True
        else:
            return False
​
    if len(cac_db[cac_db['COMPANY NAME'].apply(start)]) > 0:
        return cac_db[cac_db['COMPANY NAME'].apply(start)]
    elif len(get_close_matches(word, cac_db['COMPANY NAME'], 5, cutoff=0.7)) > 0:
        return get_close_ma

# Initialize the app
APP = Flask(__name__)

'''HTML GUI '''

# Render the home page
@APP.route('/')
def home():
    '''Display of web app homepage'''
    return render_template('index.html')

# render the new_user_recommend page
@APP.route('/company_search')
def company_find():
    '''Display of result of search'''
    return render_template('company_search.html')


# render the new user recommend page
@APP.route('/search', methods=['POST'])
def company_find():
    '''Function that accepts the company name displays search result
    for Web App Testing'''
    # get the values from the form
    try:
        word = [x for x in request.form.values()]
        for w in word:
            word = w.lower()

        company = search(word) 
        return render_template('cac_search.html', prediction_text=company_name)
    except KeyError:
        return render_template('cac_search.html', prediction_text=["company does not exist"])


# run the app
if __name__ == "__main__":
    APP.run(debug=True)
