import os
import json
from dotenv import load_dotenv
import pandas as pd
import time
import pytz
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.events_api import EventsApi

# Load DataDog API Keys
if not load_dotenv():
    raise EnvironmentError("Unable to load .env file. Make sure it exists and contains the required keys.")

DD_API_KEY = os.getenv('DD_API_KEY')
DD_APP_KEY = os.getenv('DD_APP_KEY')

if not DD_API_KEY or not DD_APP_KEY:
    raise ValueError("Datadog API Key or App Key is missing in the .env file.")

# Configure API client
configuration = Configuration()
configuration.api_key["apiKeyAuth"] = DD_API_KEY
configuration.api_key["appKeyAuth"] = DD_APP_KEY

# Initialize API client
with ApiClient(configuration) as api_client:
    events_api = EventsApi(api_client)

    # Define time range (last 24 hours)
    start_time = int(time.time()) - (86400 * 30)  # 30 days ago
    end_time = int(time.time())
    
    try:
        # Fetch events
        events_response = events_api.list_events(
            filter_from=str(start_time),
            filter_to=str(end_time),
            filter_query="TRMS",
            page_limit=1000
        )
        
        # Extract events
        events_data = []
        if events_response.data:
            for event in events_response.data:
                attributes = event.attributes.attributes
                event_timestamp = event.attributes.timestamp
                target_timezone = pytz.timezone("Asia/Manila")
                event_timestamp_local = event_timestamp.astimezone(target_timezone)

                events_data.append({
                    "event_id": event.id,
                    "event_type": event.type,
                    "event_tags": ", ".join(event.attributes.tags) if event.attributes.tags else "",
                    "event_timestamp_local": event_timestamp_local.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_title": attributes.get("title", "No Title"),
                    "event_status": attributes.get("status", "Unknown")
                })
            
            # Convert to DataFrame
            events_df = pd.DataFrame(events_data)
            print(events_df)
            
            # Write to CSV
            output_file = 'events_output.csv'
            events_df.to_csv(output_file, index=False)
            print(f"Events successfully written to {output_file}.")
        else:
            print(f"No events found between {start_time} and {end_time}.")
            
    except Exception as e:
        print(f"Error fetching events: {e}")
