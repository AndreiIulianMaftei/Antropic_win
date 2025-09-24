import os
from dotenv import load_dotenv
from bey import BeyondPresence

# Load environment variables from .env file
load_dotenv()

client = BeyondPresence(
    api_key=os.environ.get("BEY_API_KEY"),  # This is the default and can be omitted
)

session = client.session.create(
    avatar_id="b105a197-a3e9-4c8d-92d7-ccd53b5f5e8f",
    livekit_token="<your-livekit-token>",
    livekit_url="wss://<your-domain>.livekit.cloud",
)
print(session.id)