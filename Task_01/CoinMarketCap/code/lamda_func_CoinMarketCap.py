import csv
import requests
from bs4 import BeautifulSoup
import boto3
from io import StringIO
from datetime import datetime

# Set your S3 bucket name and prefix (folder)
BUCKET_NAME = "data-hackathon-smit-hassanabbas"
FILE_PREFIX = "raw/"

# Create S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        url = "https://coinmarketcap.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Fetch and parse page
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")


        # Data container
        crypto_data = []

        for row in table_rows:
            cols = row.find_all("td")
            if len(cols) < 7:
                continue

            name = cols[2].find("p", class_="sc-4984dd93-0 kKpPOn").text
            symbol = cols[2].find("p", class_="sc-4984dd93-0 iqdbQL").text
            price = cols[3].text
            market_cap = cols[7].text
            volume_24h = cols[6].text
            percent_change_24h = cols[5].text

            crypto_data.append([
                name, symbol, price, market_cap, volume_24h, percent_change_24h
            ])

        # Write to CSV in-memory
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Name", "Symbol", "Price", "Market Cap", "24h Volume", "24h % Change"])
        writer.writerows(crypto_data)

        # Timestamped filename
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
        file_key = f"{FILE_PREFIX}/top_10_crypto_{timestamp}.csv"

        # Upload CSV to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )

        return {
            "statusCode": 200,
            "body": f"CSV uploaded successfully to s3://{BUCKET_NAME}/{file_key}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error occurred: {str(e)}"
        }