from fastapi import FastAPI, Request
import uvicorn
from azure.eventhub import EventHubProducerClient, EventData
import os
import json
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables from .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins → can restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your Azure Event Hub connection here
EVENT_HUB_CONN_STR = os.getenv("EVENT_HUB_CONN_STR")  # Use Railway Secret
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")          # Use Railway Secret

print("EVENT_HUB_CONN_STR:", repr(EVENT_HUB_CONN_STR))
print("EVENT_HUB_NAME:", repr(EVENT_HUB_NAME))


producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONN_STR,
    eventhub_name=EVENT_HUB_NAME
)

@app.post("/send-events")
async def send_events(request: Request):
    try:
        payload = await request.json()
        print("✅ Received payload:", payload)

        # Send to Azure Event Hub
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(json.dumps(payload)))
        producer.send_batch(event_data_batch)

        print("🚀 Sent to Azure Event Hub")
        return {"status": "success"}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "message": str(e)}

# For local testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
