# -*- coding: utf-8 -*-
import random
import string
import os
import sys
import numpy as np


from imageFilesTools import getImageData
from model import createModel
from datasetTools import getDataset
from config import slicesPath, spectrogramsPath, predict_labels
from config import batchSize
from config import filesPerGenre
from config import nbEpoch
from config import validationRatio, testRatio
from config import sliceSize
from sliceSpectrogram import sliceSpectrogram

from songToData import createSlicesFromAudio, createSpectrogram

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN", nargs='+', choices=["train","test","slice", "predict"])
parser.add_argument('--file-path', dest='file_path', default="", help='The path of the song on which to apply the prediction')
args = parser.parse_args()

print("--------------------------")
print("| ** Config ** ")
print("| Validation ratio: {}".format(validationRatio))
print("| Test ratio: {}".format(testRatio))
print("| Slices per genre: {}".format(filesPerGenre))
print("| Slice size: {}".format(sliceSize))
print("--------------------------")

if "slice" in args.mode:
    createSlicesFromAudio()
    sys.exit()

#List genres
genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]
nbClasses = len(genres)

#Create model
model = createModel(nbClasses, sliceSize)

if "train" in args.mode:
    print genres

    #Create or load new dataset
    train_X, train_y, validation_X, validation_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="train")

    #Define run id for graphs
    run_id = "MusicGenres - "+str(batchSize)+" "+''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))

    #Train the model
    print("[+] Training the model...")
    model.fit(train_X, train_y, n_epoch=nbEpoch, batch_size=batchSize, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
    print("    Model trained! ✅")

    #Save trained model
    print("[+] Saving the weights...")
    model.save('musicDNN.tflearn')
    print("[+] Weights saved! ✅💾")

if "test" in args.mode:

    #Create or load new dataset
    test_X, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")
    #Load weights
    print("[+] Loading weights...")
    model.load('musicDNN.tflearn')
    print("    Weights loaded! ✅")

    testAccuracy = model.evaluate(test_X, test_y)[0]
    print("[+] Test accuracy: {} ".format(testAccuracy))

if "predict" in args.mode:
    # Create or load new dataset
    # test_X, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")

    # Load weights
    # print("[+] Loading weights...")
    model.load('musicDNN.tflearn')
    # print("    Weights loaded! ✅")

    # # create spectogram for mp3
    spectrogram_filename = string.replace(args.file_path, ".mp3", "")
    # createSpectrogram(args.file_path, spectrogram_filename, "")

    # create slices
    sliceSize = 128
    spectrogram_path = spectrogram_filename + ".png"
    slices_path = spectrogram_filename + "_slices"
    # sliceSpectrogram(spectrogram_path, sliceSize, slices_path, "")

    # create predict data

    data = []
    filenames = os.listdir(slices_path)
    for file in filenames:
        imgData = getImageData(spectrogram_path, sliceSize)
        data.append(imgData)

    predict_x = np.array(data).reshape([-1, sliceSize, sliceSize, 1])
    predicted_probabilities = model.predict(predict_x)

    probabilities_sum = [0]*len(predict_labels)
    for pair in predicted_probabilities:
        for idx, val in enumerate(pair):
            probabilities_sum[idx] += val

    max_prob_index = -1
    max = 0
    for idx, val in enumerate(probabilities_sum):
        if val > max:
            max = val
            max_prob_index = idx

    print (max, predict_labels[max_prob_index])