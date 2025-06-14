from linebot.models import FlexSendMessage

def generate_fortune_flex_message(zodiac, blood_type, rank, total, luck_scores, lucky_color, lucky_item, magic_phrase):
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FDEEF4",
            "contents": [
                {
                    "type": "text",
                    "text": "🌸 ソフィーの今日の占い 🌸",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#C71585"
                },
                {
                    "type": "text",
                    "text": f"{zodiac} × {blood_type}\n総合順位：{rank}位 / 48",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"💰 金運：{luck_scores['money']}/5\n📁 仕事運：{luck_scores['work']}/5\n❤️ 恋愛運：{luck_scores['love']}/5",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"🎀 ラッキーカラー：{lucky_color}\n🎁 ラッキーアイテム：{lucky_item}",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "✨ 今日の魔法の一言 ✨",
                    "align": "center",
                    "color": "#8B008B",
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": magic_phrase,
                    "align": "center",
                    "wrap": True,
                    "margin": "sm"
                }
            ]
        }
    }

    return FlexSendMessage(alt_text="今日の占い結果です！", contents=flex_contents)
