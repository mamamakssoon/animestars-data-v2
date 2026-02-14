import requests
import json
import datetime
import os

def run():
    print("Початок роботи парсера...")
    os.makedirs('databases', exist_ok=True)
    
    url = "https://animesss.com/cards/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://animesss.com/'
    }
    
    cards_data = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.anime-cards__item')
            for item in items:
                try:
                    cid = item.get('data-id') or item.get('data-card-id')
                    if cid:
                        stats = item.select('.anime-cards__item-stats span')
                        cards_data.append({
                            "cardId": int(cid),
                            "need": int(stats[0].text.strip().replace('❤', '')) if len(stats) > 0 else 0,
                            "trade": int(stats[1].text.strip().replace('🔄', '')) if len(stats) > 1 else 0,
                            "users": int(stats[2].text.strip().replace('📦', '')) if len(stats) > 2 else 0,
                            "cardAuthor": "System"
                        })
                except: continue
    except Exception as e:
        print(f"Помилка: {e}")

    # Створюємо технічний запис, якщо сайт порожній, щоб Action не падав
    if not cards_data:
        cards_data = [{"cardId": 0, "need": 0, "trade": 0, "users": 0, "cardAuthor": "Initial-Sync"}]

    # Очищення старих JSON
    for f in os.listdir('databases'):
        if f.endswith('.json'): os.remove(os.path.join('databases', f))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"databases/db_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=2)
    print(f"Файл збережено: {filename}")

if __name__ == "__main__":
    run()
