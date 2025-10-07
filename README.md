# Short URL Generator At Scale

## Objective

The objective is to show how to implement a multi tier modern web application. Hosted in azure.

### Code

Python Requirements

```python
pip list --format=freeze > requirements.txt
```

Virtual Environment

```python
python -m venv venv
venv\Scripts\activate

source venv/bin/activate
```

### Infrastructure Deployment

The infrastructure is deployed using Terraform and consists of several Azure resources:

- Azure App Service (Linux) for hosting the Python Flask application
- Azure SQL Database for storing URL mappings
- Azure Redis Cache for caching frequently accessed URLs
- Azure Key Vault for secure storage of connection strings and secrets
- Azure Application Insights for monitoring and telemetry
- Azure Log Analytics for centralized logging

**Terraform Modules:**
- `shared_services` - Deploys Key Vault, Log Analytics, and Application Insights
- `webapp` - Deploys App Service Plans and Web Apps
- SQL Server and Databases
- Redis Cache

**Required Permissions:**
- Contributor access to the target Azure subscription
- Permissions to create service principals and assign roles

**Deployment Steps:**
1. Navigate to `src/infa/tf_deploy_appsrv`
2. Update `variables.tf` and `locals.tf` with your configuration
3. Initialize Terraform: `terraform init`
4. Plan deployment: `terraform plan`
5. Apply configuration: `terraform apply`

The deployment automatically configures Key Vault references for secure secret management in the Web App settings.

### API Web Application

#### Custom startup command

The Azure Web App (linux) uses Gunicorn to host the python application. The number of worker processes can be dynamically assigned in the startup command by using the environmental variable $NUM_CORES.

```text
gunicorn --bind 0.0.0.0 --workers $((($NUM_CORES*2)+1)) application:application
```

### UI Web Application

The URL shortener application is designed with a decoupled architecture where the backend API handles all URL shortening operations. The current implementation focuses on the API layer, which can be consumed by:

- Direct API calls using curl or HTTP clients
- Custom frontend applications (web, mobile, or desktop)
- Integration with other services via REST API

**API Endpoints:**
- `POST /v1/shorten?longurl={url}` - Create a shortened URL
- `GET /v1/shorten/{short_code}` - Retrieve the original URL
- `GET /heartbeat` - Health check endpoint

Frontend applications can be built using any modern framework (React, Angular, Vue.js, etc.) and should communicate with the API to create and resolve shortened URLs.

### Database Architecture

Application uses sql alchmey to create and manage the database schema.
The snowflake ID is generated based on time, datacenter id (Azure Region Name), and instance id of the web app. 
Use snowflake ID vs using UUID - [snowflake][gh-snowflake]
![Snowflake ID](/doc/snowflakeid.png "SnowFlake ID Layout")

### Application Testing Locally

**Prerequisites:**
- Python 3.8 or higher
- SQL Server (local or Azure SQL Database)
- Redis (local or Azure Redis Cache)

**Setup Steps:**

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   cd src/akabackend
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the `src/akabackend` directory with the following variables:
   ```
   APPLICATIONINSIGHTS_CONNECTION_STRING=<your-app-insights-connection-string>
   SQL_DB_SERVER=<your-sql-server>.database.windows.net
   SQL_DB01=<your-database-name>
   SQL_USER=<your-username>
   SQL_PWD=<your-password>
   REDIS_HOST=<your-redis-host>
   REDIS_PORT=6380
   REDIS_PASS=<your-redis-password>
   HOST_TYPE=localhost
   ENV=dev
   ```

4. **Run the Application:**
   ```bash
   python application.py
   ```
   Or with Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:5000 application:application
   ```

5. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:5000/heartbeat
   
   # Create shortened URL
   curl -X POST 'http://localhost:5000/v1/shorten?longurl=https://www.example.com' \
     --header 'Content-Type: application/json'
   
   # Retrieve original URL
   curl http://localhost:5000/v1/shorten/{short_code}
   ```

**Testing with Docker:**
```bash
cd src/akabackend
docker build -t aka-url-shortener .
docker run -p 5000:5000 aka-url-shortener
```

### Azure Load Testing

The application includes load testing capabilities to validate performance at scale.

**Load Test Configuration:**

A sample JMeter test plan is provided at `src/akabackend/app/tests/SampleTest.jmx` for load testing the API endpoints.

**Azure Load Testing Service:**

Azure Load Testing can be used to simulate high-scale load on the URL shortener service. The service allows you to:

- Generate load from multiple Azure regions simultaneously
- Test the application's ability to handle concurrent requests
- Monitor performance metrics including response time, throughput, and error rates
- Identify bottlenecks in the application and infrastructure

**Key Metrics to Monitor:**
- **Requests per second:** Target throughput for URL creation and retrieval
- **Response time:** P50, P95, and P99 latency percentiles
- **Error rate:** Percentage of failed requests
- **Database performance:** Query execution time and connection pool utilization
- **Cache hit ratio:** Redis cache effectiveness

**Testing Scenarios:**
1. **URL Creation Load Test:** Measure the system's ability to create shortened URLs under high load
2. **URL Retrieval Load Test:** Test read performance with cache hits and misses
3. **Mixed Workload Test:** Simulate realistic traffic patterns with both creation and retrieval

**Running Load Tests:**
- Use the Azure Load Testing service in the Azure Portal
- Upload the JMeter test plan or configure a URL-based test
- Configure virtual users and test duration
- Monitor results in Application Insights and Azure Load Testing dashboards

**Performance Targets:**
- Support 1000+ requests per second for URL retrieval
- Sub-100ms response time for cached URLs
- Horizontal scaling with multiple App Service instances using the Snowflake ID approach to avoid collisions

<!--- Link Ref --->
[gh-snowflake]: https://github.com/twitter-archive/snowflake
<!--- Link Ref --->

<!--- Link Ref Image Source--->
[src-snowflakeid]: https://en.wikipedia.org/wiki/Snowflake_ID#/media/File:Snowflake-identifier.png
<!--- Link Ref Image Source --->