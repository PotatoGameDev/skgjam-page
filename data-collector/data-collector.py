import json
import os
import requests
import time
import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape itch.io jam results and enrich with the results"
    )
    # Example:
    # https://itch.io/jam/407781/entries.json
    parser.add_argument(
        "-j", "--jam",
        default="407781",
        help="Id of the game jam, you have to manually figure it out by inspecting itch jam page's code for now... Defaults to the original 2025 jam id."
    )
    parser.add_argument(
        "-n", "--output-name",
        default="jam_games_2025",
        help="The output base name"
    )
    return parser.parse_args()

def get_entries(args):
    jam_entries_response = requests.get(f"https://itch.io/jam/{args.jam}/entries.json") 
    jam_entries_response.raise_for_status()

    return jam_entries_response.json()

def get_entry_page(game_url):
    full_url = "https://itch.io/" + game_url

    html_response = requests.get(full_url)
    html_response.raise_for_status()

    return html_response

def save_cover(entry, output_dir):
    # Saving the cover
    cover_url = entry["game"]["cover"]
    if cover_url:
        cover_response = requests.get(cover_url)
        cover_response.raise_for_status()

        _, ext = os.path.splitext(cover_url)

        # writing the entry
        with open(output_dir + "/" + str(entry["id"]) + "_cover" + ext, "wb") as f:
            f.write(cover_response.content)

def main():
    args = parse_args()

    entries = get_entries(args)

    output_dir = "../src/_data/" + args.output_name
    os.makedirs(output_dir, exist_ok=True)

    for entry in tqdm(entries["jam_games"], desc="Downloading jam results"):
        entry_html = get_entry_page(entry["url"])

        # Saving of the covers probably is not a good idea.
        # save_cover(entry, output_dir)

        soup = BeautifulSoup(entry_html.text, "html.parser")

        table = soup.find("table", class_="ranking_results_table")

        rows = table.find_all("tr")

        rows = rows[1:] # removing the header

        scores = {}

        for row in rows:
            cells = row.find_all("td")
            criteria = cells[0].get_text(strip=True)
            rank = cells[1].get_text(strip=True)
            rank_num = int(rank.replace("#", ""))
            score = float(cells[2].get_text(strip=True))
            raw_score = float(cells[3].get_text(strip=True))

            scores[criteria] = {
                    "rank": rank_num,
                    "score": score,
                    "raw_score": raw_score,
            }

        entry["scores"] = scores

        time.sleep(0.5)

    with open(output_dir + "/jam_games.json", "w") as f:
        json.dump(entries, f)


if __name__ == "__main__":
    main()
