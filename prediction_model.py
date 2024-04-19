import numpy as np
from keras.models import load_model
from PIL import Image
import sys
sys.stdout.reconfigure(encoding='utf-8')


#prediction model
model = load_model("melanoma_classifier.keras")


X_train = []
with Image.open('uploaded_img.jpg') as img:
    img_data = np.array(img.convert("RGB").resize((450, 600)))
    X_train.append(img_data)

X_train = np.array(X_train)
X_train = X_train.reshape(len(X_train), 450, 600, 3)


print(model.predict(X_train[0:1])[0][0])