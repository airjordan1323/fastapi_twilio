import uvicorn
import os
from fastapi import FastAPI
from typing import Union
from twilio.rest import Client

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Twilio",
    description="Twilio count checker",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
)


@app.get("/api/v1/twilio_account/{sid}")
async def custom_date_filter(sid: str, from_date: str, end_date: str):
    client = Client(sid, auth_token)
    calls = client.calls.list(start_time_after=from_date, end_time_before=end_date)
    recording = client.recordings.list(date_created_after=from_date, date_created_before=end_date)
    message = client.messages.list(date_sent_after=from_date, date_sent_before=end_date)
    CALLS_ITEMS = {}
    RECORDING_ITEMS = {}
    MESSAGES_ITEMS = {}
    total = {'call': {'total_price': Union[float, int], 'total_minute': float},
             'message': {'total_price': Union[float, int], 'total_qty': float},
             'recording': {'total_price': Union[float, int], 'total_qty': float}}
    data = {'calls': [],
            'recordings': [],
            'messages': [],
            'minutes': []}
    for i in recording:
        if i.price is None:
            continue
        else:
            date = str(i.date_created).replace('+00:00', '')
            RECORDING_ITEMS[f'{date}'] = i.price
            data['recordings'].append(float(i.price))
    total['recording']['total_price'] = round(sum(map(float, data['recordings'])), 3)
    total['recording']['total_qty'] = len(data["recordings"])
    for i in message:
        if i.price is None:
            continue
        else:
            date = str(i.date_sent).replace('+00:00', '')
            MESSAGES_ITEMS[f'{date}'] = i.price
            data['messages'].append(float(i.price))
    total['message']['total_price'] = round(sum(map(float, data['messages'])), 3)
    total['message']['total_qty'] = len(data["messages"])
    for i in calls:
        if i.price is None:
            continue
        else:
            date = str(i.start_time).replace('+00:00', '')
            CALLS_ITEMS[f'{date}'] = i.price
            data['minutes'].append(i.duration)
            data['calls'].append(float(i.price))
    total['call']['total_price'] = round(sum(map(float, data['calls'])), 3)
    total['call']['total_minute'] = sum(map(float, data['minutes'])) / 60
    # total['summary'] = total['call'] + total['recordings'] + total['messages']
    print(total)
    # print(
    #     f'-----\nAll total counts without None prices:\n-----\n',
    #     f'calls -- {len(new_prices["calls"])}\n',
    #     f'recordings -- {len(new_prices["recordings"])}\n',
    #     f'messages -- {len(new_prices["messages"])}\n-----', )
    return total


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
