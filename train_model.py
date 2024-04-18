
import os
import csv
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Activation, MaxPooling2D, Dropout
from keras.optimizers import RMSprop
from keras.utils import to_categorical
from scikeras.wrappers import KerasClassifier
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import cv2



#define all necessary data structures
X_train = []
X_test = []
y_train = []
y_test = []
training_metadata = {}
testing_metadata = {}
training_image_names = set()
testing_image_names = set()



#get images to training data
#open image folder, randomly sleect 1000 to add to data
cnt = 0
dir = 'HAM10000_images_part_1'
for filename in os.listdir(dir):
    random_number = random.randint(1, 4)
    if random_number != 1:
        continue
    
    cnt += 1
    if cnt > 1000:
        break
    with Image.open(os.path.join(dir, filename)) as img:
        training_image_names.add(filename)

#add chosen images' answers
with open('HAM10000_metadata.csv', encoding="utf8") as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        if(row[1]+'.jpg' in training_image_names):
           training_metadata[row[1]+'.jpg'] = row[2]



#same process as above for test images
cnt = 0
dir = 'ISIC2018_Task3_Test_Images'
for filename in os.listdir(dir):
    random_number = random.randint(1, 2)
    if random_number != 1:
        continue
    
    cnt += 1
    if cnt > 1000:
        break
    with Image.open(os.path.join(dir, filename)) as img:
        testing_image_names.add(filename)

with open('ISIC2018_Task3_Test_GroundTruth.csv', encoding="utf8") as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        if(row[1]+'.jpg' in testing_image_names):
           testing_metadata[row[1]+'.jpg'] = row[2]
           


#filling in training & testing vectors
for key in training_metadata:
    if(os.path.exists(os.path.join('HAM10000_images_part_1', key))):
        with Image.open(os.path.join('HAM10000_images_part_1', key)) as img:
            img_data = np.array(img)
            X_train.append(img_data)
        y_train.append(int(training_metadata[key]))

for key in testing_metadata:
    if(os.path.exists(os.path.join('ISIC2018_Task3_Test_Images', key))):
        with Image.open(os.path.join('ISIC2018_Task3_Test_Images', key)) as img:
            img_data = np.array(img)
            X_test.append(img_data)
        y_test.append(int(testing_metadata[key]))
        


#scrambling data 
for i in range(len(X_train)):
    transform = random.randint(0,1)
    if (transform == 0):
        X_train.append(cv2.flip(X_train[i],1))
        y_train.append(y_train[i])
    else:
        X_train.append(cv2.blur(X_train[i],(4,4)))
        y_train.append(y_train[i])


X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)



#one hot encodings
X_train = X_train.reshape(len(X_train),450,600,3)
X_test = X_test.reshape(len(X_test),450,600,3)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

y_train = y_train.reshape((y_train.shape[0], -1))
y_test = y_test.reshape((y_test.shape[0], -1))




#create model
model = Sequential()
#layers
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(450,600,3)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(2, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


#training
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)
model.save('melanoma_classifier.keras')