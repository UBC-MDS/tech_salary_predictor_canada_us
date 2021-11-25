# author: Khalid Abdilahi
# date: 2021-11-18

"""Downloads data csv data from the web to a local filepath as a csv file format.

Usage: src/download_data.py --url=<url> --out_dir=<out_file>

Options:
--url=<url>              URL from where to download the data (must be in standard csv format)
--out_dir=<out_file>     Directory where the extracted file will be saved
"""
  
from docopt import docopt
import zipfile
import requests
from io import BytesIO

opt = docopt(__doc__)

def main(url, out_dir):
    
    try:
        request = requests.get(url)
        request.status_code == 200
        with zipfile.ZipFile(BytesIO(request.content)) as zip_ref:
            zip_ref.extract("survey_results_public.csv", out_dir)
    except Exception as req:
        print("Website at the provided url does not exist.")
        print(req)

if __name__ == "__main__":
    main(opt["--url"], opt["--out_dir"])