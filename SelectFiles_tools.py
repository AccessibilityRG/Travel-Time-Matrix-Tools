__author__ = 'hentenka'

import os, sys, random, shutil

def listFiles(topPath):
    ''' Creates a list from Travel Time Matrix file paths that are found from the directory and sub-folders of "topPath" '''
    f = []
    for root, dirs, files in os.walk(topPath):
        for filename in files:
            if filename.startswith('time_to_'):
                f.append(os.path.join(root, filename))
    return f

def selectQuery(inputFilesList,inputIDs):
    ''' Searches files based on inputIDs (YKR-ID) from the "inputFilesList" '''
    selected = []
    for id in inputIDs:
        q = 'time_to_' + str(id) + '.txt'
        for file in inputFilesList:
            basename = os.path.basename(file)
            if q in basename:
                selected.append(file)
                break
    return selected

def selectRandom(inputList, sampleSize):
    '''Creates a random selection of files with chosen sample size'''
    return random.sample(inputList, sampleSize)

def copyFiles(inputFilesList, destinationFolder):
    '''Copies files to a chosen destination folder'''

    #If folder does not exist, create one.
    if not os.path.isdir(destinationFolder):
        os.mkdir(destinationFolder)

    for file in inputFilesList:
        shutil.copy2(file, destinationFolder)

def main():
    inputPath = r"...\MetropAccess-matka-aikamatriisi_TOTAL"
    outputFolder = r"...\Test"

    #List all Matrix files
    files = listFiles(inputPath)

    #Create random selection with chosen sample size
    #randFiles = selectRandom(files, 600)

    #Select files based on list of YKR-IDs
    YKR_ids = [5894644,5970404]
    selectedFiles = selectQuery(files, YKR_ids)

    #Copy files to a directory
    copyFiles(selectedFiles, outputFolder)
    #copyFiles(randFiles, outputFolder)

if __name__ == '__main__':
    main()
