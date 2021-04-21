## Instagram_Media_Downloader
- Download all photos and videos from your friend's or favorite celebrity"s Instagram page with ease
- Username and Password not needed

## Requirements
- Python 3.x
- Requests
- Colorama
- Termcolor

## Installation
1. Download and install the latest Python 3.x version from the official Python website or [here](https://www.python.org/downloads/) and to make sure to tick **"Add Python 3.x to PATH"** checkbox when installing
2. Install all the requirements by opening a command prompt terminal from the folder in which the requirements.txt file is located and run `pip intall -r requirements.txt` or installing each requirement by running `pip install ******`
3. Add the folder where the program is located to PATH directory so that you can call the program in a short and neat way. [Click here](https://docs.alfresco.com/4.2/tasks/fot-addpath.html) to know how to add folder to PATH

## Usage
`py instagram_media_downloader.py -u USERNAME -p PATH`

## Help
```
usage: instagram_media_downloader.py [-h] -u USERNAME -p PATH

Download Instagram Images and Videos from a User's Profile Page

optional arguments:
  -h, --help                      show this help message and exit
  -u USERNAME, --user USERNAME    Username on Instagram
  -p PATH, --path PATH            Root path where downloaded Instagram Media is saved
  ```
