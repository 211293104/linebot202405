import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

# OpenAIのAPIキーを環境変数から取得
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# LINE Bot APIの設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

# ここに全48通り分のデータを追加してください
ranking_data = {
    "てんびん座AB型": {"rank": 1, "point": 92, "lucky_action": "椅子を1cm高く！"},
    "やぎ座B型": {"rank": 5, "point": 75, "lucky_action": "ハンカチを持ち歩く"},
    # ...他の46通りも同様に
}

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

    # 星座×血液型がマッチしたらランキングを返す
    if user_message in ranking_data:
        data = ranking_data[user_message]
        reply_text = (
            f"{user_message}の今日の運勢は…第{data['rank']}位！\n"
            f"（{data['point']}点／100点）\n"
            f"ラッキーアクション：{data['lucky_action']}"
        )
    else:
        # それ以外はChatGPT APIで回答
        chat_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは優しいAIアシスタントのソフィーです。質問には必ず丁寧な敬語で、パチンコ占いに詳しい設定です。"},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = chat_response.choices[0].message.content

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
