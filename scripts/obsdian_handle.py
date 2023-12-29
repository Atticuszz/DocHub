"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 29/12/2023
@Description  :
"""
import logging
import subprocess
from pathlib import Path


def run_command(command):
    """ 运行命令行指令 """
    process = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)
    if process.returncode != 0:
        logging.error(f'Error: {process.stderr}')
        exit(process.returncode)
    logging.info(process.stdout)
    return process


def main():
    # 添加 .obsidian 文件夹
    obsidian_path = Path(__file__).parent.parent / '.obsidian'
    run_command(f'git add -f {obsidian_path.as_posix()}')

    # 提交更改
    commit_message = "basic update .obsidian"
    run_command(f'git commit -m "{commit_message}"')

    # 推送到远程仓库
    run_command('git push')

    # 从版本控制中移除 .obsidian 文件夹
    # run_command(f'git rm --cached -r {obsidian_path.as_posix()}')
    # run_command('git commit -m "Remove .obsidian from tracking"')
    # run_command('git push')


if __name__ == "__main__":
    main()
