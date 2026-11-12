# FB Poster

Small Flask app to publish (or schedule) posts to a Facebook **Page** via the Graph API. Supports text, link, and image.

## Setup
1. Create an app at developers.facebook.com and get a **Page Access Token** with `pages_manage_posts` and `pages_read_engagement` (use a long-lived token).
2. `cp .env.example .env` and fill in `FB_PAGE_ID` and `FB_PAGE_ACCESS_TOKEN`.
3. `pip install -r requirements.txt`
4. `python app.py` then open http://localhost:5000

## Notes
- The Graph API only allows posting to Pages, not personal profiles.
- Scheduled posts must be 10 minutes to 6 months in the future.
- Never commit `.env`.
