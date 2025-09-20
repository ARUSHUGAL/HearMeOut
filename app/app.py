import random
from flask import request, jsonify, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def pick_one(opts):
    return random.choice(opts)

def score_to_mood(compound):
    if compound >= 0.35: return "positive"
    if compound <= -0.35: return "negative"
    return "neutral"

TIPS = {
    "positive": ["Ok slay 😎🔥 keep that vibe.", "You’re cruising ✨ — share a win with a friend."],
    "neutral": ["Chill mode detected ✌️ — micro-break + water 🚰.", "Neutral vibes — jot one thing you’re grateful for."],
    "negative": ["You’re cooked 💀 — snack + stretch 5 mins.", "Low battery. Touch grass 🌱 or text a friend."]
}

MEMES = {
    "positive": ["/static/memes/you_got_this.jpg"],
    "neutral": ["/static/memes/keep_going.jpg"],
    "negative": ["/static/memes/hang_in_there.jpg"]
}

PLAYLISTS = {
    "positive": "https://open.spotify.com/playlist/37i9dQZF1DX1BzILRveYHv",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "negative": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"
}

def register_routes(app):
    @app.get("/")
    def home():
        return render_template("index.html")

    @app.post("/analyze")
    def analyze():
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        if not text:
            return jsonify({"error": "No transcript text provided."}), 400

        scores = analyzer.polarity_scores(text)
        mood = score_to_mood(scores["compound"])
        emoji = {"positive": "😎", "neutral": "🌈", "negative": "😭"}[mood]

        return jsonify({
            "transcript": text,
            "mood": mood,
            "emoji": emoji,
            "tip": pick_one(TIPS[mood]),
            "meme_url": pick_one(MEMES[mood]),
            "playlist_url": PLAYLISTS[mood],
            "confidence": round(scores["compound"], 3)
        })
