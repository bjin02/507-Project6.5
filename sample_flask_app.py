# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
from config import FLICKR_API_KEY
import requests
import json
# Set up application
app = Flask(__name__)

manager = Manager(app)

# Routes

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {}</h1>'.format(yourname)

@app.route('/showvalues/<name>')
def basic_values_list(name):
    lst = ["hello","goodbye","tomorrow","many","words","jabberwocky"]
    if len(name) > 3:
        longname = name
        shortname = None
    else:
        longname = None
        shortname = name
    return render_template('values.html',word_list=lst,long_name=longname,short_name=shortname)


## PART 1: Add another route /word/<new_word> as the instructions describe.
@app.route('/word/<new_word>')
def new_word(new_word):
    baseurl = 'https://api.datamuse.com/words?rel_rhy='
    response_obj = requests.get(baseurl+new_word)
    word_data = json.loads(response_obj.text)
    similar_word = word_data[0]['word']
    return '<h1> {}</h1>'.format(similar_word)

## PART 2: Edit the following route so that the photo_tags.html template will render
@app.route('/flickrphotos/<tag>/<num>')
def photo_titles(tag, num):
    # HINT: Trying out the flickr accessing code in another file and seeing what data you get will help debug what you need to add and send to the template!
    # HINT 2: This is almost all the same kind of nested data investigation you've done before!
    FLICKR_KEY = FLICKR_API_KEY # TODO: fill in a flickr key
    baseurl = 'https://api.flickr.com/services/rest/'
    params = {}
    params['api_key'] = FLICKR_KEY
    params['method'] = 'flickr.photos.search'
    params['format'] = 'json'
    params['tag_mode'] = 'all'
    params['per_page'] = num
    params['tags'] = tag
    response_obj = requests.get(baseurl, params=params)
    trimmed_text = response_obj.text[14:-1]
    flickr_data = json.loads(trimmed_text)
    photo_titles = []
    for each in flickr_data['photos']['photo']:
        photo_titles.append(each['title'])
    return render_template('photo_info.html', num = num, photo_titles = photo_titles)

if __name__ == '__main__':
    manager.run() # Runs the flask server in a special way that makes it nice to debug
