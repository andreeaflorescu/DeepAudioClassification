#Define paths for files
spectrogramsPath = "Data/Spectrograms/"
slicesPath = "Data/Slices/"
datasetPath = "Data/Dataset/"
rawDataPath = "Data/Raw/"
musicDBPath = "music_db"

#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128

#Dataset parameters
filesPerGenre = 300
validationRatio = 0.2
testRatio = 0.1

#Model parameters
batchSize = 10
learningRate = 0.01
nbEpoch = 20

# predict labels
latino_index = 0
disco_index = 1

predict_labels= {latino_index: "latino", disco_index: "disco"}
