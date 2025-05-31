from linebot.models import FlexSendMessage

def create_flex_message(matched):
    flex_content = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#ffe6f2",
            "contents": [
                {
                    "type": "text",
                    "text": "🌸 ソフィーの今日の占い 🌸",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#cc3366"
                },
                {
                    "type": "text",
                    "text": f"{matched['sign']} × {matched['blood']}",
                    "size": "md",
                    "align": "center",
                    "color": "#cc3366"
                },
                {
                    "type": "text",
                    "text": f"総合順位: {matched['rank']}位 / 48",
                    "size": "sm",
                    "align": "center",
                    "color": "#996699"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f"💰 金運: {matched['money']}/5",
                    "size": "sm",
                    "color": "#ff6699"
                },
                {
                    "type": "text",
                    "text": f"💼 仕事運: {matched['work']}/5",
                    "size": "sm",
                    "color": "#66cccc"
                },
                {
                    "type": "text",
                    "text": f"💖 恋愛運: {matched['love']}/5",
                    "size": "sm",
                    "color": "#ff99cc"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"✨ 今日の魔法の一言 ✨",
                    "size": "sm",
                    "weight": "bold",
                    "color": "#cc3366",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"{matched['lucky_action']}",
                    "wrap": True,
                    "size": "sm",
                    "color": "#996699"
                }
            ]
        }
    }
    return FlexSendMessage(alt_text="今日の占い結果", contents=flex_content)
