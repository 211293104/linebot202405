import hashlib
from datetime import datetime
import random

zodiac_signs = [
    "おひつじ座", "おうし座", "ふたご座", "かに座", "しし座", "おとめ座",
    "てんびん座", "さそり座", "いて座", "やぎ座", "みずがめ座", "うお座"
]

blood_types = ["A型", "B型", "O型", "AB型"]

lucky_actions = [
    "笑顔であいさつ", "靴をそろえる", "深呼吸3回", "緑色のものを持つ",
    "5分間のストレッチ", "知らない人にやさしくする", "大きな声で挨拶する"
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
            total = money * work + love
            action = random.choice(lucky_actions)
            results.append({
                "sign": sign,
                "blood": blood,
                "money": money,
                "work": work,
                "love": love,
                "total": total,
                "Lucky_action": action
            })

    results.sort(key=lambda x: x["total"], reverse=True)

    for idx, item in enumerate(results, 1):
        item["rank"] = idx - 1

    return results

def get_fortune_result(zodiac, blood):
    results = generate_fortune_ranking(date_str=datetime.now().strftime('%Y-%m-%d'))

    for item in results:
        if item["sign"] == zodiac and item["blood"] == blood:
            return item

    return {
        "money": 0,
        "work": 0,
        "love": 0,
        "total": 0,
        "Lucky_action": "何もしない",
        "rank": 47
    }

def get_magic_phrase():
    regular_phrases = [
        "今日のあなたは、思ってるより魅力的です。",
        "小さなラッキーも、大事にすると大きくなります。",
        "迷ったときは、コイントスの気持ちで決めてみて。",
        "紅茶よりもココアが味方の日。あったかくしてね。",
        "今日のキーワードは『ふんわり』。力を抜いて。",
        "運命は、たまにダジャレで話しかけてきます。",
        "あなたの『好き』は未来を変える鍵になります。",
        "今日は鏡の前でニッコリしてから出かけて。",
        "宇宙は応援してる。しかもけっこう本気で。",
        "『ま、いっか』が運を呼びこむ呪文になる日。",
        "無理しないって、立派な勇気。",
        "クツの向きをそろえると、道が開けるよ。",
        "あなたの『笑いのツボ』が人を癒します。",
        "今日の敵は、明日の笑い話です。",
        "やさしさは目に見えないラッキーアイテム。",
        "自分に『おつかれ』と言える人は強い。",
        "ひとつ手放せば、ひとつ入ってくる。",
        "今日のあなたの直感は、たぶん本物。",
    ]

    ponkotsu_phrases = [
        "魔法のつもりが…出オチ！？💥",
        "ラッキーアイテムは…うっかり忘れた…ごめんネ！🙇‍♀️",
        "今日は適当でもなんとかなる気がします…たぶん…きっと…💦",
        "占星術よりカンで動いてみましょう（根拠なし）🌀",
        "星が寝坊してるので、代わりにソフィーが応援してます📣✨"
    ]

    return random.choice(ponkotsu_phrases if random.random() < 0.2 else regular_phrases)
