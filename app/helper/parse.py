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
