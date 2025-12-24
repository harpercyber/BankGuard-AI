from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

#Creates ASGI app; the 'brain' of the server
app = FastAPI()

#list to store incoming events; will eventually replace with database
events = []

#Basically a contract that says any event sent to this server must look like the following
class Event(BaseModel):
    user: str
    timestamp: str
    event_type: str
    amount: Optional[float] = None

#Confirms server is alive
@app.get("/")
def running():
    return {"message": "BankGuard API running"}


#events is an endpoint that accepts HTTP POST requests
#This is the log ingestion point
@app.post("/events")
def receive_event(event: Event):
    
    #event is a python object and dict converts it to JSON-style data
    events.appent(event.dict())

    #Confirms ingestion succeeded; will enhance later
    return {"status": "received", "event": event}




