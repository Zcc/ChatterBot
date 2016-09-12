import xlrd
import json


def xlsxprocess(xlsname, max, sheet=1, qcol=1, acol=2):
    xlsxfile = xlrd.open_workbook(xlsname)
    table = xlsxfile.sheets()[sheet - 1]
    nrows = table.nrows
    qalist = []
    for i in range(1, nrows):
        if i == max:
            break
        q = str(table.cell(i, qcol - 1).value)
        a = str(table.cell(i, acol - 1).value).replace('金童', '麻酱')
        qalist.append([q, a])
    qadict = {}
    qadict[xlsname.split('/')[-1].split('.')[0]] = qalist
    print(len(qalist))
    return qadict


if __name__ == '__main__':
    qadict = xlsxprocess('../corpus/data/test/common.xlsx', -1, 1, 4, 5)
    with open('../corpus/data/test/common.json', 'w', encoding='utf-8') as f:
        json.dump(qadict, f)
