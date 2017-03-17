# 公用的工具方法
from utils import pylog,constants

# 统一处理访问外网数据出现网络异常的方法
def exp_deal(method):
    try:
        result = method
        return True,result
    except Exception as e:
        pylog.log.exception("拉数据出现异常：")
        return False,None


# 判断一字涨停
def is_harden(row):
    if(row['high']==row['low'] and row['changepercent']>= constants.harden_limit \
        and row['turnoverratio']< constants.turnover_limt ):
        return True
    else:
        return False