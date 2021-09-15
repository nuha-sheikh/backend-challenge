import re
import os
from flask import Flask, render_template, redirect

app = Flask(__name__)

tags = ['trees', 'pink', 'sky', 'green', 'flowers', 'white', 'lake', 'blue']

images_tag = []

database = [
    {
        "title" : "Cherry Blossom Tree",
        "caption" : "Pink Cherry Blossom Tree in the Meadow",
        "id" : 0,
        "path" : "tree-1.jpg",
        "characteristics": ['trees', 'pink', 'sky', 'blue'],
        "similar": ['tree-2.jpg']
    }, 
    {
        "title" : "Large Green Tree",
        "caption" : "Large Green Tree in the Meadow",
        "id" : 1,
        "path" : "tree-2.jpg",
        "characteristics": ['trees', 'green', 'sky', 'blue'],
        "similar": ['tree-1.jpg']
    },
    {
        "title" : "Pink Flower",
        "caption" : "Pink Flower Sprouting",
        "id" : 2,
        "path" : "flower-1.jpg",
        "characteristics": ['flowers', 'pink', 'green'],
        "similar": ['flower-2.jpg']
    },
    {
        "title" : "Daisy Flower",
        "caption" : "A Bunch of Daisies",
        "id" : 3,
        "path" : "flower-2.jpg",
        "characteristics": ['flowers', 'white', 'green'],
        "similar": ['flower-1.jpg']
    },
    {
        "title" : "Lake Louise",
        "caption" : "Lake Louise, Alberta",
        "id" : 4,
        "path" : "lake-1.jpg",
        "characteristics": ['blue', 'lake', 'trees', 'sky'],
        "similar": ['lake-2.jpg']
    },
    {
        "title" : "Lake with an Island",
        "caption" : "Large Blue Lake with an Island",
        "id" : 5,
        "path" : "lake-2.jpg",
        "characteristics": ['blue', 'lake', 'trees', 'sky'],
        "similar": ['lake-1.jpg']
    }
]

@app.route('/')
def home():
    return render_template('home.html', database=database, tags=tags)

@app.route('/tags/<tag>')
def display_tag(tag):
    images_tag = []
    for image in database:
        if str(tag) in image['characteristics']: images_tag.append(image)
    if images_tag: return render_template('home.html', database=images_tag, tags=tags)
    return redirect('/')

@app.route('/img/<path>')
def display_image(path):
    for image in database:
        if str(path) == image['path']: return render_template('display-image.html', image=image)
    return redirect('/')

app.run()