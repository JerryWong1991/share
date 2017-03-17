# 跟涨停相关的指标
import pylab
from db import mongoutil
from utils import constants
import tushare as ts

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
    conn = mongoutil.get_collection(constants.harden_hook_stocks)
    daily_result = ts.get_today_all()
    pre_harden_stocks = mongoutil.get_harden_codes()
    # pre_harden_stocks = ['600753','601375','603603']

    for i in range(0,len(pre_harden_stocks)):
        stock = daily_result.loc[daily_result['code'] == pre_harden_stocks[i]].iloc[0]
        # stock = daily_result.iloc[i]
        if (stock['open']>=stock['settlement'] and stock['changepercent'] >= constants.hook_pchange_limit \
            and (stock['open']-stock['low'])/stock['open']>=constants.gkdz_limit):
            post={
                "stock":stock['code'],
                "name":stock['name'],
                "p_change":stock['changepercent'],
                "date":constants.date_today
            }
            conn.insert(post)


def get_pre_harden():
    result = []
    conn = mongoutil.get_collection(constants.harden_stocks)
    data = conn.find()
    for ele in data:
        record = [ele['stock'],ele['name'],str(ele['p_change']),ele['date']]
        result.append(record)
    return result

if __name__ == "__main__":
    print(get_pre_harden())