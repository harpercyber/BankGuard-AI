from faker import Faker
import datetime
import uuid
from random import random
from random import choice

fake = Faker()

class SimPerson:
    """Represents a simulated banking user."""

    #Class initialization
    def __init__(self, name, location, ipv4):
        self.name = name
        self.location = location
        self.ipv4 = ipv4
        self.user_id = str(uuid.uuid4())
        self.failed_logins = 0

    #Method that keeps track of how many times a person failed logging in.
    def attempt_login(self):
        success = random() > 0.1
        if not success:
            self.failed_logins += 1
        
        else:
            self.failed_logins = 0

        return success

#creates a list of 50 users
users = [SimPerson(fake.name(), fake.address(), fake.ipv4_private()) for _ in range(50)]

#Function generates a log of an instance of the Sim_Person class
def generate_log(person: SimPerson):
   
   #Dictionary that represents a single security/transaction log entry
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": person.user_id,
        "name": person.name,
        "transaction_amount": round(random() * 5000 + 10, 2),
        "IP_address": person.ipv4,
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
