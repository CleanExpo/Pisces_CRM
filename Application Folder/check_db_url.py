import os

db_url = os.environ.get("DATABASE_URL")
if db_url:
    print("DATABASE_URL is set")
    # Print only the type of database and host
    parts = db_url.split("://")
    if len(parts) > 1:
        db_type = parts[0]
        host = parts[1].split("@")[-1].split("/")[0]
        print(f"Database type: {db_type}")
        print(f"Host: {host}")
    else:
        print("DATABASE_URL format is unexpected")
else:
    print("DATABASE_URL is not set")

openai_api_key = os.environ.get("OPENAI_API_KEY")
if openai_api_key:
    print("OPENAI_API_KEY is set")
else:
    print("OPENAI_API_KEY is not set")
