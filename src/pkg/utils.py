from scraper import GoldNewsRetriever
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--scraper", type=str,
                    help="scrape old news data or current breaking news")

parser.add_argument("--register_mode", type=str,
                    help="load in db or in local/mount file system")

parser.add_argument("--pagination", type=int,
                    help="historical news pagination on investing.com")

args = parser.parse_args()

register_mode = args.register_mode
scraper_instance = GoldNewsRetriever(register_mode=register_mode)

if args.scraper == "back":
    page = args.pagination
    scraper_instance.back_scrape(pagination=page)

if args.scraper == "current":
    scraper_instance.scrape()
