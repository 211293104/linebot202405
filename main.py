
import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from sophie_fortune import generate_fortune_message, get_fortune_data
import traceback
from datetime import datetime
import pytz

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print("⚠️ Webhook処理中にエラー:", e)
        traceback.print_exc()
    return 'OK'  # 常に200を返す

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    zodiac_list = ["おひつじ座", "おうし座", "ふたご座", "かに座", "しし座", "おとめ座", "てんびん座", "さそり座", "いて座", "やぎ座", "みずがめ座", "うお座"]
    blood_list = ["A型", "B型", "O型", "AB型"]

    try:
        # 日本時間でのログ出力
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)
        print(f"⏰ 現在の日本時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")

        if any(z in text for z in zodiac_list) and any(b in text for b in blood_list):
            zodiac, blood = text.split()
            data = get_fortune_data(zodiac, blood)
            message = generate_fortune_message(
                zodiac=zodiac,
                blood_type=blood,
                rank=data["rank"],
                total=data["total"],
                luck_scores=data["luck_scores"],
                lucky_color=data["lucky_color"],
                lucky_item=data["lucky_item"]
            )
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

        elif text in zodiac_list:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=blood, text=f"{text} {blood}")) for blood in blood_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="あなたの血液型を教えてください♪", quick_reply=quick_reply)
            )

        elif "占い" in text:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac)) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="こんにちは！まずはあなたの星座を選んでください🌟", quick_reply=quick_reply)
            )

        else:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac)) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="まずはあなたの星座を選んでください🌟", quick_reply=quick_reply)
            )

    except Exception as e:
        print("⚠️ メッセージ処理中にエラー:", e)
        traceback.print_exc()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="エラーが発生しちゃいました💦 もう一度試してみてね！")
        )
