"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 29/12/2023
@Description  :
"""
import logging
from pathlib import Path
HEAD_TITLE = "## 快捷导航"
ROOT_PATH = Path(__file__).parents[1]
EXCLUDE_DIRS = []


def generate_markdown_links() -> str:
    """
    Generates markdown links for all files and directories in the given root_path.
    """
    def create_links(path: Path, level: int = 0) -> list:
        links = []
        for item in path.iterdir():
            if (EXCLUDE_DIRS and item.name in EXCLUDE_DIRS):
                continue

            if item.is_dir():
                links.append(f"{'  ' * level}- **{item.name}/:**")
                links.extend(create_links(item, level + 1))
            elif item.is_file():
                rel_path = item.relative_to(ROOT_PATH).as_posix()
                links.append(
                    f"{'  ' * (level + 1)}- [{item.name}]({rel_path})")
            else:
                logging.warning(f"Unknown file type: {item}")
        return links

    markdown_links = create_links(ROOT_PATH / 'docs')
    return '\n'.join(markdown_links)


README_PATH = ROOT_PATH / "README.md"


def update_readme_content(new_content: str, header_title: str):
    """
    Update the README.md file by replacing content under the specified header title
    with new_content.
    """
    if not README_PATH.exists() or not README_PATH.is_file():
        logging.error(f"README.md not found at {README_PATH}")
        return

    with README_PATH.open('r+', encoding='utf-8') as file:
        lines = file.readlines()
        start_index = None
        end_index = None

        # Find the start and end index for the replacement
        for i, line in enumerate(lines):
            if line.strip() == header_title:
                start_index = i + 1
            elif start_index is not None and line.startswith('## ') and not line.strip() == header_title:
                end_index = i
                break

        # Replace the content if the header title is found
        if start_index is not None:
            end_index = end_index or len(lines)
            lines[start_index:end_index] = [new_content + '\n']

        # Write back to the file
        file.seek(0)
        file.writelines(lines)
        file.truncate()


def update_readme():
    """
    Update the README.md file by replacing content under the specified header title
    with new_content.
    """
    new_content = generate_markdown_links()
    update_readme_content(new_content, HEAD_TITLE)


def update_recently_modified():
    """
    Update the README.md file by replacing content under the specified header title
    with new_content.
    """
    import subprocess
    import re

    # 获取最近五次提交的哈希值
    commits = subprocess.check_output(
        ['git', 'log', '-15', '--pretty=format:%H'],
        universal_newlines=True
    ).splitlines()

    # 用于存储提交和修改文件的信息
    commit_changes = {}

    # 遍历每次提交，获取修改的文件列表
    for commit in commits:
        files_changed = subprocess.check_output(
            ['git', 'diff-tree', '--no-commit-id', '--name-status', '-r', commit],
            universal_newlines=True
        )
        # 解析文件状态和文件名
        changes = re.findall(r'(\w)\s+(.+)', files_changed)
        commit_changes[commit] = changes

    # 为文件状态分配前缀或 emoji
    status_prefix = {
        'A': '✨',  # 文件添加
        'M': '🔨',  # 文件修改
        'D': '🗑️',  # 文件删除
        'R': '🚚',  # 文件重命名或移动
    }

    # 生成 Markdown 格式的提交和文件更改列表
    markdown_list = []
    for commit, changes in commit_changes.items():
        markdown_list.append(f"### Commit {commit[:7]}")
        before = len(markdown_list)
        for status, file in changes:
            if not file.startswith('docs/'):
                continue
            prefix = status_prefix.get(status, '')
            markdown_list.append(f"- {prefix} {file}")
        if len(markdown_list) == before:
            # clean useless commit imformation
            markdown_list.pop()
    # 将生成的列表转换为字符串
    markdown_content = '\n'.join(markdown_list)

    # 打印结果，或者将其写入 README.md 文件
    print(markdown_content)
if __name__ == '__main__':
    from scripts.logs.config import setup_logging
    setup_logging()
    update_recently_modified()
