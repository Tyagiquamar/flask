from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

LOG_FILE = "email_open_logs.txt"

@app.route('/pixel.png')
def tracking_pixel():
    """Tracks email opens by logging requests for a tracking pixel."""
    with open(LOG_FILE, "a") as f:
        f.write(f"Time: {datetime.datetime.now()} | IP: {request.remote_addr} | User-Agent: {request.headers.get('User-Agent')}\n")

    return send_file("static/pixel.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
