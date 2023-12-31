# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hwlQaFz-0uXwkZ-HexLw8Daq_IHqT-q9
"""

import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from keras.utils import to_categorical
!pip install tensorflow

# Load datasets
train_data = pd.read_csv('mnist_train.csv')
test_data = pd.read_csv('mnist_test.csv')

# Explore the first few rows
print(test_data.head())

unique_classes = train_data['label'].nunique()
print("Number of unique classes:", unique_classes)

# Check the number of features
num_features = len(train_data.columns) - 1  # subtract 1 for the label column
print("Number of features:", num_features)

print("Missing values in training data:\n", train_data.isnull().sum())
print(" ")
print("Missing values in test data:\n", test_data.isnull().sum())
print(" ")
train_data = train_data.dropna()
# test_data = test_data.dropna()

print("Missing values in training data after drop na :\n", train_data.isnull().sum())
# print("Missing values in test data after drop na :\n", test_data.isnull().sum())
print(" ")

train_data.iloc[:, 1:] /= 255.0
test_data.iloc[:, 1:] /= 255.0
train_data

# Get rows with unique values in the specified column
unique_records_df = train_data.drop_duplicates(subset=['label'])


def resize_images(data):
    return data.iloc[:, 1:].values.reshape(-1, 28, 28)

resized_unique_train_images = resize_images(unique_records_df)

for image in resized_unique_train_images:
  plt.imshow(image, cmap='gray')
  plt.show()

X_train, X_val, y_train, y_val = train_test_split(
    train_data.iloc[:, 1:], train_data['label'], test_size=0.2, random_state=42
)

knn = KNeighborsClassifier()

# Define the parameter grid
param_grid = {'n_neighbors': np.arange(2, 9)}
param_grid
# Initialize the grid search
grid_search = GridSearchCV(knn, param_grid, cv=5)

# Fit the grid search
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best parameters: ", best_params)

# Make predictions
predictions = grid_search.predict(X_val)

# Print the accuracy and confusion matrix
print("Accuracy: ", accuracy_score(y_val, predictions))
print("Confusion Matrix: \n", confusion_matrix(y_val, predictions))

# Define the first model
model1 = Sequential([
   Dense(32, activation='relu', input_shape=(num_features,)),
   Dense(10, activation='softmax'),
])

# Compile the first model
model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define the second model
model2 = Sequential([
   Dense(64, activation='relu', input_shape=(num_features,)),
   Dense(10, activation='softmax'),
])

# Compile the second model
model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Convert labels to categorical
y_train_cat = to_categorical(y_train)
y_val_cat = to_categorical(y_val)

# Fit the first model
history1 = model1.fit(X_train, y_train_cat, epochs=10, batch_size=32, validation_data=(X_val, y_val_cat))

# Fit the second model
history2 = model2.fit(X_train, y_train_cat, epochs=10, batch_size=64, validation_data=(X_val, y_val_cat))

# Evaluate the first model
loss1, accuracy1 = model1.evaluate(X_val, y_val_cat)

# Evaluate the second model
loss2, accuracy2 = model2.evaluate(X_val, y_val_cat)

print("Model 1 Accuracy: ", accuracy1)
print("Model 2 Accuracy: ", accuracy2)

# Save the best model
if accuracy1 > accuracy2:
   model1.save('best_model.h5')
else:
   model2.save('best_model.h5')

# Reload the best model
best_model = load_model('best_model.h5')


# Get the first record (row) in the dataset
first_record = test_data.iloc[0]

# Extract pixel values (assuming they start from the second column)
image = first_record[1:].values.reshape(28, 28)

# Plot the image
print("first image data in test.")
plt.imshow(image, cmap='gray')
plt.show()
print("")
# Use the best model to make predictions on the test data
y_test_cat = to_categorical(test_data['label'])
predictions = best_model.predict(test_data.iloc[:, 1:])



# Assuming y_test_cat is in one-hot encoded format
y_test_labels = np.argmax(y_test_cat, axis=1)
predictions_labels = np.argmax(predictions, axis=1)

print("")
print("first predictions_labels label: ",predictions_labels[0])
print("")


# Print the confusion matrix
print("Confusion Matrix: \n", confusion_matrix(y_test_labels, predictions_labels))
print("")

# Calculate accuracy using accuracy_score
accuracy = accuracy_score(y_test_labels, predictions_labels)

# Print the confusion matrix and accuracy

print("Accuracy: {:.2%}".format(accuracy))