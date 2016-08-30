#!python3

import appex
import clipboard
from console import hud_alert
from datetime import date

def main():
    date_as_md_title = date.today().strftime('# 0%Y-%m-%d')
    clipboard.set(date_as_md_title)
    hud_alert(date_as_md_title, 'success', 0.8)

if __name__ == '__main__':
    main()

