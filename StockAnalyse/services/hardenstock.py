# 跟涨停相关的指标
import pylab
from db import mongoutil
from utils import constants
import tushare as ts


############################# 计算类方法区 ##########################

# 绘图-股价和分时均价走势图
def price_trend(data):
    price_vec = data['price'].tolist()
    volume_vec = data['volume'].tolist()
    amount_vec = data['amount'].tolist()

    avg_price = []
    avg_price.append(price_vec[0])

    for i in range(1,len(volume_vec)):
        volume_vec[i] = volume_vec[i] + volume_vec[i-1]
        amount_vec[i] = amount_vec[i] + amount_vec[i-1]
        avg_price.append(amount_vec[i] / ((volume_vec[i] * 100)))

    pylab.figure(1)
    x = range(len(price_vec))

    pylab.plot(x, price_vec, "b")
    pylab.plot(x, avg_price, 'y')
    pylab.show()

    return price_vec,avg_price

# 计算符合倒挂一字板的标的
def cal_harden_hook():
    harhoo_conn = mongoutil.get_collection(constants.harden_hook_stocks)
    hoo_conn = mongoutil.get_collection(constants.hook_stocks)
    daily_result = ts.get_today_all()
    pre_harden_stocks = get_harden_codes()

    harhoo_conn.remove()
    hoo_conn.remove()

    for i in range(0,len(daily_result)):
        # stock = daily_result.loc[daily_result['code'] == pre_harden_stocks[i]].iloc[0]
        stock = daily_result.iloc[i]
        if (stock['open']>=stock['settlement'] and stock['changepercent'] >= constants.hook_pchange_limit \
            and (stock['open']-stock['low'])/stock['open']>=constants.gkdz_limit):
            post={
                "stock":stock['code'],
                "name":stock['name'],
                "p_change":stock['changepercent'],
                "date":constants.date_today
            }
            hoo_conn.insert(post)
            if(stock['code'] in pre_harden_stocks):
                harhoo_conn.insert(post)


############################# 读取数据类方法区 ##########################

# 获得前一日涨停板股票代码列表
def get_harden_codes():
    conn = mongoutil.get_collection(constants.harden_stocks)
    stocks = []
    result = conn.find()
    for ele in result:
        stocks.append(ele['stock'])
    return stocks

# 获得前一日涨停板股票实体列表
def get_pre_harden():
    return get_harden_relate_data(constants.harden_stocks)

# 获得当天走势符合倒钩形态的股票
def get_today_hook():
    return get_harden_relate_data(constants.hook_stocks)

# 获得当天收盘后符合一字板倒钩的股票
def get_harden_hook():
    return get_harden_relate_data(constants.harden_hook_stocks)


# 获取涨停相关股票由于业务一致，复用一个函数
def get_harden_relate_data(target):
    result = []
    conn = mongoutil.get_collection(target)
    data = conn.find()
    for ele in data:
        record = [ele['stock'], ele['name'], ele['p_change'], ele['date']]
        result.append(record)
    return result



if __name__ == "__main__":
    cal_harden_hook()