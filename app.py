from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import os
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash
from cloud import BASE_FOLDER, safe_join

# Чтение переменных окружения
app_secret = os.environ.get("LCKT_APP_SECRET")
PASSWORD_HASH = os.environ.get("LCKT_PASSWORD_HASH")

if not app_secret or not PASSWORD_HASH:
    raise RuntimeError("Не найдены обязательные переменные окружения: LCKT_APP_SECRET или LCKT_PASSWORD_HASH")

app = Flask(__name__)
app.secret_key = app_secret
app.permanent_session_lifetime = timedelta(hours=1)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if "attempts" not in session:
        session["attempts"] = 0

    if request.method == "POST":
        if session["attempts"] >= 3:
            flash("Превышено количество попыток. Попробуйте позже.")
            return redirect(url_for("login"))

        password = request.form.get("password")
        if check_password_hash(PASSWORD_HASH, password):
            session["logged_in"] = True
            session.permanent = True
            session.pop("attempts", None)
            flash("Успешный вход")
            return redirect(url_for("browse"))
        else:
            session["attempts"] += 1
            flash(f"Неверный пароль. Попытка {session['attempts']} из 3.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Вы вышли из системы")
    return redirect(url_for("login"))


@app.route("/", defaults={"path": ""})
@app.route("/browse/<path:path>")
@login_required
def browse(path):
    fullpath = safe_join(BASE_FOLDER, path)
    if not os.path.exists(fullpath):
        return "Папка не найдена", 404
    dirs = sorted(
        [d for d in os.listdir(fullpath) if os.path.isdir(os.path.join(fullpath, d)) and d.isdigit()],
        key=lambda x: int(x),
        reverse=True
    )
    files = [f for f in os.listdir(fullpath) if os.path.isfile(os.path.join(fullpath, f))]
    return render_template("index.html", files=files, dirs=dirs, relpath=path, os=os)


@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if "file" not in request.files:
        flash("Файлы не выбраны!")
        return redirect(url_for("browse"))

    files = request.files.getlist("file")
    if not files or all(f.filename == "" for f in files):
        flash("Файлы не выбраны!")
        return redirect(url_for("browse"))

    now = datetime.now()
    subdir = os.path.join(str(now.year), str(now.month), str(now.day))
    save_dir = safe_join(BASE_FOLDER, subdir)
    os.makedirs(save_dir, exist_ok=True)

    for file in files:
        if file and file.filename:
            file.save(os.path.join(save_dir, file.filename))

    flash(f"Загружено файлов: {len(files)}")
    return redirect(url_for("browse", path=subdir))


@app.route("/download/<path:path>")
@login_required
def download_file(path):
    fullpath = safe_join(BASE_FOLDER, path)
    directory = os.path.dirname(fullpath)
    filename = os.path.basename(fullpath)
    return send_from_directory(directory, filename, as_attachment=False)


@app.route("/delete/<path:path>")
@login_required
def delete_file(path):
    fullpath = safe_join(BASE_FOLDER, path)
    if os.path.exists(fullpath):
        os.remove(fullpath)
        flash("Файл удалён.")
    parent = os.path.dirname(path)
    return redirect(url_for("browse", path=parent))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
