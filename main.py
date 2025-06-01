import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime
from sophie_fortune import generate_fortune_ranking
from flex_message import create_flex_message

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 星座：漢字・ひらがな対応
zodiac_signs_map = {
    "牡羊座": ["牡羊座", "おひつじ座"],
    "牡牛座": ["牡牛座", "おうし座"],
    "双子座": ["双子座", "ふたご座"],
    "蟹座": ["蟹座", "かに座"],
    "獅子座": ["獅子座", "しし座"],
    "乙女座": ["乙女座", "おとめ座"],
    "天秤座": ["天秤座", "てんびん座"],
    "蠍座": ["蠍座", "さそり座"],
    "射手座": ["射手座", "いて座"],
    "山羊座": ["山羊座", "やぎ座"],
    "水瓶座": ["水瓶座", "みずがめ座"],
    "魚座": ["魚座", "うお座"]
}
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

    # 挨拶・ヘルプ系はLINE側で処理するのでスキップ
    if user_message.lower() in ["こんにちは", "はじめまして", "help", "ヘルプ"]:
        return  # 挨拶・ヘルプはBot側で返信しない

    found_zodiac = None
    for key, aliases in zodiac_signs_map.items():
        if any(alias in user_message for alias in aliases):
            found_zodiac = key
            break

    found_blood = next((b for b in blood_types if b in user_message), None)

    if not found_zodiac or not found_blood:
        reply_text = "🌟 星座と血液型を含めたメッセージを送ってください！\n例: 牡羊座のA型の運勢を教えて"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        return

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
        reply_text = "データが見つかりませんでした、もう一度試してください。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

  
