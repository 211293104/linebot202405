import random
import hashlib

# 星座と血液型の組み合わせリスト
zodiac_signs = [
    "牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座",
    "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"
]
blood_types = ["A型", "B型", "O型", "AB型"]

# ラッキーアクションのサンプル
lucky_actions = [
    "笑顔であいさつする", "新しい道を歩く", "カフェで一息つく",
    "靴をピカピカにする", "青い小物を身につける", "深呼吸を3回する",
    "今日の目標を紙に書く", "友達に感謝を伝える"
]

def generate_seed(date_str):
    """日付文字列からシードを生成"""
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16) % (10 ** 8)

def generate_fortune_ranking(date_str):
    """日付ごとに固定のランキングを生成"""
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

    # 合計ポイントで降順ソート
    results.sort(key=lambda x: x["total"], reverse=True)

    # 順位を付与
    for idx, item in enumerate(results, 1):
        item["rank"] = idx

    return results
