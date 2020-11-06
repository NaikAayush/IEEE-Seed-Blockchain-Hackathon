from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sql
import blockchain
import pprint

app = Flask(__name__)

account_sid = # twilio account sid here
auth_token = # twilio auth token here
client = Client(account_sid, auth_token)

def get_json():
    try:
        uuid = sql.returnUUIDtag("C7577-4499118")
        print(uuid)
    except Exception as e:
        print(e)
        uuid = None
    if not uuid:
        return "Could not find seed with that ID. Please try again."
    else:
        seed_data_a = blockchain.getHistory(uuid)
        data = pprint.pformat(seed_data_a)
        return data[:1500]


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    # resp.message()
    message = client.messages \
                .create(
                     body=get_json(),
                     from_=# add your twilio number here,
                     to=# add your recipient number here
                 )
    return "success"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5011)
