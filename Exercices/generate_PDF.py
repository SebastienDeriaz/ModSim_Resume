import subprocess
import os
import glob
import argparse
import json

#
# NOTE : Bullet lists in markdown must have an empty line, otherwise they won't be rendered correctly in the .pdf
#



parser = argparse.ArgumentParser(description="Convert exercises to .pdf")
parser.add_argument("--folders", type=str, default=None)
args = parser.parse_args()

folders = args.folders
if folders is None:
    foldersList = os.listdir()
else:
    foldersList = folders.split(',')

modified_dates_file = "files.json"
if os.path.isfile(modified_dates_file):
    with open(modified_dates_file, "r", encoding="utf-8") as f:
        try:
            modified_dates = json.load(f)
        except json.decoder.JSONDecodeError as e:
            modified_dates = {}
else:
    modified_dates = {}
preprocessor_style = "colorful"


for folder in foldersList:
    folder = os.getcwd() + "/" + folder
    
    if(os.path.isdir(folder)):
        os.chdir(folder)
        # Convert notebooks to pdf
        for ex in glob.glob('*SDZ.ipynb'):
            modification = os.path.getmtime(ex) 
            path = os.path.join(folder, ex)
            if(path not in modified_dates or modification != modified_dates[path]):
                print(f"   converting {path}...")
                debug = subprocess.run(['jupyter', 'nbconvert', ex, '--to', 'pdf', '--output', ex.replace('ipynb', 'pdf'), f'--LatexPreprocessor.style={preprocessor_style}'], capture_output=True)
                modified_dates[path] = modification
        # Convert markdowns to pdf
        for ex in glob.glob('*SDZ.md'):
            modification = os.path.getmtime(ex)
            path = os.path.join(folder, ex)
            if(path not in modified_dates or modification != modified_dates[path]):
                print(f"   converting {path}...")
                debug = subprocess.run(['pandoc', ex, '--pdf-engine=xelatex', '-o', ex.replace('md', 'pdf')])
                modified_dates[path] = modification

        os.chdir("..")

with open(modified_dates_file, "w", encoding="utf-8") as f:
    json.dump(modified_dates, f, indent=4)