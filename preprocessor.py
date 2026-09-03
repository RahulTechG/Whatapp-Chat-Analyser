import re
import pandas as pd


def preprocess(data):

    # ---------------------------------------------------------
    # 1. Detect WhatsApp message starting points
    # ---------------------------------------------------------

    pattern = re.compile(
        r'(?m)^'
        r'(?:'
        # Format:
        # 03/09/26, 9:42 pm - Rahul: Hello
        r'(?P<date1>\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*[apAP][mM])\s*-\s*(?P<msg1>.*)'
        r'|'
        # Format:
        # [03/09/26, 9:42 pm] Rahul: Hello
        r'\[(?P<date2>\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*[apAP][mM])\]\s*(?P<msg2>.*)'
        r')'
    )

    matches = list(pattern.finditer(data))

    # ---------------------------------------------------------
    # 2. Check whether messages were detected
    # ---------------------------------------------------------

    if not matches:
        return pd.DataFrame(
            columns=[
                'date',
                'user',
                'message',
                'only_date',
                'year',
                'month_num',
                'month',
                'day',
                'day_name',
                'hour',
                'minute',
                'period'
            ]
        )

    # ---------------------------------------------------------
    # 3. Extract messages
    # ---------------------------------------------------------

    records = []

    for i, match in enumerate(matches):

        date_string = match.group('date1') or match.group('date2')
        first_line = match.group('msg1') or match.group('msg2')

        # Find where the next message starts
        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
            remaining_text = data[start:end]
        else:
            remaining_text = data[start:]

        # Add multiline content
        full_message = first_line + remaining_text

        # -----------------------------------------------------
        # 4. Separate user and message
        # -----------------------------------------------------

        user_match = re.match(
            r'([^:]+):\s*(.*)',
            full_message,
            re.DOTALL
        )

        if user_match:

            user = user_match.group(1).strip()
            message = user_match.group(2).strip()

        else:

            # System notification / group notification
            user = 'group_notification'
            message = full_message.strip()

        records.append(
            {
                'message_date': date_string,
                'user': user,
                'message': message
            }
        )

    # ---------------------------------------------------------
    # 5. Create DataFrame
    # ---------------------------------------------------------

    df = pd.DataFrame(records)

    # ---------------------------------------------------------
    # 6. Convert date
    # ---------------------------------------------------------

    df['date'] = pd.to_datetime(
        df['message_date'],
        dayfirst=True,
        errors='coerce'
    )

    df.drop(columns=['message_date'], inplace=True)

    # Remove rows where date could not be parsed
    df = df.dropna(subset=['date']).reset_index(drop=True)

    # ---------------------------------------------------------
    # 7. Date features
    # ---------------------------------------------------------

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # ---------------------------------------------------------
    # 8. Period
    # ---------------------------------------------------------

    df['period'] = df['hour'].apply(
        lambda hour: f"{hour:02d}-{(hour + 1) % 24:02d}"
    )

    if df.empty:
    raise ValueError(
        "No messages could be parsed. "
        "Please check the chat format."
    )

    return df
