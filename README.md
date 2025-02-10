
# FetchEvent

FetchEvent is a command-line application that retrieves and processes event logs from Datadog based on customizable search parameters. It allows users to filter, analyze, and export event data for streamlined monitoring and operational insights.

## Features

- Retrieves event data from Datadog based on a user-defined query.
- Supports dynamic time range selection.
- Outputs data into a structured CSV file for analysis.
- Automatically adjusts timestamps to a specified timezone.

## Requirements

- Python 3.7+
- A Datadog account with API and application keys.
- A `.env` file containing the Datadog API and application keys.

## Installation

1. Clone this repository or download the script file.

   ```bash
   git clone https://github.com/yourusername/fetchevent.git
   cd fetchevent
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following contents:

   ```env
   DD_API_KEY=your_datadog_api_key
   DD_APP_KEY=your_datadog_app_key
   ```

## Usage

Run the script from the command line with the following options:

```bash
python fetch_events.py --query "your_search_query" --days 30
```

### Command-Line Arguments

- `--query` (required): The search query to filter events (e.g., `service:trms production service check`).
- `--days` (optional): The number of days in the past to fetch events. Defaults to `30`.

### Example

Fetch events matching the query `service:trms production service check` from the last 15 days:

```bash
python fetch_events.py --query "production service check" --days 15
```

## Output

The application generates a CSV file (`events_output.csv`) containing the following fields:

- `event_id`: The unique identifier for the event.
- `event_type`: The type of the event.
- `event_tags`: Tags associated with the event.
- `event_timestamp_local`: The timestamp of the event in the Asia/Manila timezone.
- `event_title`: The title of the event.
- `event_status`: The status of the event.

## Dependencies

The application relies on the following Python packages:

- `pandas`: For handling and exporting data.
- `python-dotenv`: For managing environment variables.
- `datadog_api_client`: For interacting with the Datadog API.
- `pytz`: For timezone handling.

Install all dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Known Issues

- Ensure that the `.env` file is correctly configured; missing or invalid API keys will result in errors.
- Large datasets may take a while to process due to API rate limits.

## Future Enhancements

- Add support for multiple timezones.
- Implement advanced filtering options.
- Provide additional output formats (e.g., JSON).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Support

For support or questions, please contact `elacson@gmail.com.
git