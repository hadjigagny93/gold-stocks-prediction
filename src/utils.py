from scraper import GoldNewsRetriever
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--scraper", type=str,
                    help="scrape old news data or current breaking news")

parser.add_argument("--register_mode", type=str,
                    help="load in db or in local/mount file system")
args = parser.parse_args()

register_mode = args.register_mode
scraper_instance = GoldNewsRetriever(register_mode=register_mode)
if args.scraper == "back":
    print("import back_scraper func")
    scraper_instance.back_scrape(1)

if args.scraper == "current":
    print("import scraper func")
    scraper_instance.scrape()
