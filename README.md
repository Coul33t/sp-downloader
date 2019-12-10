# sp-downloader

## Requirements 
Install all the required modules with `pip install -r requirements.txt`. 

### Standard modules: 
* requests (getting the pages)
* os (deleting non-finished downloads)
* json (listing already downloaded episode)
* re (used to name the file)

### External modules:
* Beautiful Soup (HTML processing, finding desired informations)
* clint (Progress bar yay)

## Usage
`py spdownloader.py`

The episodes are named as follows: `[DOWNLOAD NUMBER] - S[XX]E[YY] - [NAME OF THE EPISODE]`, so that it's easier to sort them afterwards. I added the download number first, because files are sorted as strings, not numbers, *i.e.* `1, 10, 11, 12, 13, 2, 20, 21, 3, 4, 5, 6, 7, 8, 9` on the OS. The script also save which episodes were fully downloaded, so that you can resume the downloads another time.
