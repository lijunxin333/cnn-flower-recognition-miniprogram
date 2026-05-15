import sqlite3

# 连接数据库（替换成你的数据库路径）
conn = sqlite3.connect("./backend/flowers.db")
cursor = conn.cursor()

# 方式1：按ID删除
user_id_to_delete = 9
cursor.execute("DELETE FROM user WHERE id = ?", (user_id_to_delete,))
conn.commit()
print("all done!")