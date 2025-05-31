from linebot.models import FlexSendMessage

def create_flex_message(matched):
    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{matched['sign']} {matched['blood']}",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"総合順位: {matched['rank']}/48",
                    "size": "md",
                    "color": "#888888"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "text", "text": "💰 金運", "flex": 2},
                        {"type": "text", "text": f"{matched['money']}/5", "flex": 1, "align": "end"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "text", "text": "💼 仕事運", "flex": 2},
                        {"type": "text", "text": f"{matched['work']}/5", "flex": 1, "align": "end"}
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "text", "text": "💖 恋愛運", "flex": 2},
                        {"type": "text", "text": f"{matched['love']}/5", "flex": 1, "align": "end"}
                    ]
                },
                {
                    "type": "text",
                    "text": f"✨ ラッキーアクション: {matched['lucky_action']}",
                    "wrap": True,
                    "margin": "md"
                }
            ]
        }
    }
    return FlexSendMessage(alt_text="今日の運勢結果", contents=flex_content)
