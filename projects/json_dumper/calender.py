# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "flask",
# ]
# ///
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# Store events in a list of dictionaries
events = [
    {
        "title": "Morning Meeting",
        "start": "09:30",
        "end": "10:00"
    },
    {
        "title": "Lunch Break",
        "start": "12:00",
        "end": "13:00"
    }
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Day Calendar</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .calendar {
            position: relative;
            border: 1px solid #ddd;
            width: 800px;
            height: 1440px;  /* 24 hours * 60px per hour */
        }
        .hour-marker {
            position: absolute;
            width: 100%;
            border-top: 1px solid #eee;
            height: 60px;
        }
        .hour-label {
            position: absolute;
            left: -50px;
            width: 45px;
            text-align: right;
            font-size: 12px;
            color: #666;
        }
        .event {
            position: absolute;
            left: 50px;
            right: 10px;
            background-color: #4285f4;
            color: white;
            padding: 5px;
            border-radius: 3px;
            font-size: 14px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="calendar">
        {% for hour in range(24) %}
        <div class="hour-marker" style="top: {{ hour * 60 }}px">
            <div class="hour-label">{{ "%02d:00"|format(hour) }}</div>
        </div>
        {% endfor %}
        
        {% for event in events %}
        <div class="event" style="top: {{ time_to_pixels(event['start']) }}px; height: {{ event_height(event['start'], event['end']) }}px;">
            {{ event['title'] }}<br>{{ event['start'] }} - {{ event['end'] }}
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

def time_to_pixels(time_str):
    """Convert time string (HH:MM) to pixels from top"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def event_height(start_time, end_time):
    """Calculate event height in pixels"""
    return time_to_pixels(end_time) - time_to_pixels(start_time)

@app.route('/')
def calendar():
    return render_template_string(HTML_TEMPLATE, 
                                events=events, 
                                time_to_pixels=time_to_pixels,
                                event_height=event_height)

if __name__ == '__main__':
    app.run(debug=True)