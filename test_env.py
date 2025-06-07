import os

print("EVENT_HUB_CONN_STR =", repr(os.getenv("EVENT_HUB_CONN_STR")))
print("EVENT_HUB_NAME =", repr(os.getenv("EVENT_HUB_NAME")))

print("🚩 Printing all environment variables:")
for k, v in os.environ.items():
    print(f"{k}={v}")

