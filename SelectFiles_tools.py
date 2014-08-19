__author__ = 'hentenka'

import os, sys, random, shutil

def listFiles(topPath):
    f = []
    for root, dirs, files in os.walk(topPath):
        for filename in files:
            if filename.startswith('time_to_'):
                f.append(os.path.join(root, filename))

    return f

def selectQuery(inputFilesList,inputIDs):
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
    return random.sample(inputList, sampleSize)

def copyFiles(inputFilesList, destinationFolder):
    for file in inputFilesList:
        shutil.copy2(file, destinationFolder)

def main():
    path = r"C:\HY-Data\HENTENKA\Python\MassaAjoNiputus\MetropAccess-matka-aikamatriisi_Ajot_2014_04\MetropAccess-matka-aikamatriisi_TOTAL_FixedInternalCells"
    sampleFolder = r"C:\HY-Data\HENTENKA\Python\MassaAjoNiputus\MetropAccess-matka-aikamatriisi_Ajot_2014_04\QualityCheck"
    files = listFiles(path)

    #randFiles = selectRandom(files, 600)
    selectedFiles = selectQuery(files, [5894644,5970404])

    print selectedFiles
    #copyFiles(randFiles, sampleFolder)

if __name__ == '__main__':
    main()
