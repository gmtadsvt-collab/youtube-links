import scrapetube
import csv
from datetime import date

# Впишите сюда свои запросы через запятую, каждый в кавычках
KEYWORDS = ["residential proxy"]

# Сколько видео брать по каждому запросу
LIMIT_PER_KEYWORD = 500

rows = []
for kw in KEYWORDS:
    videos = scrapetube.get_search(kw, limit=LIMIT_PER_KEYWORD, sort_by="upload_date")
    for video in videos:
        try:
            video_id = video["videoId"]
            title = video["title"]["runs"][0]["text"]
        except (KeyError, IndexError):
            continue
        link = f"https://www.youtube.com/watch?v={video_id}"
        rows.append([kw, title.replace("|", "-"), link, str(date.today())])

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Запрос", "Название", "Ссылка", "Дата сбора"])
    writer.writerows(rows)

with open("body.md", "w", encoding="utf-8") as f:
    f.write(f"Собрано ссылок: {len(rows)}\n\n")
    f.write("| Запрос | Видео | Дата |\n|---|---|---|\n")
    for kw, title, link, d in rows:
        f.write(f"| {kw} | [{title}]({link}) | {d} |\n")

print(f"Собрано {len(rows)} ссылок")
