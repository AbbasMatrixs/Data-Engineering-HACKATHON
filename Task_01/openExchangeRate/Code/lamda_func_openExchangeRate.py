import os
import json
import boto3
import requests
from datetime import datetime, timezone

def s3_client(json_data, timestamp):
    # Convert timestamp to structured folder path
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    year = dt.strftime('%Y')
    month = dt.strftime('%m')
    day = dt.strftime('%d')
    hour = dt.strftime('%H')

    # S3 path
    s3_key = f"raw/{year}/{month}/{day}/exchange-rates-{hour}.json"
    
    # Get bucket name from environment variable
    s3_bucket_name = os.environ.get('data-hackathon-smit-hassanabbas')
    if not s3_bucket_name:
        raise ValueError("Environment variable 'data-hackathon-smit-hassanabbas' is not set.")

    # Upload to S3
    s3 = boto3.client("s3")
    s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json_data)

def fetch_and_store_exchange_rates():
    # Get base URL and app_id from environment
    base_url = os.environ.get("oer_base_url")
    app_id = os.environ.get("oer_app_id")

    if not base_url or not app_id:
        raise ValueError("Environment variables 'oer_base_url' or 'oer_app_id' are not set.")

    # Build the request URL
    url = f"{base_url}?app_id={app_id}"
    print("Calling URL:", url)

    # Make the API request
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Format the timestamp
        timestamp = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert JSON to string
        json_data = json.dumps(data)
        
        # Upload to S3
        s3_client(json_data, timestamp)
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

def lambda_handler(event, context):
    try:
        fetch_and_store_exchange_rates()
        return {
            'statusCode': 200,
            'body': json.dumps('Exchange rate data saved to S3 successfully.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }