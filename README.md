# WhoSampled Submission Checker

A simple script to validate sample submission pages for user profiles 
on the website [WhoSampled](https://www.whosampled.com/).

## Background
The website WhoSampled is a user-submitted database of music samples. Each 
public user profile page on WhoSampled can contain 0 or more pages of samples 
submitted by this user. Each individual page usually contains two YouTube 
videos: one for the song that uses the sample and another for the originating 
song where the sample came from. However, it is also
possible for these videos to either be broken (the video got deleted or 
made private) or to be replaced with other widgets from music services 
(SoundCloud, Bandcamp, Spotify, etc.).

## About
This program scans user profile pages on WhoSampled for sample submission 
entries, then parses each individual sample submission page for broken YouTube 
video embeds. Either of the following conditions will qualify a page as having 
broken embeds:

- At least one of the YouTube videos embeds on the page is missing
- At least one YouTube embed has been replaced with a widget from another audio 
- streaming service (described above)

The second condition might need to be accounted for separately in a future 
release of this script as it doesn't necessarily mean the page has broken 
embeds. Just because the embeds aren't
from YouTube doesn't mean they won't work, even if the timestamps above the 
non-existent video remain broken.

The output from the program is a list of WhoSampled submission pages which have 
broken embeds.

The script currently understands and processes the following command line 
arguments and options:

- **-u** -> Stands for user. The name of a user whose profile will be parsed by 
the script. Providing this argument scripts the user prompt at the beginning 
of the script.
- **--file-output** -> Option to specify whether to output the links to pages 
with broken embeds in a file. The default is output of the links to the 
terminal.

## Installation
All script requirements are listed in the included requirements.txt file in 
the repo. However, the undetected-chromedriver package currently needs a fix 
described [here](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955#issuecomment-2223076821) to work correctly with Python 3.12. This issue can be 
avoided by using Python 3.11 instead.

After the requirements are satisfied in a global or virtual environment simply 
run the script and follow the prompts.
