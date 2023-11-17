from PIL import Image
import math
import scipy
import numpy as np
import imageio.v2 as iio
import matplotlib.pylab as plt
from flask import Flask, render_template, send_file, redirect, url_for, request, jsonify
from mpl_toolkits import mplot3d
from sklearn.decomposition import PCA
from matplotlib.pyplot import imread
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/combine", methods=["POST"])
def combine_words():
    word1 = request.form["value1"]
    word2 = request.form["word2"]
    combined_word = word1 + word2
    return jsonify({"combined_word": combined_word})


@app.route("/pca")
def test_pca():
    img = imread("static/images/dalat.jpg")
    img = img.astype(np.uint8)
    img = img / 255
    img_gray = np.mean(img, axis=2)  # Convert the image to grayscale
    plt.imshow(img_gray, cmap="gray")

    # Reshape the image to a 2D array
    img_2d = img_gray.reshape(-1, img_gray.shape[1])

    perct = int(request.args.get("value1"))
    pca = PCA(n_components=perct)
    transformed = pca.fit_transform(img_2d)
    projection = pca.inverse_transform(transformed)

    # Reshape the projection image back to the original shape
    projection = projection.reshape(img_gray.shape)
    # Create the "image" folder if it doesn't exist
    if not os.path.exists("static/images"):
        os.makedirs("static/images")

    # Get the number of files already in the folder
    file_count = len(os.listdir("static/images"))

    # Save the image with an auto-incremented name
    filename = f"static/images/image_{file_count + 1}.png"
    plt.imsave(filename, projection, cmap="gray")

    image_url = f"../{filename}"  # Construct the URL for the image

    return jsonify({"image_url": image_url, "combined_word": perct})


if __name__ == "__main__":
    app.run()
