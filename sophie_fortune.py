from datetime import datetime
from linebot.models import FlexSendMessage
from fortune_assets import lucky_colors, lucky_items, magic_phrases
import random
import hashlib

zodiac_signs = [
    "おひつじ座", "おうし座", "ふたご座", "かに座", "しし座",
    "おとめ座", "てんびん座", "さそり座", "いて座", "やぎ座",
    "みずがめ座", "うお座"
]

blood_types = ["A型", "B型", "O型", "AB型"]

def generate_seed(date_str):
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16) % (10 ** 8)

def generate_fortune_ranking(date_str):
    seed = generate_seed(date_str)
    random.seed(seed)
    results = []
    for sign in zodiac_signs:
        for blood in blood_types:
            money = random.randint(1, 5)
            work = random.randint(1, 5)
            love = random.randint(1, 5)
            total = money + work + love
            results.append({
                "sign": sign,
                "blood": blood,
                "money": money,
                "work": work,
                "love": love,
                "total": total,
                "lucky_color": random.choice(lucky_colors),
                "lucky_item": random.choice(lucky_items),
                "magic_phrase": random.choice(magic_phrases)
            })
    results.sort(key=lambda x: x["total"], reverse=True)
    for idx, item in enumerate(results, 1):
        item["rank"] = idx
    return results

def get_fortune_data(zodiac, blood_type):
    today = datetime.now().strftime('%Y-%m-%d')
    data_list = generate_fortune_ranking(today)
    for item in data_list:
        if item["sign"] == zodiac and item["blood"] == blood_type:
            return {
                "rank": item["rank"],
                "total": item["total"],
                "luck_scores": {
                    "money": item["money"],
                    "work": item["work"],
                    "love": item["love"]
                },
                "lucky_color": item["lucky_color"],
                "lucky_item": item["lucky_item"],
                "magic_phrase": item["magic_phrase"]
            }
    return {}

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
