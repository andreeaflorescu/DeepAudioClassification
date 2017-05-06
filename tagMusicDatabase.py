import os
from config import musicDBPath
from audioFilesTools import setGenre, getGenre

'''
All files in a directory are tagged with the genre
specified by the directory name
'''

def tagFilesInDirectory(dir):
	for root, dirs, files in os.walk(dir):
		musicGenre = os.path.basename(dir)
		for audioFile in files:
			audioFilePath = os.path.join(dir, audioFile) 
			setGenre(audioFilePath, unicode(musicGenre, "utf-8"))
			
def tagMusicDatabase(dir):
	for root, dirs, files in os.walk(musicDBPath):
		for dir in dirs:
			tagFilesInDirectory(os.path.join(root, dir))

def testTagDB():
	for root, dirs, files in os.walk("music_db/latino"):
        	for file in files:
        	        wtf = os.path.join(root, file)
               		print getGenre(wtf)

tagMusicDatabase(musicDBPath)
# testTagDB()
