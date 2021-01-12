#from scraper import GoldNewsRetriever
import argparse
from exceptions import RegisterModeException
from settings import PERMITTED_REGISTER_MODE


parser = argparse.ArgumentParser()

parser.add_argument("--scraper", type=str,
                    help="scrape old news data or current breaking news")

parser.add_argument("--register_mode", type=str,
                    help="load in db or in local/mount file system")

parser.add_argument("--pagination", type=int,
                    help="historical news pagination on investing.com")

args = parser.parse_args()

register_mode = args.register_mode
scraper = args.scraper
pagination = args.pagination

#scraper_instance = GoldNewsRetriever(register_mode=register_mode)
#if args.scraper == "back":
#    page = args.pagination
#    scraper_instance.back_scrape(pagination=page)
#if args.scraper == "current":
#    scraper_instance.scrape()
#print(register_mode, scraper, pagination)

if register_mode not in PERMITTED_REGISTER_MODE:
    raise RegisterModeException(register_mode)

if register_mode == "api":
    from apis import api_call
    api_call(scraper=scraper, pagination=pagination)

elif register_mode == "fs":
    from register import Register
    instance = Register(scraper=scraper, pagination=pagination)
    instance.register()

#python pkg/utils.py --scraper current --register_mode api 
#python pkg/utils.py --scraper back --register_mode api --pagination 4
#python pkg/utils.py --scraper back --register_mode fs --pagination 2


