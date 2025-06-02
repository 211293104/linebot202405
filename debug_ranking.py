from sophie_fortune import generate_fortune_ranking
from datetime import datetime

def debug_ranking():
    today_str = datetime.now().strftime("%Y-%m-%d")
    ranking_list = generate_fortune_ranking(today_str)

    print(f"Generated ranking count: {len(ranking_list)}")
    for item in ranking_list:
        print(f"{item['sign']} {item['blood']} -> total: {item['total']}")

if __name__ == "__main__":
    debug_ranking()
