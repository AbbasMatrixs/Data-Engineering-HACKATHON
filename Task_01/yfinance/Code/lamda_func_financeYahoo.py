import yfinance as yf
import pandas as pd
import boto3
import json
from datetime import datetime
import os

def lambda_handler(event, context):
    # Fetch S&P 500 ticker symbols from Wikipedia
    try:
        sp500_table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        tickers = sp500_table[0]['Symbol'].tolist()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error fetching tickers: {str(e)}'
        }

    # Optional limit for testing
    tickers = tickers[:10]  

    now = datetime.utcnow()
    path_date = now.strftime('%Y/%m/%d')
    file_time = now.strftime('%H%M')
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    filename = f"raw/yahoofinance/{path_date}/{file_time}.json"

    bucket_name = os.getenv('BUCKET_NAME', 'data-hackathon-smit-hassanabbas')

    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="1d", interval="1m")
            if df.empty:
                continue
            latest = df.tail(1).reset_index().to_dict(orient='records')[0]
            data[ticker] = latest
        except Exception as e:
            data[ticker] = {'error': str(e)}

    # Upload to S3
    s3 = boto3.client('s3')
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=json.dumps(data),
            Metadata={
                'source': 'yahoofinance',
                'timestamp': timestamp,
                'status': 'success'
            }
        )
        return {
            'statusCode': 200,
            'body': f'Successfully uploaded {filename}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Upload error: {str(e)}'
        }