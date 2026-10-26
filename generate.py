"""Convert the official release notes to RSS 2.0 (Python standard library)."""
import argparse
import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from html.parser import HTMLParser
from pathlib import Path

SOURCE = 'https://help.openai.com/en/articles/6825453-chatgpt-release-notes'
FEED = 'https://thomassaouma.github.io/chatgpt-release-notes-rss/rss.xml'

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks, self.stack, self.text = [], [], []
        self.tag = None
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.stack.append(tag)
        elif self.stack:
            return
        elif self.tag:
            if tag in ('br', 'p', 'li'):
                self.text.append('\n')
        elif tag in ('h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'pre', 'blockquote'):
            self.tag, self.text = tag, []
    def handle_endtag(self, tag):
        if self.stack:
            if tag == self.stack[-1]: self.stack.pop()
            return
        if tag == self.tag:
            value = ''.join(self.text)
            value = '\n'.join(re.sub(r'[ \t]+', ' ', x).strip() for x in value.splitlines()).strip()
            if value: self.blocks.append((tag, value))
            self.tag, self.text = None, []
        elif self.tag and tag in ('li', 'p'):
            self.text.append('\n')
    def handle_data(self, data):
        if self.tag and not self.stack: self.text.append(data)

def entries(html):
    parser = Blocks()
    parser.feed(html)
    result, date, title, body = [], None, None, []
    def flush():
        if date and body:
            result.append((date, title or 'ChatGPT update — ' + date.strftime('%B %d, %Y'), '\n\n'.join(body)))
    for tag, value in parser.blocks:
        try:
            parsed = datetime.strptime(value, '%B %d, %Y').replace(tzinfo=timezone.utc)
        except ValueError:
            parsed = None
        if tag in ('h1', 'h2', 'h3') and parsed:
            flush()
            date, title, body = parsed, None, []
        elif date and tag == 'h2':
            flush()
            title, body = value, []
        elif date and tag == 'h1':
            break
        elif date:
            body.append(value)
    flush()
    if len(result) < 5:
        raise ValueError('Source structure changed or fetch blocked: refusing to publish an empty/partial feed')
    return sorted(result, key=lambda x: x[0], reverse=True)[:100]

def render(items):
    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    for key, value in [('title', 'ChatGPT Release Notes (unofficial RSS)'), ('link', SOURCE), ('description', 'Updates from the official ChatGPT release notes. Unofficial RSS, refreshed every six hours.'), ('language', 'en'), ('ttl', '360')]:
        ET.SubElement(channel, key).text = value
    ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link', href=FEED, rel='self', type='application/rss+xml')
    seen = set()
    for date, title, body in items:
        uid = hashlib.sha256((date.date().isoformat() + '\n' + title).encode()).hexdigest()
        if uid in seen: continue
        seen.add(uid)
        item = ET.SubElement(channel, 'item')
        for key, value in [('title', title), ('link', SOURCE), ('description', body), ('pubDate', format_datetime(date))]:
            ET.SubElement(item, key).text = value
        ET.SubElement(item, 'guid', isPermaLink='false').text = 'chatgpt-release-notes:' + uid
    ET.indent(rss)
    return ET.tostring(rss, encoding='utf-8', xml_declaration=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path)
    ap.add_argument('--output', type=Path, default=Path('public/rss.xml'))
    args = ap.parse_args()
    if args.input:
        html = args.input.read_text()
    else:
        req = urllib.request.Request(SOURCE, headers={'User-Agent': 'ChatGPTReleaseNotesRSS/1.0 (+https://github.com/thomassaouma/chatgpt-release-notes-rss)'})
        with urllib.request.urlopen(req, timeout=60) as response:
            html = response.read().decode('utf-8')
    items = entries(html)
    content = render(items)
    ET.fromstring(content)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.with_suffix('.tmp').write_bytes(content)
    args.output.with_suffix('.tmp').replace(args.output)
    print(f'Validated {len(items)} entries; latest: {items[0][1]}')

if __name__ == '__main__': main()
