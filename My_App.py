# from flask import Flask,jsonify,render_template,request
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from keras.models import model_from_json
# import random
# import os
# from werkzeug.utils import secure_filename
 
# ### Loadeng our model ###

# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
 
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

# ### Class of Prediction ###

# data_generation = ImageDataGenerator(rescale=1.0/255)

# def save_and_get_pred_img(image) :
#     defrance     = str(random.randint(1,100000))
#     file         = "D:\\BE AIML Honors Seminar\\GUI\\GUI" #change to eny dir
#     file_path    = os.path.join(file,defrance)
#     os.mkdir(file_path)
#     filename = secure_filename(image.filename)
#     next_file_path =os.path.join(file_path,defrance)
#     os.mkdir(next_file_path)
#     UPLOAD_FOLDER = next_file_path
#     my_wep_app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER
#     image.save(os.path.join(my_wep_app.config["IMAGE_UPLOADS"], image.filename))
#     return file_path 
 
# class Api_service :

#     def __init__(self,img_file_path):
#         self.img_file_path = img_file_path

#     def prediction_function(self) :
#         predict_generation = data_generation.flow_from_directory( self.img_file_path,target_size=(25,25),batch_size=10
#                                                                 ,class_mode='categorical')

#         prediction = loaded_model.predict_generator(predict_generation)
#         has_cancer = 'The percentage of no cancer : '+ str(round(prediction[0][1]*100,2)) + "%"
#         has_no_cancer='The Percentage of  cancer : ' + str(round(prediction[0][0]*100,2)) + '%'
#         return has_cancer,has_no_cancer 


 
# ### Creating our API & connected with HTML files ###
# my_wep_app = Flask(__name__)
# @my_wep_app.route("/")
# def home():
#     return render_template('new_index.html')
# @my_wep_app.route("/predict",methods=['GET', 'POST'])
# def result_page():
#    if request.method == "POST":

#         if request.files:
#             image = request.files["img"]
#             img_file_path = save_and_get_pred_img(image)
#             predict_img =Api_service(img_file_path)
#             has_cancer,has_no_cancer = predict_img.prediction_function()
#    return render_template("news-detail.html",has_cancer=has_cancer,has_no_cancer=has_no_cancer) 

# my_wep_app.run(debug=True)
from flask import Flask, jsonify, render_template, request
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image as keras_image
from keras.models import model_from_json
import numpy as np
import os
from werkzeug.utils import secure_filename
from io import BytesIO

### Loading our model ###
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

### Class of Prediction ###
def preprocess_image(image):
    image = keras_image.load_img(image, target_size=(25, 25))
    image = keras_image.img_to_array(image)
    image = image / 255.0  # Normalize image
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

class Api_service:
    def __init__(self, image):
        self.image = image

    def prediction_function(self):
        processed_image = preprocess_image(self.image)
        prediction = loaded_model.predict(processed_image)
        has_cancer = 'The percentage of no cancer: ' + str(round(prediction[0][1]*100, 2)) + "%"
        has_no_cancer = 'The Percentage of cancer: ' + str(round(prediction[0][0]*100, 2)) + '%'
        return has_cancer, has_no_cancer

### Creating our API & connecting with HTML files ###
my_web_app = Flask(__name__)

@my_web_app.route("/")
def home():
    return render_template('new_index.html')

@my_web_app.route("/predict", methods=['POST'])
def result_page():
    if request.method == "POST":
        if request.files:
            image = request.files["img"]
            image_bytes = image.read()
            image = BytesIO(image_bytes)
            predict_img = Api_service(image)
            has_cancer, has_no_cancer = predict_img.prediction_function()
            return render_template("news-detail.html", has_cancer=has_cancer, has_no_cancer=has_no_cancer)
    return jsonify({'error': 'No image found.'})

my_web_app.run(debug=True)
