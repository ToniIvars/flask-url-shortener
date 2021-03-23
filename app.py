from flask import Flask, render_template, redirect, request, url_for, flash, abort
from random import sample
import json

def page_not_found(e):
    return render_template('404.html'), 404

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BFhsdDSBnsfgFDNGmjfgdsTSdhgfHGMJKFI'
app.register_error_handler(404, page_not_found)

def shortener(url):
    with open('urls.json', 'r+') as f:
        digits = 'ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz'
        shortened_url = f'http://localhost:5000/{"".join(sample(digits, 7))}'

        try:
            data = json.load(f)
            data_values = tuple(data.values())
            if url in data_values:
                return tuple(data.keys())[data_values.index(url)]

            dictionary = {shortened_url:url}
            data.update(dictionary)
            f.seek(0)

        except:
            data = {shortened_url:url}

        json.dump(data, f, indent=4)
        f.close()

    return shortened_url

@app.route('/', methods=('GET',))
def index():    
    return render_template('index.html')

@app.route('/acortado', methods=('GET', 'POST'))
def acortado():
    if request.method == 'POST':
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
        return render_template('error.html')

@app.route('/<digits>', methods=('GET',))
def redirect_to_url(digits):
    url = f'http://localhost:5000/{digits}'
    
    try:
        with open('urls.json', 'r') as f:
            dictionary = json.load(f)
            f.close()
    except:
        return abort(404)
    
    if url in dictionary.keys():
        redirect_url = dictionary[url]
        return render_template('redirect.html', url=redirect_url)

    else:
        return abort(404)

@app.route('/api')
def api_mode():
    url = request.args['url']

    if not url:
        return 'You must enter a url as an argument (/api?url=https://www.google.com)'

    elif 'http' not in url:
        return 'You must enter a valid url'

    shortened_url = shortener(url)

    return {'original':url, 'shortened':shortened_url}