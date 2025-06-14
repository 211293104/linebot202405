from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)
from sophie_fortune import get_fortune_data, generate_fortune_message
import traceback
from datetime import datetime
import pytz

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

zodiac_list = [
    "おひつじ座", "おうし座", "ふたご座", "かに座", "しし座",
    "おとめ座", "てんびん座", "さそり座", "いて座", "やぎ座",
    "みずがめ座", "うお座"
]

blood_list = ["A型", "B型", "O型", "AB型"]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("⚠ Webhook処理エラー:", e)
        traceback.print_exc()

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        text = event.message.text
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        print(f"📩 受信内容 [{now.strftime('%Y-%m-%d %H:%M:%S')}]: {text}")

        if any(z in text for z in zodiac_list) and any(b in text for b in blood_list):
            try:
                zodiac, blood = text.split()
            except ValueError:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="⚠ 星座と血液型を半角スペースで区切って送ってください\n例：てんびん座 AB型")
                )
                return

            data = get_fortune_data(zodiac, blood)
            if not data:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="⚠ 入力が一致しませんでした。再度選び直してください。")
                )
                return

            message = generate_fortune_message(
                zodiac=zodiac,
                blood_type=blood,
                rank=data["rank"],
                total=data["total"],
                luck_scores=data["luck_scores"],
                lucky_color=data["lucky_color"],
                lucky_item=data["lucky_item"],
                magic_phrase=data["magic_phrase"]
            )

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
            return

        elif text in zodiac_list:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=blood, text=f"{text} {blood}")) for blood in blood_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🩸 あなたの血液型を選んでください", quick_reply=quick_reply)
            )
            return

        elif text in blood_list:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=f"{zodiac} {text}")) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🌟 星座を選び直してください", quick_reply=quick_reply)
            )
            return

        elif "占い" in text:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac)) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🔮 星座を選んでください", quick_reply=quick_reply)
            )
            return

        else:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac)) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🌟 星座からスタートしましょう", quick_reply=quick_reply)
            )
            return

    except Exception as e:
        print("❌ メッセージ処理エラー:", e)
        traceback.print_exc()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="エラーが発生しました💦 もう一度お試しください")
        )
