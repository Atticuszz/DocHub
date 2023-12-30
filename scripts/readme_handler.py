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
HEAD_TITLE_2 = "## 最近修改"
ROOT_PATH = Path(__file__).parents[1]
EXCLUDE_DIRS = []


def generate_quick_navigation_links() -> str:
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





def update_recently_modified(target_dir: str = 'docs')->str:
    """
    Update the README.md file by replacing content under the specified header title
    with new_content.
    """
    import subprocess
    import re
    # 获取和解析 Git 提交数据

    def get_git_changes(num_commits):
        # 使用唯一分隔符（例如 "|||"）来分隔日期、作者和提交信息
        separator = "|||"
        commit_log = subprocess.check_output(
            [
                'git',
                'log',
                f'-{num_commits}',
                f'--pretty=format:%ad{separator}%an{separator}%s',
                '--date=short',
                '--name-status'],
            universal_newlines=True)

        commit_changes = []
        current_commit_info = []
        for line in commit_log.splitlines():
            if separator in line:
                # 分割日期、作者和提交信息
                parts = line.split(separator)
                date, author, message = parts[0], parts[1], parts[2]
                current_commit_info = {
                    'date': date,
                    'author': author,
                    'message': message,
                    'changes': []}
                commit_changes.append(current_commit_info)
            else:
                match = re.match(r'^([AMDRT])(\d+)?\t(.+?)(?:\t(.+))?$', line)
                if match and current_commit_info:
                    current_commit_info['changes'].append(match.groups())
        return commit_changes

    # 处理解析后的数据并生成 Markdown 内容
    def generate_markdown(commit_changes)->str:
        # 定义文件状态的 emoji
        status_emojis = {
            'A': '✨',  # Added
            'M': '🔨',  # Modified
            'D': '🗑️',  # Deleted
            'R': '🚚',  # Renamed
        }

        # 生成 Markdown
        markdown_lines = []
        for commit in commit_changes:
            # head of commit msg
            markdown_lines.append(
                f"### {commit['date']} {commit['author']} : {commit['message']}")
            start_index = len(markdown_lines)
            for status, _, path, renamed in commit['changes']:
                if not path.startswith(target_dir):
                    continue
                emoji = status_emojis.get(status, '')

                # for special case of renamed files, show both old and new paths
                if status == 'R' and renamed:
                    old_path, new_path = path, renamed
                    old_path_name = Path(old_path).name
                    new_path_name = Path(new_path).name
                    rel_path = Path(new_path).as_posix()
                    linked_path = f"[{new_path_name}]({rel_path})"
                    markdown_lines.append(
                        f"- {emoji} {linked_path} <- {old_path_name}")
                else:
                    rel_path = Path(path).as_posix()
                    path_name = Path(path).name
                    # no need to link dead files
                    if status != 'D':
                        linked_path = f"[{path_name}]({rel_path})"
                    else:
                        linked_path = path
                    markdown_lines.append(f"- {emoji} {linked_path}")

            if len(markdown_lines) == start_index:
                # clean
                markdown_lines.pop()

        return '\n'.join(markdown_lines)

    # 使用上面定义的函数
    commit_changes = get_git_changes(15)
    markdown_content = generate_markdown(commit_changes)
    return markdown_content

def update_readme():
    """
    Update the README.md file by replacing content under the specified header title
    with new_content.
    """
    new_content = generate_quick_navigation_links()
    update_readme_content(new_content, HEAD_TITLE)
    new_content = update_recently_modified()
    update_readme_content(new_content, HEAD_TITLE_2)

if __name__ == '__main__':
    from scripts.logs.config import setup_logging
    setup_logging()
    new = update_recently_modified()
    update_readme_content(new, HEAD_TITLE_2)

