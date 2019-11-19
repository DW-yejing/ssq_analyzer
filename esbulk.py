# encoding: utf-8
import logging
import configparser
import xlrd
import time
import os

def generateBulkFile(originDataFile):
    logger = logging.getLogger("generateBulkFile")
    wb = xlrd.open_workbook(originDataFile)
    sheet = wb.sheet_by_index(0)
    list = []
    for i in range(1, sheet.nrows):
        obj = {
            "code": sheet.cell(i, 0).value,
            "red": sheet.cell(i, 1).value,
            "blue": sheet.cell(i, 2).value
        }
        list.append(obj)
    filepath = os.path.join(os.path.curdir, "_bulk"+str(int(time.time()))+".json")
    with open(filepath, "a+", encoding="utf-8") as f:
        for i in range(0, len(list)):
            f.write('{ "index": {}}\n')
            line_content = ' "code":{}, "red":{}, "blue":{} '.format(list[i]["code"], list[i]["red"], list[i]["blue"])
            line_content = "{"+line_content+"}\n"
            f.write(line_content)
    return filepath

        

def execBulk(filepath):
    pass

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, filename="bulk_logger.log", format="%(name)s - %(levelname)s - %(asctime)s - %(message)s")
    cf = configparser.ConfigParser()
    cf.read("config.ini")
    cf.options("config")
    originDataFile = cf.get("config", "originDataFile")
    filepath = generateBulkFile(originDataFile)
    execBulk(filepath)