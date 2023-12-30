"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 30/12/2023
@Description  : convert wiki-links like [[]] -> standard markdown links []()
"""
import re
from pathlib import Path
import logging

from common import  ROOT_PATH


def convert_obsidian_image_and_links_to_standard_md(content):
    obsidian_pattern = r'!\[\[(.+?)\]\]|\[\[(.+?)\]\]'

    def replace_obsidian(match):
        link_text = match.group(1) or match.group(2)
        parts = link_text.split('|')
        link = parts[0].strip().replace(' ', '%20')
        # 保留.md扩展名
        text = parts[1].strip() if len(parts) > 1 else link.replace('%20', ' ')

        # 如果是图片链接，添加感叹号前缀
        prefix = '!' if match.group(1) else ''
        return f'{prefix}[{text}]({link})'

    return re.sub(obsidian_pattern, replace_obsidian, content)


def convert_wiki_links_in_dir(directory: Path = ROOT_PATH, ext='.md'):
    def convert_wiki_links_in_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        converted_content = convert_obsidian_image_and_links_to_standard_md(
            content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(converted_content)

    pathlist = directory.rglob(f'*{ext}')
    i = 0
    for path in pathlist:
        convert_wiki_links_in_file(path)
        i += 1
    logging.info(f"Converted {i} files in {directory}")


if __name__ == "__main__":
    convert_wiki_links_in_dir(Path(r'C:\Users\18317\python\KnowledgeHub'))  # 替换为你的目录路径
