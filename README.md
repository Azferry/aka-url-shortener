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

> **Note**
> Required permissions: 

Startup command for the web app

#### API Web Application

Custom startup command

```text
gunicorn --bind 0.0.0.0 --workers $((($NUM_CORES*2)+1)) application:application
```

#### UI Web Application

TBD

#### Database Architecture

TBD
Use snowflake ID vs using UUID - [snowflake][gh-snowflake]
![Snowflake ID](/doc/snowflakeid.png "SnowFlake ID Layout")

### Application Testing

#### Testing Locally

TBD

#### Azure Load Testing

TBD

<!--- Link Ref --->
[gh-snowflake]: https://github.com/twitter-archive/snowflake
<!--- Link Ref --->

<!--- Link Ref Image Source--->
[snowflakeid]: https://en.wikipedia.org/wiki/Snowflake_ID#/media/File:Snowflake-identifier.png
<!--- Link Ref Image Source --->