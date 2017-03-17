import tushare as ts
from db import mongoutil
from utils import constants,pubutils,pylog
import time
from services import hardenstock


# 获得当天的一字涨停板股票
def save_harden_stocks():
    conn = mongoutil.get_collection(constants.harden_stocks)

    flag,result = pubutils.exp_deal(ts.get_today_all())
    while not(flag):
        time.sleep(5)
        flag, result = pubutils.exp_deal(ts.get_today_all())

    conn.remove()

    for index, row in result.iterrows():
        if (pubutils.is_harden(row)):
            post={
                "stock":row['code'],
                "name":row['name'],
                "p_change":row['changepercent'],
                "date": constants.date_today
            }
            conn.insert(post)


if __name__ == "__main__":
    # save_harden_stocks()
    # df = ts.get_tick_data('603991','2017-03-16')
    #
    # df = df.sort_index(ascending=False)
    # print("\n",df)
    # hardenstock.price_trend(df)
    # df = df[0:-2]
    # print(df.iloc[-1]['pchange'])
    data = ts.get_today_all()
    ele = data.loc[data['code'] == '600753'].iloc[0]

    print("\n",str(ele['open']),str(ele['changepercent']))
