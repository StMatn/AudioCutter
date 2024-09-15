# AudioCutter
Tool for cutting long audio files into short mp3-files.

## Notes
* Audacity must be running before executing the script.
* Audacity may crash on close after the script is executed.

## Usage
Providing no arguments will print the help text.

Provide arguments in the format <argument>=<value>. You can provide multiple arguments separated by spaces.

Argument | Description | Default value
-------- | ----------- | -------------
default | Run program with default settings. Ommit "=<value>". | n/a
input | Specify input file from current working directory | input.mp3
inputFilePath | Specify absolute location of input file. | <working directory> + <input>
outputPrefix | Pfefix of output files. Two-digit running number is added to parts. | output-
outputDirectoryName | Name of directory for output files. Directory will be created in current working directory. | output
outputDirectoryPath | Specify absolute path of directory for output files. No subdirectory will be created! | <working directory> + <outputDirectoryName>
partLength | Length of regular parts in seconds. | 600 (=10 minutes)
minPartLength | Minimal length of final part in seconds. If the final part would be shorter, it will be included in the part before. | Default value: 300 (= 5 minutes)
