import xlrd
import json


def xlsxprocess(xlsname, max, sheet=1, qcol=1, acol=2):
    xlsxfile = xlrd.open_workbook(xlsname)
    table = xlsxfile.sheets()[sheet - 1]
    nrows = table.nrows
    qalist = []
    for i in range(nrows):
        if i == max:
            break
        q = table.cell(i, qcol - 1).value
        a = table.cell(i, acol - 1).value
        qalist.append([q, a])
    qadict = {}
    qadict[xlsname.split('/')[-1].split('.')[0]] = qalist
    print(len(qalist))
    return qadict

if __name__ == '__main__':
    qadict = xlsxprocess('../corpus/data/test/finance.xlsx',-1,1,6,7)
    with open('../corpus/data/test/finance.json','w',encoding='utf-8') as f:
        json.dump(qadict,f)