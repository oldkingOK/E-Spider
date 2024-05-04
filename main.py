from espider import crawl, getContent
from dbhelper import insert_data, get_by_id
from tqdm import tqdm
from config import DB
import threading
import time, random

def replace_illegal_chars(path):
    "删除路径中的非法字符"
    illegal_chars = [':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars: path = path.replace(char, '_')
    return path

def fetch_and_write(id, name, path:str):
    """爬和存"""

    path = path + id + ".md"
    text = getContent(id)
    insert_data(path, name, text)


def main(from_dict: dict):
    print("正在爬取...")
    # 主页
    if len(get_by_id('index')) == 0:
        insert_data('/index.md', "知识库", getContent(1))

    # 原始目录树，用于查找文件
    m = crawl()

    for id, data in tqdm(from_dict.items()):
        if data["is_dir"] == "1": continue
        if from_dict and id not in from_dict:
            continue

        # 获取文件路径
        path = ""
        node_id = data["pid"]
        while node_id != "1":
            path = m[node_id]["name"] + "/" + path
            node_id = m[node_id]["pid"]
        path = "/" + path
        path = replace_illegal_chars(path) # 去除非法字符

        time.sleep(random.uniform(0.5, 1)) # 随机睡觉，避免触发反爬机制
        threading.Thread(target=fetch_and_write, args=(id, data["name"], path)).start()

    print(f"爬取完毕！存放在 {DB}")

def check() -> dict:
    print("正在获取爬取清单...")
    m = crawl()
    missing = {}
    for id, data in tqdm(m.items()):
        if data["is_dir"] == "1": continue
        if len(get_by_id(id)) == 0:
            missing[id] = data
    print(f"获取完毕！长度为 {len(missing.keys())}")
    return missing

if __name__ == '__main__':
    main(check())