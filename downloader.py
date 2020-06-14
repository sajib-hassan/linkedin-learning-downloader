import json
import logging
import os
import sys

from loging_in import login
from fetch_info import fetch_courses


def check_required_info():
    required_info_path = os.path.join(os.path.dirname(__file__), 'required_info.json')
    if os.path.isfile(required_info_path) and os.access(required_info_path, os.R_OK):
        with open(required_info_path) as f:
            return json.loads(f.read())
    else:
        caching = {'linkedin_email': '', 'linkedin_password': '', 'courses_links': ["", ""]}
        with open(required_info_path, 'w') as f:
            f.write(json.dumps(caching))
        logging.error("Please copy the required_info.json.sample to required_info.json "
                      "and then fill in your info to required_info.json")
        return False


def process():
    try:
        caching = check_required_info()
        if caching:
            logging.info("[*] -------------Login-------------")
            USERNAME, PASSWORD = caching['linkedin_email'], caching['linkedin_password']
            if not USERNAME or not PASSWORD:
                logging.error("please open the required_info.json and fill in your info ")
            else:
                session = login(USERNAME, PASSWORD)
                logging.info("[*] -------------Done-------------")
                logging.info("[*] -------------Fetching Course-------------")
                fetch_courses(session, caching['courses_links'])
                logging.info("[*] -------------Done-------------")

    except Exception as e:
        logging.error(f"Connection Error: {e}")


if __name__ == "__main__":
    if sys.version_info[0] != 3:
        logging.error("This script requires Python 3")
        exit()
    process()
