#!/usr/bin/python3.6
'''
Takes a path to the directory which contains .wav and correponding
.cha files and creates a directory <datasetDirectory> with .wav files.
The name convention of file is: SUBJECT:START:END.wav
Example: M_1103_20y0m_1:111697:111869.wav
where M_1103_20y0m_1 is the subject, 111697 is the start time of the
clip in milliseconds and 111869 is the end time of the clip in milliseconds.
It also creates a file <labelFileName> which has the wav file name and a label.
Label can be STUTTER or NORMAL
'''
from __future__ import print_function
from pydub import AudioSegment
import sys
import os
import re
import shutil

datasetDirectory = "dataset"
labelFileName = "datasetLabels.txt"

try:
    if not os.path.exists(sys.argv[1]) or not os.path.isdir(sys.argv[1]):
        raise
    audioAndChaFilesDirectory = sys.argv[1]
except:
    sys.exit("Usage: " + sys.argv[0] + " " + "<directory of .wav and .cha files>")


if os.path.exists(datasetDirectory):
    shutil.rmtree(datasetDirectory)
else:
    os.makedirs(datasetDirectory)

labelFile = open(labelFileName, "w")

for chaFileName in os.listdir(audioAndChaFilesDirectory):
    if chaFileName.endswith(".cha"):
        subject = chaFileName.split('.')[0]
        wavFileName = subject + ".wav"

        print("Parsing file: " + chaFileName)

        with open(os.path.join(audioAndChaFilesDirectory, chaFileName), 'r') as chaFile:
            sndFound = False
            phoFound = False
            startTime = -1
            endTime = -1
            label = None
            for line in chaFile:
                if not sndFound:
                    if re.search(r"%snd:", line):
                        lineSplit = line.split("_")
                        startTime = lineSplit[-2]
                        endTime = lineSplit[-1]
                        endTime = re.sub(r"\u0015\n", '', endTime)
                        sndFound = True
                else:
                    if re.search(r"%pho:", line):
                        if re.search(r'[A-Z]', line):
                            label = "STUTTER"
                        else:
                            label = "NORMAL"
                        phoFound = True
                if sndFound and phoFound:
                    audiofilename = subject + ":" + startTime + ":" + endTime + ".wav"
                    labelFile.write(audiofilename + " " + label + "\n")
                    audio = AudioSegment.from_wav(os.path.join(audioAndChaFilesDirectory, wavFileName))
                    audio = audio[(int)(startTime):(int)(endTime)]
                    audio.export(os.path.join(datasetDirectory, audiofilename), format="wav")
                    sndFound = False
                    phoFound = False
                    startTime = -1
                    endTime = -1
                    label = None

labelFile.close()
