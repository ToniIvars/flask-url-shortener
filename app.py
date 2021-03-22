from flask import Flask, render_template, redirect, request, url_for, flash
from random import sample
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BFhsdDSBnsfgFDNGmjfgdsTSdhgfHGMJKFI'

def shortener(url):
    with open('urls.json', 'r+') as f:
        try:
            data = json.load(f)
            d_val = tuple(data.values())
            if url in d_val:
                return tuple(data.keys())[d_val.index(url)]

            digitos = 'ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz'
            url_acortada = f'http://localhost:5000/{"".join(sample(digitos, 7))}'

            dictionary = {url_acortada:url}
            data.update(dictionary)
            f.seek(0)

        except:
            digitos = 'ABCDEFGHIJKLMNOPQRSTUWXYZabcdefghijklmnopqrstuwxyz'
            url_acortada = f'http://localhost:5000/{"".join(sample(digitos, 7))}'

            data = {url_acortada:url}

        json.dump(data, f, indent=4)
        f.close()

    return url_acortada

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

@app.route('/<digitos>', methods=('GET',))
def redirect_to_url(digitos):
    url = f'http://localhost:5000/{digitos}'
    
    try:
        with open('urls.json', 'r') as f:
            dictionary = json.load(f)
            f.close()
    except:
        return render_template('redirect_error.html', url=url)
    
    if url in dictionary.keys():
        redirect_url = dictionary[url]
        return render_template('redirect.html', url=redirect_url)

    else:
        return render_template('redirect_error.html', url=url)

@app.route('/api')
def api_mode():
    url = request.args['url']

    if not url:
        return 'You must enter a url as an argument (/api?url=https://www.google.com)'

    elif 'http' not in url:
        return 'You must enter a valid url'

    url_acortada = shortener(url)

    return {'original':url, 'shortened':url_acortada}