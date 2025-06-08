from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
import os
from sophie_fortune import get_fortune_result, get_magic_phrase

app = Flask(__name__)

# 環境変数または直接埋め込み（セキュリティのため本番は環境変数推奨）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "<YOUR_CHANNEL_ACCESS_TOKEN>")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "<YOUR_CHANNEL_SECRET>")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ユーザーごとの状態を記録（簡易実装）
user_state = {}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"[Webhook ERROR]: {e}")
        return 'Error', 200  # 開発時は200返してWebhook確認成功させる

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    if text == "占いして":
        user_state[user_id] = {}
        zodiac_options = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=z, text=z))
            for z in ["おひつじ座", "おうし座", "ふたご座", "かに座", "しし座", "おとめ座",
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
            QuickReplyButton(action=MessageAction(label=b, text=b))
            for b in ["A型", "B型", "O型", "AB型"]
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
            magic = get_magic_phrase()
            reply = f"🔮 {zodiac} × {blood} の運勢 🔮\n{result}\n\n💫 今日の魔法のひとこと 💫\n{magic}"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
            user_state[user_id] = {}  # 状態リセット
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「占いして」と送ってくれたら、今日の運勢を占いますよ🔮")
        )
