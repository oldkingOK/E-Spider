from espider import crawl, getContent
from dbhelper import insert_data
import threading
import time, random

def replace_illegal_chars(path):
    "删除路径中的非法字符"
    illegal_chars = [':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars: path = path.replace(char, '_')
    return path


count = 0
length = 0

def fetch_and_write(id, name, path:str):
    """爬和存"""
    global count

    path = path + id + ".md"
    text = getContent(id)
    insert_data(path, name, text)

    count += 1
    print(f"\rDone {count} of {length}")


if __name__ == '__main__':
    # 主页
    insert_data(f'/index.md', "知识库", getContent(1))

    # 内容
    m = crawl()
    length = len([data for data in m.values() if data["is_dir"] == "0"])

    for id, data in m.items():
        if data["is_dir"] == "1": continue

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

    print("All Done!")