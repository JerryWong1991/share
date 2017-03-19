from flask import *
from services import hardenstock
from utils import pylog


app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# 获得前一交易日的一字涨停股
@app.route('/api/pre_harden', methods=['GET'])
def get_pre_harden():
    return pub_response(hardenstock.get_pre_harden())


# 获得当天符合倒钩的股票
@app.route('/api/hook_today', methods=['GET'])
def get_hook_stocks():
    return pub_response(hardenstock.get_today_hook())

# 获得前一天一字板，当天又倒钩的股票
@app.route('/api/harden_hook', methods=['GET'])
def get_harden_hook():
    return pub_response(hardenstock.get_harden_hook())


# 公用的封装返回函数
def pub_response(method):
    try:
        result = method
    except Exception as e:
        pylog.log.exception("读取目标标的数据时出现异常：")
        result = None
    finally:
        resp = make_response(jsonify({"data": result}))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


if __name__ == "__main__":
    app.run()