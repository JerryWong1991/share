# 从外网数据源获得相关的行情数据
from pymongo import MongoClient
from utils import constants

client = MongoClient("192.250.110.33", 27017)
db = client.stock_analyse

# 获得相关collection连接的工厂类
# 相关的collection名在constants中配置
def get_collection(name):
    return db[name]


def get_harden_stocks():
    conn = get_collection(constants.harden_stocks)
    stocks = []
    result = conn.find()
    for ele in result:
        stocks.append(ele['stock'])
    return stocks

if __name__ == "__main__":
    print(get_harden_stocks())

