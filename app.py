from flask import Flask, render_template, redirect, request, url_for, flash, abort
from random import sample
import json, os
from dotenv import load_dotenv

def page_not_found(e):
    return render_template('404.html'), 404

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_error_handler(404, page_not_found)

def shortener(url):
    with open('urls.json', 'r+') as f:
        digits = 'ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz'

        # Create the shortened URL merging 7 digits of above randomly
        shortened_url = f'{os.getenv("HOST")}/{"".join(sample(digits, 7))}'

        # Try-except for controlling if the json file is empty or not
        try:
            # If json file is not empty, load the data as a dictionary
            data = json.load(f)
            data_values = tuple(data.values())

            # If the url is already in the file, the function will return it
            if url in data_values:
                return tuple(data.keys())[data_values.index(url)]

            # The data is updated with the key-value pair of the urls
            dictionary = {shortened_url:url}
            data.update(dictionary)
            f.seek(0)

        except:
            # If json file is empty, this will set the data to be only the pair or urls
            data = {shortened_url:url}

        # Set the info in the file as the data we have already defined
        json.dump(data, f, indent=4)
        f.close()

    return shortened_url

@app.route('/', methods=('GET',))
def index():    
    return render_template('index.html')

@app.route('/acortado', methods=('GET', 'POST'))
def acortado():
    if request.method == 'POST':
        # Get the url from the form
        data = request.form['data']
    
        if not data:
            flash('Debes escribir una URL en el campo de texto.')
            return redirect(url_for('index'))

        elif 'http' not in data:
            flash('Debes escribir una URL válida.')
            return redirect(url_for('index'))

        url = shortener(data)
        return render_template('acortado.html', url=url)
        
    else:
        # Returns an error template if the method is GET
        return render_template('error.html')

@app.route('/<digits>', methods=('GET',))
def redirect_to_url(digits):
    url = f'{os.getenv("HOST")}/{digits}'
    
    # Tryes to load the data of the json file. It will fail if the file is empty
    try:
        with open('urls.json', 'r') as f:
            dictionary = json.load(f)
            f.close()
    except:
        return abort(404)
    
    # Check if the digits are in the json file. If they are, this will redirect to the url,
    # else it will return an error
    if url in dictionary.keys():
        redirect_url = dictionary[url]
        return render_template('redirect.html', url=redirect_url)

    else:
        return abort(404)

@app.route('/api')
def api_mode():
    # Gets the url from the 'url' arg of the url
    try:
        url = request.args['url']
    except:
        return 'You must enter a url as an argument (/api?url=https://www.google.com)'

    # Return errors if the 'url' arg doesen't exist or is not valid
    if not url:
        return 'You must enter a url as an argument (/api?url=https://www.google.com)'

    elif 'http' not in url:
        return 'You must enter a valid url'

    # Shortens the url
    shortened_url = shortener(url)

    # Returns a 'json object' with the original url and the shortened one
    return {'original':url, 'shortened':shortened_url}
