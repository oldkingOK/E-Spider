from sqlite_worker import SqliteWorker
from config import DB
import atexit

worker = SqliteWorker(DB)

def get_all():
    for row in worker.execute("SELECT * FROM ebook"):
        yield row

def create_table():
    sql = 'CREATE TABLE ebook (Path TEXT, Name TEXT, Text TEXT);'
    worker.execute(sql)

def has_table():
    sql_text = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{'ebook'}'"
    r = worker.execute(sql_text)
    return len(r) > 0

query = "INSERT INTO ebook (Path, Name, Text) VALUES (?,?,?)"

def insert_data(path, name, text):
    """安全的插入数据"""
    worker.execute(query, (path, name, text))

def get_by_id(id: str):
    sql = f"SELECT Path, Name, Text FROM ebook WHERE Path LIKE '%/{id}.html';"
    return worker.execute(sql)

if not has_table(): create_table()
atexit.register(worker.close)

if __name__ == "__main__":
    insert_data("HelloWorld", "Dmasdnasdasd")