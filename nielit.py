from flask import *
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Define the timezone for India (IST)
    tz = pytz.timezone('Asia/Kolkata')

    # Get the UTC offset for the India time zone
    india_offset = timedelta(seconds=tz.utcoffset(utc_now).total_seconds())

    # Add the UTC offset to the current UTC time to get India time
    india_time = utc_now + india_offset

    # Extract date and time components in 12-hour format
    date = india_time.strftime("%Y-%m-%d")
    time = india_time.strftime("%I:%M %p")

    return render_template("index.html", date=date, time=time)

if __name__ == '__main__':
    app.run()
