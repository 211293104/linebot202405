import random
from datetime import datetime
from fortune_assets import lucky_colors, lucky_items, magic_phrases

zodiac_signs = [...]
blood_types = [...]

def generate_seed(date_str):
    import hashlib
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

def generate_fortune_message(zodiac, blood_type, rank, total, luck_scores, lucky_color, lucky_item, magic_phrase):
    return f"""🌸 ソフィーの今日の占い 🌸

{zodiac} × {blood_type}
総合順位：{rank}位 / 48

💰 金運：{luck_scores["money"]}/5  
📁 仕事運：{luck_scores["work"]}/5  
❤️ 恋愛運：{luck_scores["love"]}/5  

🎀 ラッキーカラー：{lucky_color}  
🎁 ラッキーアイテム：{lucky_item}

✨ 今日の魔法の一言 ✨  
{magic_phrase}
"""
