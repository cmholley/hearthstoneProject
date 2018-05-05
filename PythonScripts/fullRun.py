import generateCards
import processGames
import generateGraph
import winRates
import writeCardsCsv
import writeWeightsCsv
import time


printFilesBool = False

def printFiles():
    writeCardsCsv.start()
    writeWeightsCsv.start()

if __name__ == '__main__':
    start = time.time()

    generateCards.start()
    processGames.start()
    generateGraph.start()
    winRates.start()

    if printFilesBool:
        printFiles()

    end = time.time()
    print "Finished full run in ", (end - start), " seconds"
