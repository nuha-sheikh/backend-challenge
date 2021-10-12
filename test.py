import unittest
import ssl
from image import Image
from pymongo import MongoClient
from bson.objectid import ObjectId

#Database Configeration
cluster = "mongodb+srv://nsheikh:k4L504qXqRbIMsvH@cluster0.kt5nm.mongodb.net/repository?retryWrites=true&w=majority"
client = MongoClient(cluster, ssl_cert_reqs=ssl.CERT_NONE)
db = client.repository
collection = db.test

#Sample Tests
class TestImage(unittest.TestCase):
    img_title = "test"
    img_categories = "test_label1,test_label2,test_label3"
    img_url = "https://test_image.com/test.jpg"
    img_caption = "test caption"

    def test_get_by_id(self):
        assert(Image.get_image(collection, "61660870a2d4f66e09921c27")['title'] == "Cherry Blossom")

    def test_image_success(self):
        img = Image(self.img_title, self.img_caption, self.img_url, self.img_categories)
        assert(img.title == self.img_title and img.categories == self.img_categories.split(',') and img.url == self.img_url and img.caption == self.img_caption)

    def test_image_failure(self):
        self.assertRaises(ValueError, Image, "", "", "", "")
    
    def test_search(self):
        result = Image.search(collection, "Pink")
        assert(result.count() == 2)

        result = Image.search(collection, "Tree")
        assert(result.count() == 1)

        result = Image.search(collection, "Nature")
        assert(result.count() == 3)

    def test_load_images(self):
        assert(Image.get_images(collection).count() == 3)

if __name__ == '__main__':
    unittest.main()