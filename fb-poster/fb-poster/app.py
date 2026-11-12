import os
from datetime import datetime
import requests
from flask import Flask, request, render_template_string, flash
from dotenv import load_dotenv

load_dotenv()
PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
API = "https://graph.facebook.com/v21.0"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me")

HTML = """
<!doctype html><title>FB Poster</title>
<style>
body{font-family:system-ui;max-width:560px;margin:40px auto;padding:0 16px}
textarea,input{width:100%;padding:8px;margin:6px 0 14px;box-sizing:border-box}
button{padding:10px 18px;background:#1877f2;color:#fff;border:0;border-radius:6px;cursor:pointer}
.msg{padding:10px;border-radius:6px;margin-bottom:12px;background:#eef}
</style>
<h2>Post to Facebook Page</h2>
{% for m in get_flashed_messages() %}<div class="msg">{{ m }}</div>{% endfor %}
<form method="post" action="/post" enctype="multipart/form-data">
  <label>Message</label><textarea name="message" rows="5" required></textarea>
  <label>Link (optional)</label><input name="link" type="url">
  <label>Image (optional)</label><input name="image" type="file" accept="image/*">
  <label>Schedule for (optional, leave blank to post now)</label>
  <input name="schedule" type="datetime-local">
  <button>Send post</button>
</form>
"""

def publish(message, link=None, image=None, schedule=None):
    data = {"access_token": TOKEN}
    if schedule:
        ts = int(datetime.fromisoformat(schedule).timestamp())
        data.update(published="false", scheduled_publish_time=ts)
    if image:
        data["caption"] = message
        r = requests.post(f"{API}/{PAGE_ID}/photos", data=data,
                          files={"source": (image.filename, image.stream, image.mimetype)})
    else:
        data["message"] = message
        if link:
            data["link"] = link
        r = requests.post(f"{API}/{PAGE_ID}/feed", data=data)
    return r.json()

@app.get("/")
def index():
    return render_template_string(HTML)

@app.post("/post")
def post():
    if not PAGE_ID or not TOKEN:
        flash("Set FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN in .env first.")
        return render_template_string(HTML)
    f = request.form
    img = request.files.get("image")
    res = publish(f["message"], f.get("link") or None,
                  img if img and img.filename else None,
                  f.get("schedule") or None)
    if "error" in res:
        flash("Error: " + res["error"].get("message", str(res)))
    else:
        flash("Success! Post ID: " + str(res.get("id") or res.get("post_id")))
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
