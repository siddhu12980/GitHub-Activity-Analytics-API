

import os
from fastapi import Depends, HTTPException
import requests


def parse_github_events(events):

    events_by_type = {}
    
    for event in events:
        event_type = event['type']
        
        if event_type not in events_by_type:
            events_by_type[event_type] = []
            
        cleaned_event = {
            'id': event['id'],
            'actor': event['actor'],
            'repo': event['repo'],
            'payload': event['payload'],
            'created_at': event['created_at']
        }
        
        events_by_type[event_type].append(cleaned_event)
    
    return events_by_type


def get_github_token():

    token = os.getenv("GITHUB_ACCESS_TOKEN")
      
    if not token:
        raise HTTPException(
            status_code=403,
            detail="GitHub token not available"
        )
    return token

def validate_token(token : str = Depends(get_github_token)):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    
    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Invalid GitHub token"
        )
    return token
    

