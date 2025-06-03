import os
import re
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime
import pytz
from sophie_fortune import generate_fortune_ranking
from flex_message import create_flex_message

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

zodiac_signs_map = {
    "牡羊座": ["牡羊座", "おひつじ座", "おひつじ"],
    "牡牛座": ["牡牛座", "おうし座", "おうし"],
    "双子座": ["双子座", "ふたご座", "ふたご"],
    "蟹座": ["蟹座", "かに座", "かに"],
    "獅子座": ["獅子座", "しし座", "しし"],
    "乙女座": ["乙女座", "おとめ座", "おとめ"],
    "天秤座": ["天秤座", "てんびん座", "てんびん"],
    "蠍座": ["蠍座", "さそり座", "さそり"],
    "射手座": ["射手座", "いて座", "いて"],
    "山羊座": ["山羊座", "やぎ座", "やぎ"],
    "水瓶座": ["水瓶座", "みずがめ座", "みずがめ"],
    "魚座": ["魚座", "うお座", "うお"]
}

blood_types = ["AB型", "A型", "B型", "O型"]

cheer_messages = [
    "笑顔は世界を変える魔法だよ！",
    "深呼吸して、また一歩進もう。",
    "今日も頑張ってるね、ソフィーは知ってるよ✨",
    "無理しすぎないで、自分を大事にしてね🌸",
    "きっとうまくいくよ、信じてみて！",
    "小さな一歩でも、それは前進だよ💖"
]

def normalize_input(text):
    text = text.strip().lower()
    text = re.sub(r'[\\s\u3000]', '', text)

    # 星座の変換（表記ゆれ対応）
    text = text.replace('ざ', '座')
    text = text.replace('おひつじ', '牡羊')
    text = text.replace('おうし', '牡牛')
    text = text.replace('ふたご', '双子')
    text = text.replace('かに', '蟹')
    text = text.replace('しし', '獅子')
    text = text.replace('おとめ', '乙女')
    text = text.replace('てんびん', '天秤')
    text = text.replace('さそり', '蠍')
    text = text.replace('いて', '射手')
    text = text.replace('やぎ', '山羊')
    text = text.replace('みずがめ', '水瓶')
    text = text.replace('うお', '魚')

    # 血液型の変換（全角・小文字・平仮名対応）
    # AB型の正規化は先にやること！
   text = text.replace('ａｂ', 'AB')
   text = text.replace('ab型', 'AB型')
   text = text.replace('ＡＢ', 'AB')

   # そのあとに個別文字を置き換え
   text = text.replace('ａ', 'A').replace('ｂ', 'B').replace('ｏ', 'O')
   text = text.replace('a型', 'A型').replace('b型', 'B型').replace('o型', 'O型')
   text = text.replace('Ａ', 'A').replace('Ｂ', 'B').replace('Ｏ', 'O')
   text = text.replace('えー', 'A').replace('びー', 'B').replace('おー', 'O').replace('えーびー', 'AB')
    return text
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
    user_message = normalize_input(event.message.text)
    print(f"[DEBUG] User message after normalization: {user_message}")

    if "元気" in user_message or "励まし" in user_message:
        reply_text = random.choice(cheer_messages)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        return

    found_zodiac = next((key for key, aliases in zodiac_signs_map.items() if any(alias in user_message for alias in aliases)), None)
    found_blood = next((b for b in blood_types if b in user_message), None)

    print(f"[DEBUG] Found zodiac: {found_zodiac}, Found blood: {found_blood}")

    if not found_zodiac or not found_blood:
        reply_text = "🌸 星座と血液型を含めたメッセージを送ってください！\n例: 牡羊座のA型の運勢を教えて"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        return

    jst = pytz.timezone('Asia/Tokyo')
    today_str = datetime.now(jst).strftime("%Y-%m-%d")
    print(f"[DEBUG] Using date string: {today_str}")

    ranking_list = generate_fortune_ranking(today_str)
    print(f"[DEBUG] First few rankings: {ranking_list[:3]}")
    matched = next((
    item for item in ranking_list
    if item['sign'].strip() == found_zodiac and item['blood'].strip() == found_blood
    ), None)
    print(f"[DEBUG] Matched fortune result: {matched}")

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
