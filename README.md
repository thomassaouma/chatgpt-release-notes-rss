# ChatGPT Release Notes RSS

RSS URL: https://thomassaouma.github.io/chatgpt-release-notes-rss/rss.xml

## Current status — October 26, 2026

The published feed is a verified snapshot containing 100 announcements. Automatic refresh is configured every six hours but is NOT operational: the official source returns HTTP 403 from GitHub-hosted runners, both with Python urllib and curl. Do not rely on this feed for future updates until this is resolved. The last published feed is preserved when refresh fails.

The snapshot was generated from the exact official source page downloaded successfully in the authoring environment. The separate Publish verified RSS snapshot workflow publishes committed public/rss.xml; the scheduled Update workflow only publishes after successfully downloading and validating the live source.

Apple Shortcuts: use Get Items from RSS Feed with the URL above.

No API key or paid service configured. Dates use midnight UTC since the source provides no time. Stable IDs use date and title; title changes can create a new item. Latest 100 entries retained.

Local checks: `python -m unittest discover -s tests`; `python generate.py --input source.html`.
