from .scraper import GoldNewsRetriever
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--scraper", type=str,
                    help="scrape old news data or current breaking news")
args = parser.parse_args()

scraper_instance = GoldNewsRetriever()
if args.scraper == "back":
    print("import back_scraper func")
    scraper_instance.back_scrape(1)

if args.scraper == "current":
    print("import scraper func")
    scraper_instance.scrape()
