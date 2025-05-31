import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from datetime import datetime
from sophie_fortune import generate_fortune_ranking

# LINE Bot API設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    # 今日の日付を取得（YYYY-MM-DD形式）
    today_str = datetime.now().strftime("%Y-%m-%d")
    ranking_list = generate_fortune_ranking(today_str)

    # ユーザー入力（例: 牡羊座A型）とマッチするか確認
    matched = None
    for item in ranking_list:
        if f"{item['sign']}{item['blood']}" == user_message:
            matched = item
            break

    if matched:
        reply_text = (
            f"🌟 今日の運勢 🌟\n"
            f"{matched['sign']} {matched['blood']}\n"
            f"総合順位: {matched['rank']}/48\n"
            f"💰 金運: {matched['money']}/5\n"
            f"💼 仕事運: {matched['work']}/5\n"
            f"💖 恋愛運: {matched['love']}/5\n"
            f"✨ ラッキーアクション: {matched['lucky_action']}"
        )
    else:
        reply_text = (
            "星座と血液型を続けて送ってください（例: 牡羊座A型）\n"
            "対応する運勢をお知らせします！"
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()

