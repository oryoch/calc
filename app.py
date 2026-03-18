from flask import Flask, request, render_template_string
import datetime
import os

app = Flask(__name__)

DATA_FILE = "data.txt"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>初期費用計算ツール</title>
    <style>
        body {
            font-family: Arial;
            max-width: 500px;
            margin: 40px auto;
        }

        h1 {
            text-align: center;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input {
            width: 100%;
            padding: 8px;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            padding: 10px;
            background: #f1f1f1;
        }

        .history {
            margin-top: 30px;
        }
    </style>
</head>

<body>

<h1>初期費用計算</h1>

<form method="POST">

    <div class="form-group">
        <label>顧客名</label>
        <input name="name">
    </div>

    <div class="form-group">
        <label>家賃</label>
        <input name="yachin">
    </div>

    <div class="form-group">
        <label>手取り（月収）</label>
        <input name="salary">
    </div>

    <button type="submit">計算</button>
</form>

{% if result %}
<div class="result">
    <p>初期費用：約 {{ result }} 円</p>
    <p>適正家賃：約 {{ rent }} 円</p>
</div>
{% endif %}

<div class="history">
    <h3>履歴</h3>
    {% for h in history %}
        <p>{{ h }}</p>
    {% endfor %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    rent = None

    try:
        if request.method == "POST":
            name = request.form.get("name", "名無し")
            yachin = int(request.form.get("yachin", 0))
            salary = int(request.form.get("salary", 0))

            # 初期費用（ざっくり5ヶ月分）
            result = yachin * 5

            # 適正家賃（手取りの1/3）
            rent = int(salary / 3)

            # 履歴保存
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            text = f"{now} | {name} | 初期費用:{result}円 | 適正家賃:{rent}円\\n"

            with open(DATA_FILE, "a", encoding="utf-8") as f:
                f.write(text)

    except Exception as e:
        return f"エラー: {e}"

    # 履歴読み込み
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            history = f.readlines()

    return render_template_string(HTML, result=result, rent=rent, history=history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)