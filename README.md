# aka-url-shortener
Example Architecture for hosting apps in Azure
pip list --format=freeze > requirements.txt

python -m venv venv
venv\Scripts\activate

 source venv/bin/activate

gunicorn --bind 0.0.0.0 --workers $((($NUM_CORES*2)+1)) application:application