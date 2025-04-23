
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    msg = MessagingResponse()
    msg.message("Bot online e funcional.")
    return str(msg)

if __name__ == "__main__":
    app.run(debug=True)
