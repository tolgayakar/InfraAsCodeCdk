from datetime import datetime

def lambda_handler(event, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return {"UTC": current_time}
