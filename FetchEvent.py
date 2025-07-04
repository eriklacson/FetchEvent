#!/usr/bin/python3

import os
import json
from dotenv import load_dotenv
import pandas as pd
import argparse
import time
import pytz
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.events_api import EventsApi

def initialize_config():
    """
    Sets up configurations, API keys, and Datadog API client.
    """
    if not load_dotenv():
        raise EnvironmentError("Unable to load .env file. Make sure it exists and contains the required keys.")

    DD_API_KEY = os.getenv('DD_API_KEY')
    DD_APP_KEY = os.getenv('DD_APP_KEY')

    if not DD_API_KEY or not DD_APP_KEY:
        raise ValueError("Datadog API Key or App Key is missing in the .env file.")

    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = DD_API_KEY
    configuration.api_key["appKeyAuth"] = DD_APP_KEY

    return configuration

def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Fetch events from Datadog API.")
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="The filter query for fetching events, e.g., 'service:trms production service check'."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days in the past to fetch events (default: 30)."    
    )
    return parser.parse_args()

def fetch_event_data(events_api, query, days):
    """
    Fetches event data from Datadog API.
    """
    start_time = int(time.time()) - (86400 * days)  # X days ago
    end_time = int(time.time())

    try:
        events_response = events_api.list_events(
            filter_from=str(start_time),
            filter_to=str(end_time),
            filter_query=query, 
            page_limit=1000
        )
        return events_response.data if events_response.data else []
    except Exception as e:
        handle_errors(f"Error fetching events: {e}")
        return []

def process_event_data(events_data):
    """
    Processes and transforms the fetched event data.
    """
    processed_events = []
    target_timezone = pytz.timezone("Asia/Manila")

    for event in events_data:
        attributes = event.attributes.attributes
        event_timestamp = event.attributes.timestamp
        event_timestamp_local = event_timestamp.astimezone(target_timezone)

        processed_events.append({
            "event_id": event.id,
            "event_type": event.type,
            "event_tags": ", ".join(event.attributes.tags) if event.attributes.tags else "",
            "event_timestamp_local": event_timestamp_local.strftime("%Y-%m-%d %H:%M:%S"),
            "event_title": attributes.get("title", "No Title"),
            "event_status": attributes.get("status", "Unknown")
        })

    return pd.DataFrame(processed_events)

def save_to_csv(events_df, output_dir_path="output", output_file="output/events_output.csv"):
    """
    Saves the processed event data to a CSV file.
    """
    try:
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"Directory created at: {output_dir_path}")
    except OSError as e:
        handle_errors(f"Error creating directory: {e}")
        return

    try:
        events_df.to_csv(output_file, index=False)
        print(f"Events successfully written to {output_file}.")
    except Exception as e:
        handle_errors(f"Error saving to CSV: {e}")

def handle_errors(error_message):
    """
    Centralized error handling mechanism.
    """
    print(error_message)

def main():
    """
    Orchestrates the workflow and executes the main logic.
    """
    args = parse_arguments()
    configuration = initialize_config()

    with ApiClient(configuration) as api_client:
        events_api = EventsApi(api_client)
        events_data = fetch_event_data(events_api, args.query, args.days)

        if events_data:
            events_df = process_event_data(events_data)
            print(events_df)
            save_to_csv(events_df)
        else:
            print("No events found.")

if __name__ == "__main__":
    main()

