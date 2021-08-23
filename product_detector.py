from PIL import Image, ImageOps
import tensorflow
import numpy as np
import re


class ProductDetector():
    # __init__ function
    def __init__(self):
        self = dict()

    def predictImage(self, image_name):

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = tensorflow.keras.models.load_model(
            './ml_models/products_model.h5')

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(f'tmp/{image_name}')

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)

        # Convert numpy_list to list
        prediction_list = list(prediction[0])

        # Get max value in prediction list
        max_value = max(prediction_list)

        print('')

        print(prediction_list)

        print('')

        return self.getProductName(list.index(prediction_list, max_value))

    # Get product name by index in prediction_list
    def getProductName(self, max_value_index):
        labels = self.loadLabels('./assets/labels.txt')
        return labels[max_value_index]

    # This function parses the labels.txt and puts it in a python dictionary
    def loadLabels(self, labelPath):
        p = re.compile(r'\s*(\d+)(.+)')
        with open(labelPath, 'r', encoding='utf-8') as labelFile:
            lines = (p.match(line).groups() for line in labelFile.readlines())
            return {int(num): text.strip() for num, text in lines}
