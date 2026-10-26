import unittest
import xml.etree.ElementTree as ET
from generate import entries, render

class FeedTests(unittest.TestCase):
    def test_multiple_announcements_and_stable_identifiers(self):
        html = '<h1>October 26, 2026</h1>' + ''.join(f'<h2>Update {i}</h2><p>Text &amp; detail {i}</p>' for i in range(6))
        items = entries(html)
        self.assertEqual(len(items), 6)
        root = ET.fromstring(render(items))
        self.assertEqual(root.findtext('channel/item/description'), 'Text & detail 0')
        changed = [(d,t,b+' edited') for d,t,b in items]
        self.assertEqual([x.text for x in root.findall('.//guid')], [x.text for x in ET.fromstring(render(changed)).findall('.//guid')])
    def test_block_page_fails_closed(self):
        with self.assertRaises(ValueError): entries('<h1>Access denied</h1>')
    def test_inline_comments_and_markup(self):
        html = '<h1><b>October 26, 2026</b></h1>' + ''.join(f'<h2>Lo<!-- -->cked {i}</h2><p>A <b>bold</b> word.</p>' for i in range(5))
        self.assertEqual(entries(html)[0][1:], ('Locked 0','A bold word.'))

if __name__ == '__main__': unittest.main()
