import xml.etree.ElementTree as ET
from urllib.request import urlopen
from datetime import datetime

FEEDS = {
    "G1 Política": "https://g1.globo.com/rss/g1/politica/",
    "Folha Poder": "https://www1.folha.uol.com.br/poder/rss.xml"
}


def fetch_feed(url: str) -> bytes:
    with urlopen(url) as resp:
        return resp.read()

def parse_feed(xml_content: bytes):
    root = ET.fromstring(xml_content)
    for item in root.findall('.//item'):
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        pub_date = item.findtext('pubDate') or ''
        yield {
            'title': title.strip(),
            'link': link.strip(),
            'pub_date': pub_date.strip()
        }

def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except Exception:
        return datetime.min

def main():
    entries = []
    for source, url in FEEDS.items():
        try:
            data = fetch_feed(url)
            for item in parse_feed(data):
                item['source'] = source
                entries.append(item)
        except Exception as exc:
            print(f'Erro ao obter {source}: {exc}')
    entries.sort(key=lambda x: parse_date(x['pub_date']), reverse=True)
    for e in entries[:10]:
        date = e['pub_date']
        print(f"[{e['source']}] {e['title']} ({date})")
        print(f"  {e['link']}")
        print()

if __name__ == '__main__':
    main()
