from flask import Flask, request, send_file, make_response
import datetime
import os
from PIL import Image

app = Flask(__name__)

LOG_FILE = "email_open_logs.txt"
PIXEL_FILE = "pixel.png"

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Email Open Log Initialized\n")

# Ensure a 1x1 transparent pixel exists
if not os.path.exists(PIXEL_FILE):
    img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    img.save(PIXEL_FILE)

@app.route('/')
def home():
    return "Tracking Pixel is running!", 200

@app.route('/pixel.png')
def tracking_pixel():
    """Logs email open event and returns a tracking pixel."""
    log_entry = f"Time: {datetime.datetime.now()} | IP: {request.remote_addr} | User-Agent: {request.headers.get('User-Agent')}\n"

    # Write log entry
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    # Send tracking pixel with cache prevention headers
    response = make_response(send_file(PIXEL_FILE, mimetype="image/png"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
