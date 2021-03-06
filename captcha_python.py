# -*- coding: utf-8 -*-
"""captcha.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d2yftIKYdueMuGzPOKw1J9H0o5OSX036
"""

from keras.datasets.mnist import load_data 
from keras.layers.advanced_activations import LeakyReLU
from keras.layers import Dense, Dropout, Input
from keras.models import Model, Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical
from matplotlib.pyplot import *
from numpy import *
from numpy.random import normal, randint

"""# GAN Network

## Defining GAN
"""

def discriminator():
    model = Sequential()
    model.add(Dense(784,input_dim=784))

    model.add(LeakyReLU(0.1))
    model.add(Dropout(0.1))
    model.add(Dense(400))

    model.add(LeakyReLU(0.1))
    model.add(Dropout(0.1))
    model.add(Dense(200))

    model.add(LeakyReLU(0.1))
    model.add(Dropout(0.1))
    model.add(Dense(100))

    model.add(LeakyReLU(0.1))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer=Adam(lr=0.0002, beta_1=0.4))

    return model

def generator():
    model = Sequential()
    model.add(Dense(100,input_dim=100))

    model.add(LeakyReLU(0.1))
    model.add(Dense(200))

    model.add(LeakyReLU(0.1))
    model.add(Dense(400))

    model.add(LeakyReLU(0.1))
    model.add(Dense(784, activation="tanh"))
    model.compile(loss="binary_crossentropy", optimizer=Adam(lr=0.0002, beta_1=0.4))

    return model

"""## Preprocessing"""

batch_size = 128
epochs = 100

(x_train, y_train), (x_test, y_test) = load_data()

x_train = x_train/255
x_train = x_train.reshape(60000, 784)

gen = generator()
disc = discriminator()

disc.trainable = False

input = Input(shape=(100,))
output = disc(gen(input))
model = Model(inputs=input, outputs=output)

model.compile(loss="binary_crossentropy", optimizer=Adam(lr=0.0002, beta_1=0.4))

"""## Training GAN"""

for i in range(epochs):
    for j in range(batch_size):        
        x = x_train[randint(0,60000, size=batch_size)]
        y = gen.predict(normal(0,1, (batch_size, 100)))

        x = concatenate((x, y))
        y = zeros(batch_size * 2)
        y[:batch_size] = 1

        disc.trainable=True
        disc.train_on_batch(x, y)
        disc.trainable=False

        x = normal(0,1, (batch_size, 100))
        y = ones(batch_size)
        model.train_on_batch(x, y)

    print("Epoch",i+1,"/",epochs)

"""# Digit Classifier"""

def digit_classifier():
  model = Sequential()
  model.add(Dense(784,input_dim=784))

  model.add(LeakyReLU(0.1))
  model.add(Dropout(0.1))
  model.add(Dense(400))

  model.add(LeakyReLU(0.1))
  model.add(Dropout(0.1))
  model.add(Dense(200))

  model.add(LeakyReLU(0.1))
  model.add(Dropout(0.1))
  model.add(Dense(100))

  model.add(LeakyReLU(0.1))
  model.add(Dropout(0.1))
  model.add(Dense(10, activation='softmax'))
  model.compile(optimizer="sgd", loss='categorical_crossentropy', metrics=['accuracy'])

  return model

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

classifier = digit_classifier()
classifier.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split = 0.1)

"""# Capcha Generator"""

# Rerun to regenerate captcha
images = gen.predict(normal(0, 1, size=(10, 100)))
predictions = classifier.predict(images)
labels = ""
for prediction in predictions:
  max_index = 0
  for j in range(len(prediction)-1):
    if prediction[max_index] < prediction[j+1]:
      max_index = j+1
  labels += str(max_index)

images = images.reshape(10,28,28)
figure(figsize=(25,25))
ans=[]
for i in range(10):
    subplot(1,10, i+1)
    axis("off")
    imshow(images[i])
savefig("capcha.png")

# User input of Captcha
value = "5080883883"  # Look at the captcha and enter digits without spaces here
if labels == value:
  print("Success")
else:
  print("Fail! Correct = ",labels, ", Input = ",value)