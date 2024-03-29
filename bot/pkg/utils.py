#from scraper import GoldNewsRetriever
import argparse
from exceptions import RegisterModeException
from settings import PERMITTED_REGISTER_MODE


parser = argparse.ArgumentParser()

parser.add_argument("--scraper", type=str,
                    help="scrape old news data or current breaking news")

parser.add_argument("--register_mode", type=str,
                    help="load in db or in local/mount file system")

parser.add_argument("--pagination_low", type=int,
                    help="historical news pagination on investing.com low")

parser.add_argument("--pagination_up", type=int,
                    help="historical news pagination on investing.com up")

args = parser.parse_args()

register_mode = args.register_mode
scraper = args.scraper
pagination_low = args.pagination_low
pagination_up = args.pagination_up

if register_mode not in PERMITTED_REGISTER_MODE:
    raise RegisterModeException(register_mode)

if register_mode == "api":
    from apis import api_call
    api_call(scraper=scraper, pagination=pagination)

elif register_mode == "fs":
    from register import Register
    instance = Register(scraper=scraper, pagination_low=pagination_low, pagination_up=pagination_up)
    instance.register()

# api 
#python pkg/utils.py --scraper current --register_mode api 
#python pkg/utils.py --scraper back --register_mode api --pagination 4

# fs
#python bot/pkg/utils.py --scraper current --register_mode fs
#python pkg/utils.py --scraper back --register_mode fs --pagination 4


