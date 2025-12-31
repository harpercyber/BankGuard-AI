from faker import Faker
import datetime
import uuid
from random import random
from random import choice, random, randint

fake = Faker()

# Define home regions with corresponding IP prefixes
REGION_IP_RANGES = {
    "US_EAST": ["10.10.", "10.11."],
    "US_WEST": ["10.20.", "10.21."],
    "EU_CENTRAL": ["10.30.", "10.31."],
    "ASIA_EAST": ["10.40.", "10.41."],
}

def gen_ip_region(region: str) -> str:
    """Generate a random IP in the given region's range"""
    
    #pick a random IP prefix for the region
    prefix = choice(REGION_IP_RANGES[region])
    
    #fill the last two octets randomly and return full IP string
    return f"{prefix}{randint(0,255)}.{randint(1,254)}"


class SimPerson:
    """Represents a simulated banking user."""

    #Class initialization
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.user_id = str(uuid.uuid4())
        self.failed_logins = 0
        self.home_region = choice(list(REGION_IP_RANGES.keys()))


    #Method that keeps track of how many times a person failed logging in.
    def attempt_login(self):
        success = random() > 0.2
        if not success:
            self.failed_logins += 1
        
        else:
            self.failed_logins = 0

        return success

#creates a list of 50 users
#users = [SimPerson(fake.name(), fake.address(), fake.ipv4_private()) for _ in range(50)]

#Function generates a log of an instance of the Sim_Person class
def generate_log(person: SimPerson, mismatch_rate=0.1) -> dict:
    """
    Generate a single log for a person.
    Sometimes intentionally mismatches IP region to simulate suspicious behaviour
    """
    #10% of logs will have an IP outside of the home region
    use_home_region = random() > mismatch_rate
   
   #decides if the log uses the user's correct region
    if use_home_region:
        ip_region = person.home_region

    else:
        ip_region = choice([r for r in REGION_IP_RANGES.keys() if r !=  person.home_region])
    
    ip_address = gen_ip_region(ip_region)

   
   
   
   #Dictionary that represents a single security/transaction log entry
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": person.user_id,
        "name": person.name,
        "transaction_amount": round(random() * 5000 + 10, 2),
        "IP_address": ip_address,
        "home_region": person.home_region,
        "location": person.location,
        "login_success": person.attempt_login()
    }
    return log

#Function that passes through a list of Sim_Person objects and generates a log for each of them depending on n's value
def gen_logs(users, n=200):
    #Create empty list to store logs of users. A list of dictionaries.
    logs =[]

    #for any in range of n a random user is selected from list of users
    #The user is then generated a log and added to logs
    for _ in range(n):
        user  = choice(users)
        logs.append(generate_log(user))
    return logs

