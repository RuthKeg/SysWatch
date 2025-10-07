from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import psutil, datetime, json, os
from functools import wraps

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "change_this_secret_for_prod"

USERS_FILE = "users.json"
SETTINGS_FILE = "settings.json"

# ----------------- Helpers -----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        # example default
        with open(USERS_FILE, "w") as f:
            json.dump({"ruth":"password123"}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def load_settings():
    default = {"show_cpu": True, "show_ram": True, "show_disk": True}
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(default, f, indent=2)
        return default
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_stats():
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpu = psutil.cpu_percent(interval=0.5)
    return {
        "cpu": round(cpu,1),
        "ram_total": round(vm.total / (1024**3), 2),
        "ram_used": round((vm.total - vm.available) / (1024**3), 2),
        "ram_percent": vm.percent,
        "disk_total": round(disk.total / (1024**3), 2),
        "disk_used": round(disk.used / (1024**3), 2),
        "disk_percent": disk.percent,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }

# ----------------- Auth -----------------
USERS = load_users()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            flash("Connectez-vous pour accéder au dashboard", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        if username in USERS and USERS[username] == password:
            session["username"] = username
            flash(f"Bienvenue {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Identifiant ou mot de passe incorrect", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

# ----------------- Routes -----------------
@app.route("/")
@login_required
def dashboard():
    prefs = load_settings()
    return render_template("dashboard.html", prefs=prefs)

# Protected stats API (used by dashboard JS)
@app.route("/api/stats")
@login_required
def api_stats():
    return jsonify(get_stats())

# Local stats API for desktop Tkinter (no login) - only allow localhost
@app.route("/api/stats_local")
def api_stats_local():
    # Permit only local requests
    remote = request.remote_addr
    if remote not in ("127.0.0.1", "::1", "localhost"):
        return jsonify({"error":"Forbidden"}), 403
    return jsonify(get_stats())

@app.route("/settings", methods=["GET","POST"])
@login_required
def settings():
    if request.method == "POST":
        prefs = {
            "show_cpu": bool(request.form.get("cpu")),
            "show_ram": bool(request.form.get("ram")),
            "show_disk": bool(request.form.get("disk"))
        }
        save_settings(prefs)
        flash("Préférences enregistrées.", "success")
        return redirect(url_for("dashboard"))
    prefs = load_settings()
    return render_template("settings.html", prefs=prefs)

if __name__ == "__main__":
    app.run(debug=True)
