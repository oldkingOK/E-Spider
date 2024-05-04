from requests import get
from config import URL
import urllib3
import json

# 懒得配置证书，直接关闭警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getData(deep) -> dict:
    """
    get到的信息的data节点 结构如下
    {
        "41234": {
            "id": "41234",      // 当前id
            "pid": "1",         // 父节点的id
            "name": "README",   // 文件名
            "is_dir": "0",
            "deep": "2",
            "search": "1"
        },
        "41236": {
            "id": "41236",
            "pid": "1",
            "name": "软件下载",
            "is_dir": "1",
            "deep": "2",
            "search": "1"
        }
    }
    """
    # 深度从1 ~ 8
    param = {
        'id': 'eknow',
        'mod': 'index',
        'ac': 'getMatchData',
        'deep': deep
    }
    response = get(URL,verify=False,params=param)
    return json.loads(response.text)["data"]

def getContent(id) -> str:
    """获取节点对应的html信息"""

    param = {
        'id': 'eknow',
        'mod': 'index',
        'ac': 'getdata',
        'aid': id
    }

    response = get(URL, verify=False,params=param)
    return json.loads(response.text)["html"]

def crawl() -> dict:
    """爬取所有节点"""
    m = {}
    for i in range(1, 9):
        m = {**m, **getData(i)}
    return m

if __name__ == '__main__':
    print(getData(1))
