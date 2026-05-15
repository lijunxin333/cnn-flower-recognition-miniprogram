# init_db.py 初始化数据库
import sqlite3

conn = sqlite3.connect("./backend/flowers.db")
cursor = conn.cursor()

# 创建表
# 用户表
cursor.execute("""
create table if not exists user (
  id integer primary key autoincrement,
  username text unique not null,
  password text not null
)
""")

# 花卉表
cursor.execute("""
create table if not exists flower (
  id integer primary key autoincrement,
  name text,
  image_path text,                   --存储花卉路径
  description text default '待补充',  --中文字，介绍啥的
  language text default '待补充',     --花语
  light text default '待补充',
  water text default '待补充',
  soil text default '待补充'
)
""")

# 收藏表
cursor.execute("""
create table if not exists favorite (
  id integer primary key autoincrement,
  user_id integer,                             --标记微信用户
  flower_id integer,                         -- 花卉ID
  unique(user_id, flower_id)               -- 业务唯一（不重复收藏）
)
""")

conn.commit()
conn.close()

print("all done!")