from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

PAGE_RESULT = """
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

PAGE_404 = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 - Page not found</title>
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
    @media (prefers-color-scheme: light) {
        :root { --bg: #17181d; } /* keep the dark look everywhere */
    }
    html, body {
        height: 100%;
        margin: 0;
        background: #101114;
        color: var(--text);
        font-family: 'Rajdhani', 'Segoe UI', Arial, sans-serif;
    }
    body {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 16px;
        box-sizing: border-box;
    }
    .card {
        width: 100%;
        max-width: 520px;
        box-sizing: border-box;
        padding: 8px;
        background: var(--bg);
        border: 1px solid var(--line);
        border-radius: 12px;
    }
    .stats {
        display: flex;
        gap: 8px;
    }
    .stat {
        flex: 1;
        padding: 18px 0 14px;
        text-align: center;
        background: var(--tile);
        border-radius: 8px;
        border-bottom: 3px solid var(--c);
    }
    .value {
        font-size: 44px;
        font-weight: 700;
        line-height: 1;
        color: var(--c);
    }
    .label {
        margin-top: 4px;
        font-size: 17px;
        font-weight: 500;
        color: var(--muted);
        letter-spacing: 0.5px;
    }
    .message {
        padding: 24px 16px 20px;
        text-align: center;
    }
    h1 {
        margin: 0 0 6px;
        font-size: 30px;
        font-weight: 700;
    }
    p {
        margin: 0 0 20px;
        font-size: 19px;
        font-weight: 500;
        color: var(--muted);
    }
    a.btn {
        display: inline-block;
        padding: 9px 26px;
        font: 700 20px 'Rajdhani', 'Segoe UI', Arial, sans-serif;
        color: #0f1a13;
        background: var(--good);
        border-radius: 8px;
        text-decoration: none;
        transition: filter .15s;
    }
    a.btn:hover { filter: brightness(1.12); }
    a.btn:focus-visible { outline: 2px solid var(--text); outline-offset: 3px; }
</style>
</head>
<body>
    <main class="card">
        <div class="stats">
            <div class="stat" style="--c: var(--bad)">
                <div class="value">404</div>
                <div class="label">Error</div>
            </div>
            <div class="stat" style="--c: var(--mid)">
                <div class="value">0.0</div>
                <div class="label">Aim</div>
            </div>
            <div class="stat" style="--c: var(--bad)">
                <div class="value">0.0</div>
                <div class="label">K/D</div>
            </div>
        </div>
        <div class="message">
            <h1>Page not found</h1>
            <p>This page doesn't exist or has been moved.</p>
            <a class="btn" href="/">Back to home</a>
        </div>
    </main>
</body>
</html>
"""

@app.route("/")
def error():
    return render_template_string(PAGE_404)

@app.route("/<steam_id>")
def index(steam_id):
    return render_template_string(PAGE_RESULT, steam_id=steam_id)

@app.route("/api/<steam_id>")
def api(steam_id):
    URL = f"https://api.cs-prod.leetify.com/api/profile/{steam_id}/recent-games/5v5"
    r = requests.get(URL, timeout=10)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(debug=True)
