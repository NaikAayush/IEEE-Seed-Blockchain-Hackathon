import pprint
import time
import sys
import os
import urllib3
import requests
import sql
import blockchain
from dotenv import load_dotenv
load_dotenv()

BOT_TAG = "@seed_chain_bot"
TOKEN = os.getenv("TOKEN")
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

# configuration here
HELP_TEXT = """Welcome to Seed Chain Bot, send a tag number to get
              seed information"""
# when keys are matched, the corresponding value is sent
# message_responses = {
#         "who are you?": "Kono Dio Da!",
#         "who are you": "Kono Dio Da!",
#         "what are you?": "Kono Dio Da!",
#         "what are you": "Kono Dio Da!",
#         "hi": "_Oh, you're approaching me?_",
#         "help": HELP_TEXT,
#         "help?": HELP_TEXT,
#         "/help": HELP_TEXT,
#         "/?": HELP_TEXT,
#         "?": HELP_TEXT
#         }

# default message when nothing is matched
default_message = "Please send a tag number to get seed information"

# set up requests
sess = requests.Session()
retries = urllib3.util.retry.Retry(total=10,
                                   backoff_factor=0.1,
                                   status_forcelist=[500, 502, 503, 504])
sess.mount("https://", requests.adapters.HTTPAdapter(max_retries=retries))

def send_message(text, chat_id):
    """Sends `text` to chat `chat_id`
    """
    url = "{}/sendMessage".format(BASE_URL)
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = sess.get(url=url, params=params)
    if response.status_code != requests.codes.ok: # pylint: disable=no-member
        print("*"*20, "ERROR", "*"*20)
        pprint.pprint(response.json())
        print("*"*45)
    else:
        print(f"Sent message to chat_id {chat_id}, replying with '{text}'")

update_url = "{}/getUpdates".format(BASE_URL)
# headers = {'Prefer': 'wait=120'}

print("Listening...")

def main():
    """Main method to handle everything"""
    # to store ID of the last update processed
    LAST_UPDATE_FILE = "last_id.txt"
    with open(LAST_UPDATE_FILE, "rt") as f:
        last_update = int(f.read()) + 1

    while True:
        print(".", end="")
        sys.stdout.flush()
        update_params = {"offset": last_update, "timeout": 5}
        # headers = {'Prefer': 'wait=120'}
        headers = {}
        response = sess.get(
            url=update_url, params=update_params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            for update in data["result"]:
                if "message" in update and \
                        "text" in update["message"] and \
                        not update["message"]["from"]["is_bot"] and \
                        "reply_to_message" not in update["message"]:
                    text = update["message"]["text"].lower()
                    text = text.replace(BOT_TAG, "")
                    print(f"\nGot message '{text}'"
                          f"from chat_id {update['message']['chat']['id']}")

                    try:
                        uuid = sql.returnUUIDtag(text)
                        print(uuid)
                    except Exception as e:
                        print(e)
                        uuid = None
                    if not uuid:
                        send_message("Could not find seed with that ID. Please try again",
                                     update['message']['chat']['id'])
                    else:
                        seed_data_a = blockchain.getHistory(uuid)
                        print(seed_data_a)
                        send_message(str(seed_data_a), update['message']['chat']['id'])

                with open(LAST_UPDATE_FILE, "wt") as f:
                    last_update = update["update_id"] + 1
                    f.write(str(last_update))

        elif response.status_code != 304:
            time.sleep(60)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
