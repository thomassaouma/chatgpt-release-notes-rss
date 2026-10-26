# ChatGPT Release Notes RSS

RSS URL: https://thomassaouma.github.io/chatgpt-release-notes-rss/rss.xml

Unofficial feed from the official release notes, one item per announcement, latest 100 entries. Updated every six hours with GitHub Actions and published to GitHub Pages. No API key or paid service.

Apple Shortcuts: use Get Items from RSS Feed with the URL above.

Failures preserve the previous deployed feed. Dates are published dates at midnight UTC because the source gives no time. Stable IDs use date and title; title changes can create a new item.

GitHub can delay scheduled jobs and disables schedules in public repositories after 60 days without activity: if needed, re-enable the workflow in Actions. Monitor workflow failure emails. Source layout changes may require a parser update.

Local checks: `python -m unittest discover -s tests`; `python generate.py`.
