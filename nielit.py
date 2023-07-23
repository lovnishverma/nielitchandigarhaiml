from flask import *
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# Helper function to read and update visitor count
def get_visitor_count():
    with open("visitor_count.txt", "r") as f:
        count = int(f.read())
    count += 1
    with open("visitor_count.txt", "w") as f:
        f.write(str(count))
    return count

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

    # Extract only the year from the date
    year = india_time.strftime("%Y")
    
    # Get the visitor count
    visitor_count = get_visitor_count()

    return render_template("index.html", date=date, time=time, year=year, visitor_count=visitor_count)

if __name__ == '__main__':
    app.run()
