from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from sophie_fortune import get_fortune_result  # 自作関数として仮定

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# ユーザーごとの状態管理（簡易実装）
user_state = {}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text

    if text == "占いして":
        user_state[user_id] = {}
        zodiac_options = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac))
            for zodiac in ["おひつじ座", "おうし座", "ふたご座", "かに座", "しし座", "おとめ座",
                           "てんびん座", "さそり座", "いて座", "やぎ座", "みずがめ座", "うお座"]
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="あなたの星座を選んでください🌟", quick_reply=zodiac_options)
        )

    elif text in ["おひつじ座", "おうし座", "ふたご座", "かに座", "しし座", "おとめ座",
                  "てんびん座", "さそり座", "いて座", "やぎ座", "みずがめ座", "うお座"]:
        user_state[user_id]["zodiac"] = text
        blood_options = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=blood, text=blood))
            for blood in ["A型", "B型", "O型", "AB型"]
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="血液型を選んでください🩸", quick_reply=blood_options)
        )

    elif text in ["A型", "B型", "O型", "AB型"]:
        if user_id in user_state and "zodiac" in user_state[user_id]:
            zodiac = user_state[user_id]["zodiac"]
            blood = text
            result = get_fortune_result(zodiac, blood)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=result)
            )
            user_state[user_id] = {}  # 状態リセット

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「占いして」と送ってみてくださいね🔮")
        )
