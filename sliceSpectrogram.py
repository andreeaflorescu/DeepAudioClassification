# Import Pillow:
from PIL import Image
import os.path

import errno

from config import spectrogramsPath, slicesPath

#Slices all spectrograms
def createSlicesFromSpectrograms(desiredSize):
    for filename in os.listdir(spectrogramsPath):
        if filename.endswith(".png"):
            sliceSpectrogram(filename,desiredSize)

#Creates slices from spectrogram
#TODO Improvement - Make sure we don't miss the end of the song
def sliceSpectrogram(filename, desiredSize, slicePath="", spectrogramPath=spectrogramsPath):
    genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

    # Load the full spectrogram
    img = Image.open(spectrogramPath+filename)

    #Compute approximate number of 128x128 samples
    width, height = img.size
    nbSamples = int(width/desiredSize)
    width - desiredSize

    #Create path if not existing
    if not slicePath:
        slicePath = slicesPath+"{}/".format(genre)

    if not os.path.exists(os.path.dirname(slicePath)):
        try:
            print(slicePath)
            # os.makedirs(os.path.dirname(slicePath))
            os.makedirs(slicePath)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    #For each sample
    for i in range(nbSamples):
            #Extract and save 128x128 sample
        startPixel = i*desiredSize
        imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
        if not slicePath:
            imgTmp.save(slicesPath+"{}/{}_{}.png".format(genre,filename[:-4],i))
        else:
            imgTmp.save(slicePath+"/{}_{}.png".format(filename, i))
