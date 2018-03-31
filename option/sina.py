# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
import json
import logging
import time
import pandas as pd

assets = [
    {'code': '510050', 'name': '50ETF'},
]

columns = [
    'bid_num',             #买量
    'bid',                 #买价
    'latest_price',
    'ask',
    'ask_num',
    'hold',                #持仓
    'change_ratio',        #涨幅
    'strike',
    'pre_close',
    'open',
    'ceiling',
    'floor',

    'ask5',
    'ask5_num',
    'ask4',
    'ask4_num',
    'ask3',
    'ask3_num',
    'ask2',
    'ask2_num',
    'ask1',
    'ask1_num',
    'bid1',
    'bid1_num',
    'bid2',
    'bid2_num',
    'bid3',
    'bid3_num',
    'bid4',
    'bid4_num',
    'bid5',
    'bid5_num',

    'time',
    'is_main',
    'status_code',
    'type',
    'asset_code',
    'short_name',
    'amplitude',
    'high',
    'low',
    'volume',
    'amount',
    'label'
]


def get_trading_months(retry=3, pause=1):
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName"
    for _ in range(retry):
        try:
            req = Request(url)
            res = urlopen(req, timeout=9).read()
            logging.debug(res)
            js = json.loads(res.decode('utf-8'))
            logging.debug(js)

            cate = js['result']['data']['cateList']
            months = js['result']['data']['contractMonth']

            return months[1:]
        except Exception as e:
            logging.info(e)

        time.sleep(pause)


def get_trading_expire_day(month='2018-04', retry=3, pause=1):
    """

    :param month: e.g. '2011-7'
    :param retry:
    :param pause:
    :return:
    """
    if month.index('-') != 4:
        raise Exception("Wrong month format:{0}.".fomrat(month))
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay"
    url = url + "?date=" + month
    logging.debug(url)
    for _ in range(retry):
        try:
            req = Request(url)
            res = urlopen(req, timeout=9).read()
            logging.debug(res)
            js = json.loads(res.decode('utf-8'))
            logging.debug(js)

            day = js['result']['data']['expireDay']
            return day
        except Exception as e:
            logging.info(e)

        time.sleep(pause)


def get_trading_option_list(option_code_10, retry=3, pause=1):
    """

    :param option_code_10: e.g. '5100501804'
    :param retry:
    :param pause:
    :return: DataFrame
    """
    if len(option_code_10) != 10:
        raise Exception("Wrong option code format:{0}.".format(option_code_10))
    url = "http://hq.sinajs.cn/list=OP_UP_{0},OP_DOWN_{1}".\
        format(option_code_10, option_code_10)
    logging.debug(url)
    df = pd.DataFrame(columns=columns)
    for t in range(retry):
        try:
            req = Request(url)
            res = urlopen(req, timeout=9).read()
            logging.debug(res)
            str = res.decode('utf-8')
            list = str.split('\n')
            str_up = list[0][list[0].index('"')+1:list[0].rindex('"')]
            str_down = list[1][list[1].index('"')+1:list[1].rindex('"')]
            logging.debug(str_up)
            logging.debug(str_down)
            str_up_down = str_up + str_down
            str_up_down = str_up_down[:-1]
            index = str_up_down.split(',')

            td_url = "http://hq.sinajs.cn/list={0}".format(str_up_down)
            logging.debug(td_url)
            td_req = Request(td_url)
            td_res = urlopen(td_req, timeout=9).read()
            logging.debug(td_res)
        except Exception as e:
            logging.info(e)
            logging.info("Try {0} times".format(t+1))
        else:
            str = td_res.decode('gbk')
            list = str.split('\n')
            for i in range(len(list)):
                if len(list[i]) < 20:
                    logging.debug("skip:list[{0}]:{1}".format(i, list[i]))
                    continue
                str_hq = list[i][list[i].index('"')+1:list[i].rindex('"')]
                list_detail = str_hq.split(',')
                if len(list_detail) != len(columns):
                    logging.error(columns)
                    logging.error(list_detail)
                    raise Exception("Option detail mismatch.")
                df.loc[i] = list_detail

            df.index = index
            logging.debug("\n{0}".format(df.head(5)))
            return df

        time.sleep(pause)
    return df

dbgFormatter = "%(levelname)s:%(filename)s:%(lineno)s %(funcName)s() %(message)s"
logging.basicConfig(level=logging.DEBUG, format=dbgFormatter)
df = get_trading_option_list('5100501804')
print(df.iloc[0])