import ssl
from pymongo import MongoClient
from image import Image
from flask import Flask, render_template, request
from bson.json_util import dumps

app = Flask(__name__)
 
#Database Configeration
cluster = "mongodb+srv://nsheikh:k4L504qXqRbIMsvH@cluster0.kt5nm.mongodb.net/repository?retryWrites=true&w=majority"
client = MongoClient(cluster, ssl_cert_reqs=ssl.CERT_NONE)
db = client.repository
collection = db.images

#Routes

#Home: view all images within database
@app.route('/', methods=['GET'])
def home():
    images = Image.get_images(collection)
    result = struct_images(images)
    return render_home(result)

#Search: search for images by their title, category, caption
@app.route('/search', methods=['POST'])
def search():
    parameter = request.form['parameter']
    images = Image.search(collection, parameter)
    result = struct_images(images)
    return render_home(result)

#Select Image: view image details, view similar images 
@app.route('/img/<id>', methods=['GET'])
def get_image(id):
    image = Image.get_image(collection, id)
    single_image = struct_images(image)
    
    similar_images = get_similar_images(image)
    
    if single_image[0] in similar_images: similar_images.remove(single_image[0])
    return render_image(single_image, similar_images)

def get_similar_images(image):
    categories = image["categories"]
    
    dup_arr = []
    for category in categories:
        dup_arr += Image.struct_images( Image.search(collection, category) )
    
    arr = list(map(list, set(map(tuple, dup_arr))))
    return arr

#Structure images for template
def struct_images(images):
    result = Image.struct_images(images)
    return result

#Render "Home" template
def render_home(result):
    return render_template("home.html", images=result)

#Render "Image" template
def render_image(image, similar_images):
    return render_template("image.html", image=image, images=similar_images)

if __name__ == '__main__':
	app.run()