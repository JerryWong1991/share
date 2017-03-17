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

    try:
        result = hardenstock.get_pre_harden()
    except Exception as e:
        pylog.log.exception("读取前一日涨停数据时出现异常：")
        result = None
    finally:
        resp = make_response(jsonify({"data": result}))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


if __name__ == "__main__":
    app.run()