# MongoDB 各个 collection
import datetime


# 涨停股票涨幅最低值
harden_limit = 9.97
# 涨停板股票换手率不超过的值（百分值）
turnover_limt = 3
# 倒挂一字板收盘涨幅不低于的百分值
hook_pchange_limit = 7
# 高开低走的振幅要求
gkdz_limit = 0.01


#今天的日期
date_today = str(datetime.date.today())

# 涨停股票池
harden_stocks = "harden_stocks"
# 满足倒挂一字板的股票
harden_hook_stocks = "harden_hook"
# 当天满足倒钩的股票
hook_stocks = "hook_stocks"
