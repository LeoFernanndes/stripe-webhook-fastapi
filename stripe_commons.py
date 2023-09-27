import stripe
import json
from decouple import config
from json_commons import append_to_json_file

STRIPE_API_KEY=config('STRIPE_API_KEY')
stripe.api_key =STRIPE_API_KEY

def list_events(limit: int = 20) -> [stripe.Subscription]:
    response = stripe.Event.list(limit=limit)
    events: [stripe.Event] = response.data
    return events

def list_subscriptions(limit: int = 20, customer: str = 'cus_NCsC3D0mgrWNAt') -> [stripe.Event]:
    subscriptions = stripe.Subscription.list(limit=limit, customer=customer)
    return subscriptions.data

def upcoming_invoice(customer: str = 'cus_NCsC3D0mgrWNAt') -> stripe.Invoice:
    upcoming_invoice = stripe.Invoice.upcoming(customer=customer)
    return upcoming_invoice

def reset_last_event(filename: str):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    try:
        file_data[-29]
        print("reset last events not necessary")
    except IndexError:
        last_events = list_events(limit=30)
        last_events.reverse()
        for event in last_events:
            append_to_json_file(filename=filename, json_content=event)
        print("reset last events ok")