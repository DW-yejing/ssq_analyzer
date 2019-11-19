# encoding: utf-8
import logging
import configparser
import xlrd
import time
import os
import re

def generateBulkFile(originDataFile):
    logger = logging.getLogger("generateBulkFile")
    wb = xlrd.open_workbook(originDataFile)
    sheet = wb.sheet_by_index(0)
    red_values = []
    for i in range(1, sheet.nrows):
        obj = {
            "code": sheet.cell(i, 0).value,
            "red": sheet.cell(i, 1).value,
            "blue": str(int(sheet.cell(i, 2).value))
        }
        red_values.append(obj)
    filepath = os.path.join(os.path.curdir, "_bulk"+str(int(time.time()))+".json")
    with open(filepath, "a+", encoding="utf-8") as f:
        for i in range(0, len(red_values)):
            f.write('{ "index": {}}\n')
            #解析红球
            reds_str = red_values[i]["red"]
            reds_str = re.sub(r'(?<=\b)0(?=\d\b)', '', reds_str)
            line_content = ' "code":{}, "red":[{}], "blue":{} '.format(red_values[i]["code"], reds_str, red_values[i]["blue"])
            line_content = "{"+line_content+"}\n"
            f.write(line_content)
    logger.info("入库文件已生成：%s", filepath)
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