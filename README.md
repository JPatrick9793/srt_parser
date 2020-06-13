# srt_parser
Modify the timestamps on .SRT extension subtitle files to better line up with a movie

# Installation
- None! this is totally python 3.6+ native. No additional packages required.

# How to Use?
- make sure you have python 3.6 installed and available on your path
- clone/download this repo
- The script takes the following arguments:
    - inFile: path to the input file
    - milliseconds: Number of milliseconds to add to the file timestamps (negative numbers will subtract time).
    - outFile: (optional) path to the new output file. 
        If not specified, will default to the input file name with "Copy" appended to the name.
    - suffix: (optional) will add a suffix before the file extension 
        (e.g. if the outFIle is *someFile.txt* and suffix="en", then the new file would be *someFile.en.txt*)
- cd into this directory, and run the following command:
    - `python main --inFile <inFile> --milliseconds <milliseconds> [--outFile <outFile>] [--suffix <suffix>]`
    - Replace the angle-brackets with your information.
    - Square brackets are optional input parameters.
    
    
    
    
