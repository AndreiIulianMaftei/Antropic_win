import os
from dotenv import load_dotenv
from bey import BeyondPresence

# Load environment variables from .env file
load_dotenv()

client = BeyondPresence(
    api_key=os.environ.get("BEY_API_KEY"),  # This is the default and can be omitted
)

session = client.session.create(
    avatar_id="01234567-89ab-cdef-0123-456789abcdef",
    livekit_token="<your-livekit-token>",
    livekit_url="wss://<your-domain>.livekit.cloud",
)
print(session.id)