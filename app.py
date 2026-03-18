from flask import Flask, request, render_template
import datetime
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    total = None
    man = None

    if request.method == "POST":
        try:
            yachin = int(request.form["yachin"])
            shikikin = int(request.form["shikikin"])
            reikin = int(request.form["reikin"])
            hoshou = float(request.form["hoshou"])
            mae = int(request.form["mae"])

            chukai_choice = request.form["chukai"]

            if chukai_choice == "1":
                chukai = yachin * 1.1
            elif chukai_choice == "2":
                chukai = yachin * 1.1 * 0.8
            elif chukai_choice == "3":
                chukai = yachin * 1.1 * 0.5
            else:
                chukai = 22000

            kagi = int(request.form["kagi"])
            shoudoku = int(request.form["shoudoku"])
            cleaning = int(request.form["cleaning"])
            hoken = int(request.form["hoken"])

            total = (
                yachin * mae +
                yachin * shikikin +
                yachin * reikin +
                yachin * (hoshou / 100) +
                chukai + kagi + shoudoku + cleaning + hoken
            )

            man = round(total / 10000, 1)

            with open("data.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.datetime.now()} | 合計:{total}円 | 手取り:{man}万円\n")

        except Exception as e:
            return f"エラー: {e}"

    return render_template("index.html", total=total, man=man)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)