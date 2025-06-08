import random

def get_magic_phrase():
    regular_phrases = [
        "今日のあなたは、思ってるより魅力的です。",
        "小さなラッキーも、大事にすると大きくなります。",
        "迷ったときは、コイントスの気持ちで決めてみて。",
        "紅茶よりもココアが味方の日。あったかくしてね。",
        "今日のキーワードは「ふんわり」。力を抜いて。",
        "なんとなく、今の選択は正解です。",
        "運命は、たまにダジャレで話しかけてきます。",
        "あなたの「好き」は未来を変える鍵になります。",
        "今日は鏡の前でニッコリしてから出かけて。",
        "宇宙は応援してる。しかもけっこう本気で。",
        "意外と世界は、あなたのことが好きです。",
        "「ま、いっか」が運を呼びこむ呪文になる日。",
        "無理しないって、立派な勇気。",
        "今日のあなたは、心がラッキーカラー。",
        "深呼吸ひとつで、空気が味方に変わるよ。",
        "忘れものの中にチャンスが混ざってるかも。",
        "今日は「あと5分」だけがんばってみよう。",
        "頑張る人は、見えないところでちゃんと光ってます。",
        "エレベーターで一緒になった人、意外と福の神かも。",
        "クツの向きをそろえると、道が開けるよ。",
        "思い出す夢の断片、今日は大事にしてみて。",
        "あなたの「笑いのツボ」が人を癒します。",
        "猫っぽい気まぐれさが、今日は武器になります。",
        "今日の敵は、明日の笑い話です。",
        "やさしさは目に見えないラッキーアイテム。",
        "予定外のことが、運命の種になります。",
        "コインを拾ったら、裏の意味も感じてみて。",
        "自分に「おつかれ」と言える人は強い。",
        "ひとつ手放せば、ひとつ入ってくる。",
        "今日のあなたの直感は、たぶん本物。"
    ]

    ponkotsu_phrases = [
        "魔法のつもりが…え、出オチ！？💥",
        "ラッキーアイテムは…うっかり忘れた…ごめんネ！🙇‍♀️",
        "今日は適当でもなんとかなる気がします…たぶん…きっと…💦",
        "占星術よりカンで動いてみましょう（根拠なし）🌀",
        "星が寝坊してるので、代わりにソフィーが応援してます📣✨"
    ]

    return random.choice(ponkotsu_phrases if random.random() < 0.2 else regular_phrases)

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

  from datetime import datetime

def get_fortune_result(zodiac, blood):
    results = generate_fortune_ranking(date_str=datetime.now().strftime('%Y-%m-%d'))

    for idx, item in enumerate(results, 1):
        item["rank"] = idx - 1

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
