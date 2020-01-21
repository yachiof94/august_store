from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('G+23J7JMI1rd5XxYPVt5adGqo+cR0Zmir53gBgpWGkOYB/qj2lflMh3M6rVH63eOycxjx1FafE6EwLf9l8A8qkSh2wZHC5kNsntnTEJr52QxSHdfs97uaA9LVLwbE3rBD6dqXOCP80bbfREppv86sQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('290d700975697bb22122d423c7aeaef5')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
