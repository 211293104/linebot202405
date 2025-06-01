# ソフィー：LINE連携用 全体コード（完全ダミーデータ対応版）

def generate_fortune_ranking(date_str):
    return [
        {
            'sign': 'おひつじ座',
            'blood': 'A型',
            'rank': 1,
            'money': 5,
            'work': 4,
            'love': 3,
            'lucky_action': '赤いものを身につけると吉！'
        },
        {
            'sign': 'おうし座',
            'blood': 'B型',
            'rank': 2,
            'money': 3,
            'work': 5,
            'love': 4,
            'lucky_action': '朝一番の深呼吸で気分アップ！'
        },
        {
            'sign': 'ふたご座',
            'blood': 'O型',
            'rank': 3,
            'money': 2,
            'work': 3,
            'love': 5,
            'lucky_action': '笑顔を意識して話すと運気向上！'
        }
    ]

class FortuneBot:
    def __init__(self):
        self.line_greeting = "こんにちは！占い師ソフィーです🌸"
        self.help_message = "キーワードを入力してくださいね。運勢やアドバイスをご希望の場合は『アドバイス希望』と送ってください！"

    def get_today_fortune(self, zodiac, blood_type):
        return f"{zodiac}×{blood_type}さん、今日は挑戦に向く日ですよ！"

    def handle_keyword(self, keyword, zodiac, blood_type):
        if keyword == "アドバイス希望":
            advice = self.get_advice(zodiac, blood_type)
            return advice
        else:
            return "ごめんなさい、そのキーワードはわかりません💦『アドバイス希望』と送ってくださいね。"

    def get_advice(self, zodiac, blood_type):
        advice_list = [
            "今日は焦らず、着実にいきましょう。",
            "新しいことにチャレンジすると良い日です！",
            "周囲の人に感謝を伝えると運気アップ。",
            "無理せず休息を大事にしてね。"
        ]
        import random
        advice = random.choice(advice_list)
        return f"{zodiac}×{blood_type}さんへの今日のアドバイス：{advice}"

# LINE側の処理例
def line_greeting():
    bot = FortuneBot()
    return bot.line_greeting

def line_help():
    bot = FortuneBot()
    return bot.help_message

# main.py想定の流れ
if __name__ == "__main__":
    from datetime import datetime
    
    bot = FortuneBot()
    zodiac = "おひつじ座"
    blood_type = "A型"
    
    print(line_greeting())
    print(line_help())
    print(bot.get_today_fortune(zodiac, blood_type))
    print(bot.handle_keyword("アドバイス希望", zodiac, blood_type))
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    ranking_list = generate_fortune_ranking(today_str)
    
    print(f"ダミーランキング取得: {ranking_list}")
