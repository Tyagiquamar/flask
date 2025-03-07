from flask import Flask, request, send_file, make_response
import datetime
import os

app = Flask(__name__)

LOG_FILE = "email_open_logs.txt"
PIXEL_FILE = "pixel.png"

# Create a 1x1 transparent pixel if missing
if not os.path.exists(PIXEL_FILE):
    from PIL import Image
    img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    img.save(PIXEL_FILE)

@app.route('/')
def home():
    return "Tracking Pixel is running!", 200

@app.route('/pixel.png')
def tracking_pixel():
    """Logs email open event and returns a tracking pixel."""
    log_entry = f"Time: {datetime.datetime.now()} | IP: {request.remote_addr} | User-Agent: {request.headers.get('User-Agent')}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    response = make_response(send_file(PIXEL_FILE, mimetype="image/png"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
