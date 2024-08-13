"""
Pandoc filter using panflute: scientific 2column mode fixes
This filter does the following:
    1) fixes longtables -> tabular

It's intended use is for scientific papers that require 2 columns in the template layotu.
"""
import sys

import pandas as pd
from panflute import *


def color_cell(value, rank):
    colors = {
        1: "\\cellcolor{green!30}\\textbf{",
        2: "\\cellcolor{yellow!30}",
        3: "\\cellcolor{lime!50}",
    }
    # bold no.1
    color_start = colors.get(rank, "")
    color_end = "}" if rank == 1 else ""
    return f"{color_start}{value:.2f}{color_end}"


def process_table_data(data, is_lower_better):
    df = pd.DataFrame(data)

    for col in df.columns[1:]:  # 跳过第一列（方法名）
        col_data = pd.to_numeric(df[col], errors="coerce")
        if is_lower_better:
            ranks = col_data.rank(method="min")
        else:
            ranks = col_data.rank(method="min", ascending=False)
        df[col] = [
            color_cell(float(val), rank) if pd.notnull(val) else val
            for val, rank in zip(col_data, ranks)
        ]
    return df.astype(str)


def get_text(item):
    if isinstance(item, (Str, Math, RawInline)):
        return item.text
    elif isinstance(item, Space):
        return " "
    # elif isinstance(item, ListContainer):
    #     # return "".join([get_text(i) for i in item])
    #     return stringify(item)
    else:
        return stringify(item)


table_count = 0
current_table_pair = []


def replace_longtables_with_tabular(elem, doc, is_paired):
    global table_count
    try:

        def tabular():
            # 使用 l 作为第一列，其余列使用 X,防止换因为名称出现'-'行
            width = "0.48" if is_paired else "1.0"
            return (
                "\\begin{tabularx}{"
                + width
                + "\\textwidth}{l"
                + "X" * (elem.cols - 1)
                + "}\n\\toprule\n"
            )

        def headers():
            if elem.head and elem.head.content:
                return (
                    " & ".join(
                        [get_text(cell) for cell in elem.head.content[0].content]
                    )
                    + "\\\\\n\\midrule\n"
                )
            return ""

        def items():
            # collect data
            data = []
            for body in elem.content:
                for row in body.content:
                    data.append([get_text(cell) for cell in row.content])
            # color data
            is_lower_better = "↓" in (
                get_text(elem.caption.content[0])
                if elem.caption and elem.caption.content
                else ""
            )
            df = process_table_data(data, is_lower_better)
            # format data as latex table
            rows = []
            for index, row in df.iterrows():
                cells = list(row)

                if index == len(df) - 1:
                    cells[0] = "\\textbf{" + cells[0] + "}"
                rows.append(" & ".join(cells) + "\\\\")
                if index == len(df) - 2 and len(df) > 1:  # 确保至少有两行
                    rows.append("\\midrule")  # 在最后一行之前添加分割线
            return "\n".join(rows) + "\n"

        def caption():
            if elem.caption and elem.caption.content:
                caption_text = get_text(elem.caption)
                return (
                    "\\caption{"
                    + caption_text
                    + "}\n"
                    + "\\label{table:"
                    + (elem.identifier or "")
                    + "}\n"
                )
            return ""

        result = (
            tabular()
            + headers()
            + items()
            + "\\bottomrule\n\\end{tabularx}\n"
            + caption()
        )

        print(f"Table {table_count} processed successfully", file=sys.stderr)
        return result
    except Exception as e:
        print(f"Error processing table {table_count}: {str(e)}", file=sys.stderr)
        return elem


def prepare(doc):
    global table_count
    table_count = 0


def action(elem, doc):
    global table_count, current_table_pair
    if doc.format != "latex":
        return None

    if isinstance(elem, Table):
        table_count += 1
        print(f"Table {table_count} found!", file=sys.stderr)

        is_paired = table_count % 2 == 0
        processed_table = replace_longtables_with_tabular(elem, doc, is_paired)

        if is_paired:
            current_table_pair.append(processed_table)
            if len(current_table_pair) == 2:
                result = RawBlock(
                    "\\begin{table*}[htbp]\n\\centering\n"
                    + "\\begin{minipage}[t]{0.48\\textwidth}\n"
                    + current_table_pair[0]
                    + "\n\\end{minipage}\n\\hfill\n"
                    + "\\begin{minipage}[t]{0.48\\textwidth}\n"
                    + processed_table
                    + "\n\\end{minipage}\n"
                    + "\\end{table*}",
                    "latex",
                )
                current_table_pair = []
                return result
            return []  # 返回空列表，等待下一个表格
        else:
            current_table_pair = []
            return RawBlock(
                "\\begin{table}[htbp]\n\\centering\n"
                + processed_table
                + "\\end{table}",
                "latex",
            )

    return None


def finalize(doc):
    global current_table_pair
    if len(current_table_pair) == 1:
        # 如果最后剩下一个未配对的表格，将其作为全宽度表格
        last_table = current_table_pair[0].replace("0.48\\textwidth", "\\textwidth")
        doc.content.append(
            RawBlock(
                "\\begin{table}[htbp]\n\\centering\n" + last_table + "\\end{table}",
                "latex",
            )
        )


def main(doc=None):
    return run_filter(action, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
