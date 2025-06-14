from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)
from sophie_fortune import get_fortune_data, generate_fortune_message
import os
import traceback
from datetime import datetime
import pytz

# ✅ 環境変数から安全に読み込む
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

app = Flask(__name__)

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
        print("⚠ Webhook処理中のエラー:", e)
        traceback.print_exc()

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        text = event.message.text.strip()
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        print(f"📩 [{now.strftime('%Y-%m-%d %H:%M:%S')}] ユーザー入力: {text}")

        if any(z in text for z in zodiac_list) and any(b in text for b in blood_list):
            try:
                zodiac, blood = text.split()
            except ValueError:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="⚠ 星座と血液型の間は半角スペースで区切ってね！\n例：やぎ座 AB型")
                )
                return

            data = get_fortune_data(zodiac, blood)
            if not data:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="⚠ データが見つかりませんでした。もう一度選んでね")
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
                TextSendMessage(text="🩸 血液型を教えてください", quick_reply=quick_reply)
            )
            return

        elif text in blood_list:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=f"{zodiac} {text}")) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🌟 星座を選び直してね", quick_reply=quick_reply)
            )
            return

        elif "占い" in text or text == "占いして":
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac)) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🔮 占いたい星座を教えてください", quick_reply=quick_reply)
            )
            return

        else:
            quick_reply = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=zodiac, text=zodiac)) for zodiac in zodiac_list
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🌠 星座から始めてください", quick_reply=quick_reply)
            )

    except Exception as e:
        print("❌ メッセージ処理エラー:", e)
        traceback.print_exc()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="エラーが出ちゃいました💦 もう一度試してね")
        )
