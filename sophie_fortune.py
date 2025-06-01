# ソフィー：LINE連携用の全体コード修正版

class FortuneBot:
    def __init__(self):
        self.line_greeting = "こんにちは！占い師ソフィーです🌸"
        self.help_message = "キーワードを入力してくださいね。運勢やアドバイスをご希望の場合は『アドバイス希望』と送ってください！"

    def get_today_fortune(self, zodiac, blood_type):
        # 簡易版の運勢コメント
        return f"{zodiac}×{blood_type}さん、今日は挑戦に向く日ですよ！"

    def handle_keyword(self, keyword, zodiac, blood_type):
        if keyword == "アドバイス希望":
            advice = self.get_advice(zodiac, blood_type)
            return advice
        else:
            return "ごめんなさい、そのキーワードはわかりません💦『アドバイス希望』と送ってくださいね。"

    def get_advice(self, zodiac, blood_type):
        # 星座×血液型に基づく簡易アドバイス
        advice_list = [
            "今日は焦らず、着実にいきましょう。",
            "新しいことにチャレンジすると良い日です！",
            "周囲の人に感謝を伝えると運気アップ。",
            "無理せず休息を大事にしてね。"
        ]
        import random
        advice = random.choice(advice_list)
        return f"{zodiac}×{blood_type}さんへの今日のアドバイス：{advice}"

# LINE側の処理（例示）
def line_greeting():
    bot = FortuneBot()
    return bot.line_greeting

def line_help():
    bot = FortuneBot()
    return bot.help_message

# 使用例（バックエンド側で呼び出し）
if __name__ == "__main__":
    bot = FortuneBot()
    zodiac = "おひつじ座"
    blood_type = "A型"
    
    print(line_greeting())
    print(line_help())
    print(bot.get_today_fortune(zodiac, blood_type))
    print(bot.handle_keyword("アドバイス希望", zodiac, blood_type))
