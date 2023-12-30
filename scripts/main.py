"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 29/12/2023
@Description  :
"""
from logs.config import setup_logging
from readme_handler import update_readme
from scripts.convert_links import convert_wiki_links_in_dir

if __name__ == '__main__':
    setup_logging()
    update_readme()
    convert_wiki_links_in_dir()
