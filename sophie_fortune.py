import random
import hashlib

zodiac_signs = [
    "牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座",
    "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"
]
blood_types = ["AB型", "A型", "B型", "O型"]

lucky_actions = [
    "笑顔であいさつしてみよう", "新しい道を歩いてみよう", "カフェで一息ついてみよう",
    "靴をピカピカにしてみよう", "青い小物を身につけよう", "深呼吸を3回してリフレッシュ",
    "今日の目標を紙に書いてみよう", "友達に感謝を伝えてみよう"
]

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
            action = random.choice(lucky_actions)
            results.append({
                "sign": sign,
                "blood": blood,
                "money": money,
                "work": work,
                "love": love,
                "total": total,
                "lucky_action": action
            })

    results.sort(key=lambda x: x["total"], reverse=True)

    for idx, item in enumerate(results, 1):
        item["rank"] = idx

    return results
