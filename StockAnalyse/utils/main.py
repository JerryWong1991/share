import requests

# 用于测试各个测试案列
if __name__ == "__main__":
    port_info = {}
    r = requests.post("http://127.0.0.1:5000/api/pre_harden",data=port_info)
    print(r.text)
