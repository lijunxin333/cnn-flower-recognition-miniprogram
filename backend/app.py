# 相当于服务器
from flask import Flask, request, jsonify
import os
import uuid
import sys
import sqlite3

# 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(PROJECT_ROOT)
DB_PATH = os.path.join(BASE_DIR, "flowers.db")

from ai_model.predict import load_model, predict_flower


# 应用实例
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 模型加载
print("Loading model...")
model = load_model()
print("Model loaded!")

# 1.1函数——连接数据库
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1.2函数——允许上传的文件类型
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return "Flower Recognition API Running"

"""
一.用户相关
   1.用户注册
"""
@app.route("/user/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"code": 1, "msg": "参数不完整"})

    if len(password) < 6:
        return jsonify({"code": 1, "msg": "密码至少6位"})

    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return jsonify({"code": 0, "msg": "注册成功"})
    except sqlite3.IntegrityError:
        return jsonify({"code": 1, "msg": "用户名已存在"})
    finally:
        conn.close()

"""
一.用户相关
   2.用户登录
"""
@app.route("/user/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"code": 1, "msg": "参数不完整"})

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM user WHERE username=?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({"code": 1, "msg": "用户不存在"})

    user_id, db_password = result

    if password != db_password:
        return jsonify({"code": 1, "msg": "密码错误"})

    return jsonify({
        "code": 0,
        "msg": "登录成功",
        "data": {
            "user_id": user_id,
            "username": username
        }
    })


"""
二.花卉识别
   1.调用ai模型
"""
@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    parts = file.filename.rsplit(".", 1)
    ext = parts[1].lower() if len(parts) == 2 else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print(f"[INFO] File saved: {filepath}")
    print("Received image:", file.filename)

    try:
        result = predict_flower(filepath, model)
        print("Prediction:", result["names"][0])
        flower_id = int(result["classes"][0])

        conn = get_conn()
        cursor = conn.cursor()

        flower = cursor.execute(
            "SELECT * FROM flower WHERE id=?",
            (flower_id,)
        ).fetchone()
        conn.close()

        return jsonify({
    "success": True,
    "data": {
        "top1": {
            "id": flower["id"],
            "name": flower["name"],
            "prob": float(result["probs"][0]),
            "image": flower["image_path"]
        },
        "top3": [
            {
                "id": int(c),
                "name": n,
                "prob": float(p)
            }
            for c, n, p in zip(
                result["classes"][:3],
                result["names"][:3],
                result["probs"][:3]
            )
        ]
    }
}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # 删除临时下载的文件，防止过载
    finally:
        try:
           if os.path.exists(filepath):
              os.remove(filepath)
        except Exception as e:
            print("File cleanup failed:", e)


"""
三.花卉收藏相关
   1.添加收藏
"""
@app.route("/favorite/add", methods=["POST"])
def favorite_add():
    data = request.json
    user_id = data.get("user_id")
    flower_id = data.get("flower_id")

    if not user_id or not flower_id:
        return jsonify({"code": 1, "msg": "missing params"}), 400

    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO favorite (user_id, flower_id)
            VALUES (?, ?)
        """, (user_id, flower_id))

        conn.commit()
        msg = "ok"

    except:
        msg = "exists"

    conn.close()

    return jsonify({"code": 0, "msg": msg})

"""
三.花卉收藏相关
   2.展示收藏花卉列表
"""
@app.route("/favorite/list", methods=["GET"])
def favorite_list():
    user_id = request.args.get("user_id")

    conn = get_conn()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT f.id, f.name, f.image_path
        FROM flower f
        JOIN favorite fav ON f.id = fav.flower_id
        WHERE fav.user_id=?
    """, (user_id,)).fetchall()

    conn.close()

    return jsonify({
        "code": 0,
        "data": [dict(r) for r in rows]
    })

"""
三.花卉收藏相关
   3.删除收藏
"""
@app.route("/favorite/delete", methods=["POST"])
def favorite_delete():
    data = request.json
    user_id = data.get("user_id")
    flower_id = data.get("flower_id")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM favorite WHERE user_id=? AND flower_id=?",
        (user_id, flower_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"code": 0, "msg": "ok"})


"""
四.花卉详细
   1.展示详情
"""
# 4.花卉详情接口
@app.route("/flower/detail", methods=["GET"])
def flower_detail():
    flower_id = request.args.get("id")

    conn = get_conn()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM flower WHERE id=?",
        (flower_id,)
    ).fetchone()

    conn.close()

    if not row:
        return jsonify({"code": 1, "msg": "not found"})

    return jsonify({
        "code": 0,
        "data": dict(row)
    })


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)