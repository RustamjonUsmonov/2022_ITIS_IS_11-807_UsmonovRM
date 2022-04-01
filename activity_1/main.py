import shutil, requests
from typing import Optional
from bs4 import BeautifulSoup


def get_next_link(bs: BeautifulSoup) -> Optional[str]:
    links = bs.select("a.pages__right")
    if len(links) > 0:
        for a in links:
            if a.attrs.get("href") is not None:
                r = requests.get('http://www.consultant.ru' + a.attrs["href"])
                return r.url
    else:
        return None


def main():
    i = 1
    index_page = 'http://www.consultant.ru/document/cons_doc_LAW_10699/e8ecf933c52a85d9223094e0e7fbf52f0128d399/'
    index = open("index.txt", "w", encoding="utf-8")

    while index_page is not None and i <= 100:
        print(f"Parsing {i} page")
        response = requests.get(index_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        site = open(f"activity_1/sites/{i}.txt", "w", encoding="utf-8")
        title = soup.select('h1')[0].text.strip()
        content = soup.find('div', {"class": "document-page__content document-page_left-padding"}).get_text(
            separator=" ").strip()

        site.write(f"{title}\n{content}")
        site.close()
        index.write(f"{i} {index_page}\n")
        i += 1
        index_page = get_next_link(soup)

    index.close()
    shutil.make_archive("activity_1/saves", 'zip', "activity_1/sites")


if __name__ == '__main__':
    main()
