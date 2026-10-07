from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Widget Leetify</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #17181d;
        --tile: #202228;
        --line: #2e3038;
        --text: #f2f3f5;
        --muted: #8b8f9a;
        --good: #3ddc84;
        --mid: #f5c542;
        --bad: #ff5a5f;
    }
    html, body {
        margin: 0;
        background: transparent; /* transparent in OBS */
        font-family: 'Rajdhani', 'Segoe UI', Arial, sans-serif;
    }
    /* Set the OBS Browser Source to 520 x 110 */
    .widget {
        box-sizing: border-box;
        width: 520px;
        height: 110px;
        display: flex;
        gap: 8px;
        padding: 8px;
        background: var(--bg);
        border: 1px solid var(--line);
        border-color: grey;
    }
    .stat {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: var(--tile);
        border-radius: 8px;
        border-bottom: 3px solid var(--c, var(--muted));
    }
    .value {
        font-size: 44px;
        font-weight: 700;
        line-height: 1;
        color: var(--c, var(--text));
    }
    .value small {
        font-size: 20px;
        font-weight: 500;
        margin-left: 2px;
        color: var(--muted);
    }
    .label {
        margin-top: 4px;
        font-size: 17px;
        font-weight: 500;
        color: var(--muted);
        letter-spacing: 0.5px;
    }
</style>
</head>
<body>
    <div class="widget">
        <img src="https://leetify.com/assets/images/favicon.svg">
        <div class="stat" id="aim-box">
            <div class="value"><span id="aim">--</span></div>
            <div class="label">Aim</div>
        </div>
        <div class="stat" id="kd-box">
            <div class="value"><span id="kd">--</span></div>
            <div class="label">K/D</div>
        </div>
        <div class="stat" id="react-box">
            <div class="value"><span id="react">--</span><small>ms</small></div>
            <div class="label">Reaction</div>
        </div>
    </div>

    <script>
        const GOOD = 'var(--good)', MID = 'var(--mid)', BAD = 'var(--bad)';

        function setStat(id, text, color) {
            document.getElementById(id).textContent = text;
            document.getElementById(id + '-box').style.setProperty('--c', color);
        }

        async function update() {
            try {
                const data = await fetch('/api/{{ steam_id }}').then(r => r.json());
                const aim = Number(data.aimRating);
                const react = Number(data.reactionTime);
                const kd = Number(data.kdRatio);

                setStat('aim', String(aim).substr(0, 4), aim >= 75 ? GOOD : aim >= 50 ? MID : BAD);
                setStat('react', Math.round(react), react <= 550 ? GOOD : react <= 700 ? MID : BAD);
                setStat('kd', String(kd).substr(0, 4), kd >= 1.1 ? GOOD : kd >= 0.9 ? MID : BAD);
            } catch (e) {
                console.log(e);
            }
        }
        update();
        setInterval(update, 600000); // refresh every 60s
    </script>
</body>
</html>
"""

@app.route("/<steam_id>")
def index(steam_id):
    return render_template_string(PAGE, steam_id=steam_id)

@app.route("/api/<steam_id>")
def api(steam_id):
    URL = f"https://api.cs-prod.leetify.com/api/profile/{steam_id}/recent-games/5v5"
    r = requests.get(URL, timeout=10)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(debug=True)