import requests
import time
import datetime
from decouple import config
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from stripe_commons import list_events, list_subscriptions, upcoming_invoice, reset_last_event
from json_commons import append_to_json_file, get_last_posted_event, list_posted_events


WEBHOOK_URL=config('WEBHOOK_URL' ,'http://localhost:8003/app/billing/v2/webhook/')
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/subscriptions")
async def get_subscriptions():
    subscriptions = list_subscriptions()
    return subscriptions

@app.get("/events")
async def get_events():
    events = list_events()
    return events

@app.get("/upcoming-invoice")
async def get_upcoming_invoice():
    invoice = upcoming_invoice()
    return invoice

@app.on_event("startup")
@repeat_every(seconds=60)  # 1 hour
def periodically_post_last_events() -> None:
    webhook_url = WEBHOOK_URL
    json_filename = 'history.json'
    reset_last_event(filename=json_filename)
    events_to_post = []
    posted_events = list_posted_events(filename=json_filename)
    for event in list_events():
        if event["id"] in [event["id"] for event in posted_events]:
            continue
        if event["id"] in [event["id"] for event in events_to_post]:
            continue
        events_to_post.append(event)
    
    ordered_events_to_post = events_to_post.copy()
    ordered_events_to_post.reverse()
    
    errors = []
    for event in ordered_events_to_post:
        try:
            time.sleep(5)
            requests.post(webhook_url, json=event)
            append_to_json_file(filename=json_filename, json_content=event)
        except Exception as e:
            print(e)  
            error_object = {
                "id": event["id"],
                "type": event["type"],
                "error": type(e)
            }
            errors.append(error_object)
    
    _time = datetime.datetime.now().isoformat()
    print(f"Iteration completed at {_time} ->")
    if errors:
        response = {"data": errors}
        print(response)
    response = {"data": f"posted {len(ordered_events_to_post) - len(errors)} from {len(ordered_events_to_post)} with success"}
    print(response)

    
    
@app.post("/trigger-webhook")
async def trigger_webhook():
    webhook_url = WEBHOOK_URL
    json_filename = 'history.json'
    time.sleep(5)
    reset_last_event(filename=json_filename)
    events_to_post = []
    posted_events = list_posted_events(filename=json_filename)
    print(f"{len(events_to_post)} events to post")
    for event in list_events():
        if event in posted_events:
            print(f"{event.id} in posted event")
            continue
        if event in events_to_post:
            print(f"{event.id} in events to post")
            continue
        print(f"{event.id} added to events to post")
        events_to_post.append(event)
    
    
    
    ordered_events_to_post = events_to_post.copy()
    ordered_events_to_post.reverse()
    print(f"len ordered items to post {len(ordered_events_to_post)}")
    
    errors = []
    for event in ordered_events_to_post:
        try:
            time.sleep(5)
            requests.post(webhook_url, json=event)
            append_to_json_file(filename=json_filename, json_content=event)
        except:
            error_object = {
                "id": event["id"],
                "type": event["type"]
            }
            errors.append(error_object)
        
    if errors:
        response = {"data": errors}
        print(response)
        return response
    response = {"data": f"posted {len(ordered_events_to_post)} with success"}
    print(response)
    return response

    
@app.get("/manually-trigger-webhook")
async def trigger_webhook():
    webhook_url = WEBHOOK_URL
    json_filename = 'history.json'
    last_event = list_events()[0]
    print(last_event)
    try:
        response  = requests.post(webhook_url, json=last_event)
        print(response.content)
        append_to_json_file(filename=json_filename, json_content=last_event)
        return {"data": "webhook post ok"}
    except Exception as e:
        print(e)
        return {"data":"failed to post to webhook"}