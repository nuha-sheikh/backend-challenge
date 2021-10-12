import pymongo
from urllib.parse import urlparse
from bson.objectid import ObjectId

class Image():
    def __init__(self, title, caption, url, categories):
        if not (title and caption and url and categories):
            raise ValueError("ERROR: Invalid")
        self.title = title 
        self.caption = caption 
        self.url = url 
        
        categories_list = []
        for category in categories.split(','):
            categories_list.append(category.lower().strip())
        
        self.categories = categories_list

    #Return all images
    @staticmethod
    def get_images(collection):
        images = collection.find()
        return images
    
    #Return image with corresponding id
    @staticmethod
    def get_image(collection, id):
        result = collection.find_one({"_id" : ObjectId(id)})
        return result
    
    #Return images that match search query
    @staticmethod
    def search(collection, parameter):
        query = { "$or": [ {"title": {"$regex": parameter, "$options": "i"}}, {"caption": {"$regex": parameter, "$options": "i"}}, {"categories": parameter.lower()}]} 
        result = collection.find(query)
        return result
    
    #Structure images for template
    @staticmethod
    def struct_images(results):
        try:
            images = [[result['url'], result['title'], result['caption'], result['_id']] for result in results]
        except:
            images = [[results['url'], results['title'], results['caption'], results['_id']]]
        return images