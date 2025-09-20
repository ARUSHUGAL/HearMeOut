import random
from flask import request, jsonify, render_template
from transformers import pipeline

# Hugging Face sentiment pipeline (baseline: positive/negative/neutral)
sentiment_model = pipeline("sentiment-analysis")


def pick_one(opts):
    return random.choice(opts)


# Expanded vibes dictionary — you can keep adding!
TIPS = {
    "positive": [
        "Ok slay 😎🔥 keep that vibe.",
        "You’re cruising ✨ — share a win with a friend.",
        "Celebrate a small W today 🎉.",
        "Dance break time 💃🕺.",
        "Bottle this energy for later ⚡️.",
        "Treat yourself, you earned it 🍦.",
        "Post a silly selfie 🤳.",
        "Laugh at a meme — dopamine hit 🤣."
    ],
    "neutral": [
        "Chill mode detected ✌️ — micro-break + water 🚰.",
        "Neutral vibes — jot one thing you’re grateful for.",
        "Pause and stretch 🧘.",
        "Stand up, shake it out 🕺.",
        "Hydrate like it’s your job 💧.",
        "Organize your desk 🗂️.",
        "Step outside for sunlight ☀️.",
        "Queue up a calm playlist 🎶."
    ],
    "negative": [
        "You’re cooked 💀 — snack + stretch 5 mins.",
        "Low battery. Touch grass 🌱 or text a friend.",
        "Step away, breathe deeply 🌬️.",
        "Cry if you need to — release is healing 😢.",
        "Take a cold splash on face 💦.",
        "Journal your anger 🔥.",
        "Queue your comfort show 📺.",
        "Wrap yourself in a blanket 🥶."
    ],
    "horny": [
        "Text your crush something cheeky 😏.",
        "Hydrate before you slide into DMs 💦.",
        "Playlist: slow jams only 🎶.",
        "Maybe… touch grass 🌱 before sending that risky text."
    ],
    "anxious": [
        "Box breathing 4-4-4-4 🌬️.",
        "Ground yourself: 5 things you see, 4 touch, 3 hear 👀🤲👂.",
        "Remind yourself: feelings ≠ facts.",
        "Stretch your hands, release the jitters 🖐️."
    ],
    "bored": [
        "Try a random Wikipedia rabbit hole 📚.",
        "Doodle something weird ✏️.",
        "Queue up a podcast 🎙️.",
        "Send a meme to a friend 😂."
    ],
    "tired": [
        "Drink some water 💧.",
        "Lie down for 10 mins 🛏️.",
        "Do a quick stretch 🧘.",
        "Queue up chill lo-fi 🎶."
    ],
    "stressed": [
        "Make a mini to-do list ✅.",
        "Step away for 5 mins ⏱️.",
        "Listen to white noise 🌊.",
        "Remind yourself: you’re doing your best 💌."
    ]
}

# fallback memes (you can expand these too)
MEMES = {
    "positive": ["/static/memes/you_got_this.jpg"],
    "neutral": ["/static/memes/keep_going.jpg"],
    "negative": ["/static/memes/hang_in_there.jpg"]
}

# fallback playlists
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

        # Hugging Face result
        result = sentiment_model(text)[0]
        label = result["label"]  # "POSITIVE" or "NEGATIVE"
        confidence = float(result["score"])

        # map Hugging Face labels to your vibes
        if label == "POSITIVE":
            mood = "positive"
        elif label == "NEGATIVE":
            mood = "negative"
        else:
            mood = "neutral"

        # 🔥 add keyword-based custom vibes (hacky but fun)
        lowered = text.lower()
        if any(word in lowered for word in ["horny", "thirsty", "down bad"]):
            mood = "horny"
        elif any(word in lowered for word in ["anxious", "worried", "panic"]):
            mood = "anxious"
        elif any(word in lowered for word in ["bored", "meh", "whatever"]):
            mood = "bored"
        elif any(word in lowered for word in ["tired", "sleepy", "exhausted"]):
            mood = "tired"
        elif any(word in lowered for word in ["stress", "overwhelmed"]):
            mood = "stressed"

        emoji = {
            "positive": "😎",
            "neutral": "🌈",
            "negative": "😭",
            "horny": "😏",
            "anxious": "😰",
            "bored": "🥱",
            "tired": "😴",
            "stressed": "😵"
        }.get(mood, "🌈")  # fallback emoji

        return jsonify({
            "transcript": text,
            "mood": mood,
            "emoji": emoji,
            "tip": pick_one(TIPS.get(mood, TIPS["neutral"])),
            "meme_url": pick_one(MEMES.get(mood, MEMES["neutral"])),
            "playlist_url": PLAYLISTS.get(mood, PLAYLISTS["neutral"]),
            "confidence": round(confidence, 3)
        })