 Data Engineering Hackathon: Real-time Financial Data Pipeline

🧠 Overview

This project builds a real-time, serverless data pipeline using AWS to ingest and store data from major financial sources:

- 📈 **Yahoo Finance** – OHLCV data for all S&P 500 companies
- 💰 **CoinMarketCap** – Top 10 cryptocurrencies by market cap
- 🌍 **Open Exchange Rates** – Live foreign exchange rates

Data is collected every minute and stored in an Amazon S3 bucket, structured by source and timestamp.

---

 ⚙️ Architecture

🔹 Task 1 – Data Acquisition

- **3 AWS Lambda Functions** (1 per source)
- **Amazon EventBridge** triggers each function every minute
- **Amazon S3** stores raw data under the `raw/` directory with metadata

 🔹 Task 2 – (Optional Future Setup)

- **Amazon SNS**: Detects new files in S3 and filters events by source
- **SQS FIFO Queues**: One per data source
- **3 Lambda Processors**:
  - Yahoo Finance → Snowflake
  - CoinMarketCap → Processed S3
  - Open Exchange Rates → SQL Server

📌 Technologies Used
AWS Lambda (Python 3.9)
Amazon EventBridge
Amazon S3
yfinance, pandas, BeautifulSoup, requests

🧩 Future Enhancements (Task 2)
Add Amazon SNS and SQS FIFO queues for streaming event routing

Use additional Lambda processors to transform/load into:

💾 Snowflake (Yahoo Finance)

🗃️ SQL Server (Open FX)

🧊 S3 Processed Zone (CoinMarketCap)

🛡️ Security
Use IAM roles for Lambda to access S3, EventBridge, and logs.

Store sensitive keys using AWS Secrets Manager or env variables.

👤 Author
Hassan Abbas
GitHub: https://github.com/AbbasMatrixs
Hackathon: [Data Engineering Hackathon 2025]