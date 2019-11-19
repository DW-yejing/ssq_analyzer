# coding: utf-8
import requests
import os
import configparser
import logging
import time
import xlwt
import random
from ugentlist import userAgents

agents = userAgents

def requestByDate():
    global agents
    logger = logging.getLogger(name="requestByDate")
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    cf.options("config")
    beginDate = cf.get("config", "beginDate")
    endDate = cf.get("config", "endDate")
    url = cf.get("config", "url")
    postdata = {
        "name": "ssq",
        "dayStart": beginDate,
        "dayEnd": endDate
    }
    headers = {
        "User-Agent": agents[random.randint(0, len(agents)-1)],
        "Referer": "http://www.cwl.gov.cn/kjxx/ssq/kjgg/"
    }
    res = requests.post(url=url, data=postdata, headers=headers)
    if not res.ok:
        logger.info("请求失败")
        return
    data = res.json()
    pageCount = data["pageCount"]
    countNum = data["countNum"]
    request(url, postdata, headers, pageCount)
    logger.info("数据统计完成，总共查询到%s条数据", str(countNum))

def request(url, postdata, headers, pageCount):
    global agents
    logger = logging.getLogger(name="request")
    list = []
    for i in range(1, pageCount+1):
        postdata["pageNo"] = i
        headers["User-Agent"] = agents[random.randint(0, len(agents)-1)]
        res = requests.post(url=url, data=postdata, headers=headers)
        if not res.ok:
            logger.info("请求失败")
            return
        data = res.json()
        results = data['result']
        for item in results:
            obj = {
                "code": item["code"],
                "red": item["red"],
                "blue": item["blue"],
                "date": item["date"],
                "sales": item["sales"]
            }
            list.append(obj)
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("Sheet1")
    for index in range(0, len(list)):
        rowno = index%10000+1
        sheet.write(rowno,0,list[index]["code"])
        sheet.write(rowno,1,list[index]["red"])
        sheet.write(rowno,2,list[index]["blue"])
        sheet.write(rowno,3,list[index]["sales"])
        sheet.write(rowno,4,list[index]["date"])
        if (index+1)==len(list) or (index+1)%10000==0:
            #写入标题
            sheet.write(0,0,"期号")
            sheet.write(0,1,"红球")
            sheet.write(0,2,"篮球")
            sheet.write(0,3,"总销售额（元）")
            sheet.write(0,4,"开奖日期")
            wb.save("ssq_"+str(int(time.time()))+".xls")
            wb = xlwt.Workbook()
            sheet = wb.add_sheet("Sheet1")


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, filename="logger.log", format="%(name)s - %(levelname)s - %(asctime)s - %(message)s")
    requestByDate()