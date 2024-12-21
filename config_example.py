# Immich
INSTANCE = "https://immich.your.domain.tld"  # Your Immich instance (required)
TOKEN = ""  # Immich api token (required)

TAG_PREFIX = "AI_"  # Prefix for album names (required)

# Connection
CLIENT_CERT = ""  # A client certificate for mTLS (optional)
CLIENT_KEY = ""  # Client key for mTLS (optional)

# AI
MODEL = ''  # Vision model to use. Must be a loaded model in ollama (required)

# Categories to classify the images into
ALL_TAGS = ["Holiday", "Meme", "Screenshot", "People", "Food and Drinks", "Animals",
            "Tech", "Nature/Landscape", "Other", "Interior", "Document", "Receipt/Invoice", "Event", "Product"]

# Amount of scaling that should be applied to the pictures before passing to the model.
SCALE = 0.7

MAX_INFERENCE_RETRIES = 5
