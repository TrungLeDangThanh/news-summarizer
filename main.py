from dotenv import find_dotenv, load_dotenv
from os import environ
from time import sleep
import requests
import logging
import json

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    logging.info("'.env' not found. Skipping...")

news_api_key = environ.get("NEWS_API_KEY")


def get_news(topic):
    url = (
        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"  # pageSize determines the number of articles to be received
    )
    news = list()
    sleep_interval = 1

    while True:
        try:
            response = requests.get(url)  # 'response' is now a JSON object
            if response.status_code == 200:
                response = response.json()  # 'response' is now a Python object
                response = json.dumps(response, indent=4)  # 'response is now a JSON formatted string
                response = json.loads(response)  # 'response' is now a Python formatted object, usually dictionary

                status = response["status"]
                articles = response["articles"]
                number = 0

                if status == "ok":
                    for article in articles:
                        source_name = article["source"]["name"]
                        author = article["author"]
                        title = article["title"]
                        description = article["description"]
                        url = article["url"]
                        number += 1
                        layout = f"""
{number}
Title: {title}
Author: {author}
Source: {source_name}
Description: {description}
URL: {url}
"""
                        news.append(layout)
                    
                    logging.info("Response received successfully")
                    return news
                    break  # this 'break' doesn't run because a function ends at 'return'

                else:
                    logging.info("Reponse received but incorrect")
                    break

            logging.info("Waiting for response...")
            sleep(sleep_interval)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred during API request: {e}")
            break
            
topic = input("Enter your topic of interest: ")
news = get_news(topic)
for new in news:
    print(new)
