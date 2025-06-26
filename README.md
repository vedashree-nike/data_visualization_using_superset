## Architecture Diagram

![Image](https://github.com/user-attachments/assets/282926b7-c0ca-458b-80e3-64e991b40a70)

## Problem Statement

In today's data-rich environment, businesses face an enormous challenge: how to make sense of millions of transactions, identify critical patterns, and pinpoint potential issues or opportunities. Manually tracking and analyzing every single transaction is not just inefficient; it's practically impossible. This lack of clear visibility into transaction data often leads to:

#### Suboptimal decision-making:
Without a comprehensive understanding of trends and anomalies, strategic choices are often based on incomplete or outdated information.

#### Missed opportunities:
Valuable insights hidden within the data—such as customer behavior shifts or emerging market trends—remain undiscovered.

#### Inefficient problem-solving:
Identifying the root cause of issues, like discrepancies in vendor transactions or product performance, becomes a time-consuming and arduous task.

## My Approach

This project addresses these challenges by leveraging data science and modern data architecture to transform raw transaction data into actionable insights. Our approach focuses on providing a visual outline of millions of data points in a structured format to empower better decision-making.

### Key aspects of our solution include:

#### Data Collection & Analysis:
We begin by understanding crucial transaction attributes like location, time, vendors, and products. For this prototype, we're generating randomized data using a Python script to simulate real-world scenarios.

#### Robust Design & Implementation:
This stage involves designing a scalable database structure, integrating a powerful tech stack, and creating insightful dashboards.

##### Apache Kafka as a Real-Time Data Interface:
Recognizing the future need for real-time data processing, we've integrated Apache Kafka. Its exceptional scalability and flexibility allow it to handle high-velocity data streams, serving as a seamless interface between diverse data sources and our central database. This eliminates the need for complex pipelines, modifications, or duplications when connecting to the source, enabling real-time analysis.

##### Apache Superset for Intuitive Visualizations:
While many BI tools exist, we've chosen Apache Superset for its ability to directly integrate with the central database and handle large volumes of data from different teams. It's an open-source, cost-effective solution that provides powerful, interactive dashboards, simplifying data review and analysis for quick insights and solutions.

## Requirements Setup

## Setting Up SuperSet

### 1. Clone Superset's repository in your terminal with the following command:

```git clone --depth=1  https://github.com/apache/superset.git```

Once that command completes successfully, you should see a new superset folder in your current directory.

### 2. Launch Superset Through Docker Compose
First let's assume you're familiar with docker compose mechanics.
 Here we'll refer generally to docker compose up even though in some cases you may want to force a check for newer remote images using docker compose pull,
 force a build with docker compose build or force a build on latest base images using docker compose build --pull.
In most cases though, the simple up command should do just fine.
Refer to docker compose docs for more information on the topic.

#### Option 1 - for an interactive development environment
The --build argument insures all the layers are up-to-date

```docker compose up --build```

#### Option 2 - build a set of immutable images from the local branch

```docker compose -f docker-compose-non-dev.yml up```

### 3. Log in to Superset
Your local Superset instance also includes a Postgres server to store your data and is already pre-loaded with some example datasets that ship with Superset.
You can access Superset now via your web browser by visiting http://localhost:8088.
Note that many browsers now default to https - if yours is one of them, please make sure it uses http.

Log in with the default username and password:

username: admin

password: admin

### Setting up Apache Kafka and MySQL

Copy docker-compose.yml file.
Run docker-compose.yml file using command:

```docker compose up```

#### Setting up Apache Kafka Listeners
Run the producer.py and consumer.py simultaneously to generate and ingest the dataset.

```python3 producer.py```
```python3 consumer.py```

#### Importing dashboard
Download the dashboard file.
Import the file after setting up Superset.
