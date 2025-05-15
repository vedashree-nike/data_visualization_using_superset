# Setting Up SuperSet

## 1.Clone Superset's repo in your terminal with the following command:

git clone --depth=1  https://github.com/apache/superset.git

Once that command completes successfully, you should see a new superset folder in your current directory.

## 2. Launch Superset Through Docker Compose
First let's assume you're familiar with docker compose mechanics.
 Here we'll refer generally to docker compose up even though in some cases you may want to force a check for newer remote images using docker compose pull,
 force a build with docker compose build or force a build on latest base images using docker compose build --pull.
In most cases though, the simple up command should do just fine.
Refer to docker compose docs for more information on the topic.

### Option 1 - for an interactive development environment
The --build argument insures all the layers are up-to-date

docker compose up --build

### Option 2 - build a set of immutable images from the local branch

docker compose -f docker-compose-non-dev.yml up

## 3.Log in to Superset
Your local Superset instance also includes a Postgres server to store your data and is already pre-loaded with some example datasets that ship with Superset.
You can access Superset now via your web browser by visiting http://localhost:8088.
Note that many browsers now default to https - if yours is one of them, please make sure it uses http.

Log in with the default username and password:

 username: admin

password: admin

# Setting up Apache Kafka and MySQL

Copy docker-compose.yml file.
Run docker-compose.yml file using command:

docker compose up

### Setting up Apache Kafka Listeners



