import os
import sys
from time import sleep
import re


####################################
########## Audacity stuff ##########
####################################
audacityCommandAcceptorPath = ""
audacityResponsePath = ""
lineDelimiter = ""
dirDelimiter = ""

# set paths respective to OS variant
if sys.platform == 'win32':
    audacityCommandAcceptorPath = "\\\\.\\pipe\\ToSrvPipe"
    audacityResponsePath = "\\\\.\\pipe\\FromSrvPipe"
    lineDelimiter = "\r\n\0"
    dirDelimiter = "\\"
else:
    audacityCommandAcceptorPath = "/tmp/audacity_script_pipe.to." + str(os.getuid())
    audacityResponsePath = "/tmp/audacity_script_pipe.from." + str(os.getuid())
    lineDelimiter = "\n"
    dirDelimiter = "/"

print("=== Connecting to Audacity ... ===")

if not os.path.exists(audacityCommandAcceptorPath):
    print("Error connecting to Audacity: Pipe not found. Is Audacity running and scripting enabled?")
    sys.exit()

# Apparent race condition in Audacity -> Sleep to ensure Audacity is available for next command
sleep(.1)

if not os.path.exists(audacityResponsePath):
    print("Error connecting to Audacity: Pipe not found. Is Audacity running and scripting enabled?")
    sys.exit()

# Apparent race condition in Audacity -> Sleep to ensure Audacity is available for next command
sleep(.1)

audacityCommandAcceptor = open(audacityCommandAcceptorPath, 'w')

# Apparent race condition in Audacity -> Sleep to ensure Audacity is available for next command
sleep(.1)

audacityResponder = open(audacityResponsePath, 'rt')

print("=== Connection to Audacity established ===")


def sendCommand(command):
    audacityCommandAcceptor.write(command + lineDelimiter)
    audacityCommandAcceptor.flush()


def readResponse():
    response = ''
    line = ''
    while line != '\n' and len(response) == 0:
        response += line
        line = audacityResponder.readline()
    return response


def executeCommand(command, printResponse=False):
    sendCommand(command)
    response = readResponse()
    if (printResponse):
        print("AudacityResponse: " + response)
    return response


###################################
########## Cutting stuff ##########
###################################

# === input file stuff ===
inputFileName = "input.mp3"
inputFileDir = os.path.abspath(os.getcwd())
inputFilePath = inputFileDir + dirDelimiter + inputFileName

# === output file stuff ===
outputPrefix = "output-"
outputFolderName = "output"
outputFolderDir = os.path.abspath(os.getcwd())
outputFolderPath = outputFolderDir + dirDelimiter + outputFolderName + dirDelimiter

# === part stuff file stuff ===
partLength = 10 * 60
minPartLength = 5 * 60

remainingLength = 0
partNumber = 1


# === driver code ===
def sendCuttingCommands():
    global inputFilePath

    global outputPrefix
    global outputFolderPath

    global partLength
    global minPartLength

    global remainingLength
    global partNumber

    # open
    executeCommand('OpenProject2: Filename="' + inputFilePath + '"')

    # get track length
    response = executeCommand('GetInfo: Type=Tracks')
    for part in re.split(' |,', response):
        parts = part.split(":")
        if parts[0] == "\"end\"":
            remainingLength = float(parts[1])

    # check output dir
    if not os.path.isdir(outputFolderPath):
        os.makedirs(outputFolderPath)

    # split track
    while remainingLength > 0:
        if remainingLength - partLength > minPartLength:
            executeCommand('SelectTime: Start=' + str((partNumber-1) * partLength) + ' End=' + str(partNumber*partLength))
            remainingLength -= partLength
        else:
            executeCommand('SelectTime: Start=' + str((partNumber-1)*partLength) + ' End=' + str((partNumber-1)*partLength+remainingLength))
            remainingLength = 0

        executeCommand('Export2: Filename="' + outputFolderDir + outputPrefix + ("0" if partNumber < 10 else "") + str(partNumber) + '.mp3"')
        partNumber += 1

    # close on finish
    executeCommand('TrackClose:')
    executeCommand('Close:')


# === main program ===
# parse arguments
for arg in sys.argv:
    parts = arg.split("=")
    match parts[0]:
        case "input":
            inputFileName = parts[1]
            inputFilePath = inputFileDir + dirDelimiter + inputFileName
        case "inputFilePath":
            inputFilePath = parts[1]
        case "outputPrefix":
            outputPrefix = parts[1]
        case "outputDirectoryName":
            outputFolderName = parts[1]
            outputFolderPath = outputFolderDir + dirDelimiter + outputFolderName + dirDelimiter
        case "outputDirectoryPath":
            outputFolderPath = parts[1]
        case "partLength":
            partLength = int(parts[1])
        case "minPartLength":
            minPartLength = int(parts[1])
        case _:
            print("Error reading arguments: Argument unknown: " + parts[0])
            sys.exit()


# run cutting code
sendCuttingCommands()
