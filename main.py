from flask import Flask, request
import os
import shutil
from product_detector import ProductDetector
import uuid

app = Flask(__name__)


@app.post('/')
def helloWorld():
    my_uuid = uuid.uuid4()

    file = request.files['product_image']
    file.save(f'tmp/{my_uuid}')

    product = ProductDetector().predictImage(my_uuid)
    return f'The product is {product}'


@app.get('/restore-folder')
def restoreFolder():
    folder = 'tmp'

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return 'Restored'        


if __name__ == '__main__':
    app.run(debug=True)
