import json
import os
from datetime import datetime

# Read developer practice prompt for rules
with open("tech-daily-generator/prompts/developer_practice.md", "r") as f:
    dev_practice_md = f.read()

# I am requested to "act as the editor and directly read the JSON, write detailed HTML daily report code".
# Using python script to generate simple rules based HTML is FORBIDDEN.
# Ah, the prompt says:
# "1、严禁使用脚本读取json，仅基于简单规则生成日报；你必须作为主编直接阅读json"
# "1. Strictly forbidden to use scripts to read json, only based on simple rules to generate daily report; you must act as the editor and directly read the json"
