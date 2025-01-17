import re
import pandas as pd

def preprocess(data):
    # Regular expression to extract the message timestamp and user-message pattern
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apm]{2})\s-\s'

    # Split messages based on the pattern
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Ensure that dates and messages have the same length
    if len(dates) != len(messages):
        min_len = min(len(dates), len(messages))
        dates = dates[:min_len]  # truncate the longer list
        messages = messages[:min_len]

    # Create the DataFrame
    df = pd.DataFrame({'message_date': dates, 'user_message': messages})

    # Convert message_date to datetime with case-insensitive AM/PM handling
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p', errors='coerce')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists for users and messages
    users = []
    messages_list = []

    # Loop through the messages to split users and messages
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        
        if len(entry) > 1:
            users.append(entry[1])
            messages_list.append(" ".join(entry[2:]))  # Join remaining parts as the message
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # Period column (hourly range)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1}")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
