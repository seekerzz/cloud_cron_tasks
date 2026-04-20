#!/bin/bash
jq '.articles | limit(20; .[]) | {title, summary, link, feed_title}' DEST_REPO/tech-daily/freshrss_24h_compact_20260331_015039.json > validation/first20.txt
