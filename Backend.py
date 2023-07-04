import os
import numpy as np
from skimage import io
from skimage.feature import graycomatrix, graycoprops
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
metric_texture = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']

def glcm_matrix(image):
    glcm = graycomatrix(image, distances=[1], angles=angles, levels=256, symmetric=True, normed=True)
    features = []
    for i in metric_texture:
        feature = []
        for j in angles:
            feature.append(graycoprops(glcm, prop=i)[0, 0])
        features.extend(feature)
    return np.array(features)

X = []  # Features
y = []  # Labels

image_path = "dataset training/"

def load_images_and_extract_features(directory, label, X, y):
    image_paths = os.listdir(directory)
    for img_path in image_paths:
        image = io.imread(os.path.join(directory, img_path))
        features = glcm_matrix(image)
        X.append(features)
        y.append(label)

load_images_and_extract_features(f"{image_path}happy/", 1, X, y)    # Load citra dengan ekspresi happy
load_images_and_extract_features(f"{image_path}sad/", 0, X, y)      # Load citra dengan ekspresi sad

# Pisahkan data menjadi data latih (80%) dan data uji (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def knn_predict(features, n):
    knn = KNeighborsClassifier(n_neighbors=n)               # Inisialisasi model KNN
    knn.fit(X_train, y_train)                               # Latih model
    prediction = knn.predict([features])                    # Prediksi sentimen
    accuracy_percentage = knn.score(X_test, y_test) * 100   # Evaluasi model
    return prediction[0], accuracy_percentage

def knn_score(n):
    knn = KNeighborsClassifier(n_neighbors=n)               # Inisialisasi model KNN
    knn.fit(X_train, y_train)                               # Latih model
    accuracy_percentage = knn.score(X_test, y_test) * 100   # Evaluasi model
    return accuracy_percentage.round(2)

def get_data():
    return [len(X_train), len(X_test)]