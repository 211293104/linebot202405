import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from datetime import datetime
from sophie_fortune import generate_fortune_ranking
from flex_message import create_flex_message

# LINE Bot API設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 星座・血液型リスト
zodiac_signs = [
    "牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座",
    "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"
]
# 血液型は長い順に並べる
blood_types = ["AB型", "A型", "B型", "O型"]

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

    # 星座と血液型を文章から探す
    found_zodiac = next((z for z in zodiac_signs if z in user_message), None)
    found_blood = next((b for b in blood_types if b in user_message), None)

    if not found_zodiac or not found_blood:
        reply_text = "🌸 星座と血液型を含めたメッセージを送ってください！\n例: 牡羊座のA型の運勢を教えて"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        return

    # 今日のランキングを取得
    today_str = datetime.now().strftime("%Y-%m-%d")
    ranking_list = generate_fortune_ranking(today_str)

    matched = next((item for item in ranking_list if item['sign'] == found_zodiac and item['blood'] == found_blood), None)

    if matched:
        flex_message = create_flex_message(matched)
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )
    else:
        reply_text = "データが見つかりませんでした。もう一度試してください。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

if __name__ == "__main__":
    app.run()
