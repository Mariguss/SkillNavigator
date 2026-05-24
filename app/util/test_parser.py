import feedparser

url = "https://career.habr.com/vacancies/rss?currency=RUR&sort=relevance&type=all"

# feedparser сам скачает контент по URL
feed = feedparser.parse(
    url,
    agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
)

# Проверяем, нет ли ошибок парсинга
if feed.bozo:
    print("Внимание: возникла ошибка при чтении XML, но данные могут быть доступны.")

print(feed.entries)


# Выводим заголовки новостей
for entry in feed.entries:
    print(entry)
    print("Название вакансии:", (str(entry.title)).replace("Требуется ",""))
    print("Ссылка на вакансию:", entry.link) # для обработки ии потребуется перейти по ссылке и прочестоь текст
    print("Текст вакансии:", entry.summary)
    print("Компания:", entry.author)
    print("Дата публикации:", entry.published)
    break
