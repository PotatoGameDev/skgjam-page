# SKG Community Jam Web Page

Simple page for the SKG Community Jam.

## Data Preparation
In src/_data there is a python script that scrapes itch.io for all the data.
Initialize venv:

```bash
cd src/_data
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run:
```bash
python3 data-collector.py -j 12345 -o ./skgjam202Xentries.json
```
Obviously substitute 12345 and X with something.
the -j param you can scrape from the source of the jam page.
It's basically the internal itch.io jam id.

The file name will be the name of data variable in eleventy.
It will contain the entry details and the scores for all the entries.




