from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from rules import label_event

#Creates ASGI app; the 'brain' of the server
app = FastAPI()

#list to store incoming events; will eventually replace with database
events = []

#Basically a contract that says any event sent to this server must look like the following
class Event(BaseModel):
    user_id: str
    name: str
    IP_address: str
    home_region: str
    timestamp: str
    location: str
    login_success: bool
    transaction_amount: Optional[float] = None

#Confirms server is alive
@app.get("/")
def running():
    return {"message": "BankGuard API running"}


#events is an endpoint that accepts HTTP POST requests
#This is the log ingestion point
@app.post("/events")
def receive_event(event: Event):
    
    #event is a python object and dict converts it to JSON-style data
    events.append(event.dict())

    #Confirms ingestion succeeded; will enhance later
    return {"status": "received", "event": event}


print(f"Total events received: {len(events)}")


def label_event(event:dict) -> dict:
    """
    Accepts a single log (dictionary) and labels it as normal or suspicious based on your defined rules.
    """
    #Creates a list that will append reasons for a user being suspicious based on conditions they trigger
    reasons = []

    #adds failed logins as a reason
    if not event.get("login_success", True):
        reasons.append("failed login")

    #if transaction amount higher than $5000 then it is added as a suspicious reason
    if event.get("transaction amount", 0) > 5000:
        reasons.append("high transaction")

    event["is_suspicious"] = len(reasons) > 0
    #gives each log a explanation for why its suspicious or marks it as normal if no issues
    event["reason"] = ",".join(reasons) if reasons else "normal"
    event["risk_level"] = len(reasons)

    return event