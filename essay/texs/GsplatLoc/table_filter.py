"""
Pandoc filter using panflute: scientific 2column mode fixes
This filter does the following:
    1) fixes longtables -> tabular

It's intended use is for scientific papers that require 2 columns in the template layotu.
"""
import sys
from panflute import *


def get_text(item):
    if isinstance(item, Str):
        return item.text
    elif isinstance(item, Cite):
        return get_text(item.content)  # Raw content
    elif isinstance(item, Plain):
        return ''.join([get_text(i) for i in item.content])
    elif isinstance(item, ListContainer):
        return ''.join([get_text(i) for i in item])
    else:
        raise TypeError('Unsupported filter type ! ' + type(item))

def replace_longtables_with_tabular(elem, doc):
    try:
        def tabular():
            # 使用 l 作为第一列，其余列使用 X,防止换因为名称出现'-'行
            return '\\begin{tabularx}{\\textwidth}{l' + 'X' * (elem.cols - 1) + '}\n\\toprule\n'

        def headers():
            if elem.head and elem.head.content:
                return ' & '.join([get_text(cell.content) for cell in elem.head.content[0].content]) + '\\\\\n\\midrule\n'
            return ''

        def items():
            rows = []
            for body in elem.content:
                for row in body.content:
                    rows.append(' & '.join([get_text(cell.content) for cell in row.content]) + '\\\\')
            return '\n'.join(rows) + '\n'

        def caption():
            if elem.caption and elem.caption.content:
                return '\\caption{' + get_text(elem.caption.content) + '}\n' + \
                    '\\label{table:' + (elem.identifier or '') + '}\n'
            return ''

        result = '\\begin{table*}[htbp]\n\\centering\n' + \
                 tabular() + \
                 headers() + \
                 items() + \
                 '\\bottomrule\n\\end{tabularx}\n' + \
                 caption() + \
                 '\\end{table*}'

        print("Table processed successfully", file=sys.stderr)
        return RawBlock(result, 'latex')
    except Exception as e:
        print(f"Error processing table: {str(e)}", file=sys.stderr)
        return elem


def prepare(doc):
    pass

def action(elem, doc):
    if doc.format != 'latex':
        return None

    if isinstance(elem, Table):
        print("Table found!", file=sys.stderr)
        return replace_longtables_with_tabular(elem, doc)

    return None

def finalize(doc):
    pass

def main(doc=None):
    return run_filter(action,
                      prepare=prepare,
                      finalize=finalize,
                      doc=doc)


if __name__ == '__main__':
    main()
