import io
import re
import zipfile
import requests

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_FILE = "ssa-baby-names.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
}

response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

with zipfile.ZipFile(io.BytesIO(response.content)) as zf, open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("year,name,sex,count\n")
    for filename in sorted(zf.namelist()):
        match = re.fullmatch(r"yob(\d{4})\.txt", filename)
        if not match:
            continue
        year = match.group(1)
        with zf.open(filename) as f:
            for raw_line in f:
                line = raw_line.decode("utf-8").strip()
                if line:
                    out.write(f"{year},{line}\n")
