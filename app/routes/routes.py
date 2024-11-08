import os
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests

import app
from app.utils import get_github_token, parse_github_events

router = APIRouter()

         
@router.get("/")
async def roots():
        return {
        "NOTE":"First login through /login to try it out",
        "docs":"Visit docs at /docs to try it out",
        "authentication": {
            "/login": "Start GitHub authentication",
            "/auth/callback/github": "GitHub OAuth callback URL"
        },
        "user_info": {
            "/user": "Get your GitHub profile information",
            "/user/repo": "Get list of your repositories"
        },
        "activity": {
            "/events": "Get your GitHub activity (commits, PRs, issues) grouped by type",
            "/user/events": "Get activities from people you follow",
            "/user/activity": "Get summary of your GitHub activity with counts of PRs, commits, etc."
        },
        "social": {
            "/user/followers": "List of people who follow you",
            "/user/following": "List of people you follow",
            "/user/starred": "Repositories you have starred",
            "/user/subscriptions": "Repositories you are watching"
        }
    }


@router.get("/login")
async def login_with_github():
    client_id = os.getenv("GITHUB_CLIENT_ID")
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI")
    link = f"https://github.com/login/oauth/authorize?client_id={client_id}&response_type=code&scope=repo%20user&redirect_uri={redirect_uri}"
    response = RedirectResponse(url=link)
    return response

@router.get("/auth/callback/github")
async def auth_with_github(code:str ):
    print("Verifying")
    token_url = "https://github.com/login/oauth/access_token"
    data ={
        "code":code,
        "client_id":os.getenv("GITHUB_CLIENT_ID"),
        "client_secret":os.getenv("GITHUB_CLIENT_SECRET"),
        "redirect_uri":os.getenv("GITHUB_REDIRECT_URI"),
    }
    
    headers = {"Accept": "application/json"}
    
    res = requests.post(token_url,data=data,headers=headers)
    
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token.")
    
    access_token = res.json().get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found in response.")
    
 
    if access_token:
        os.environ["GITHUB_ACCESS_TOKEN"] = access_token  

    
    print("res",res.json())
    

    user_info_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if user_info_res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info.")
    
    user_info = user_info_res.json()
    
    print(f"User Info: {user_info}")
    
    return RedirectResponse("/")
    
   


@router.get("/user")
def get_user_details(token:str = Depends(get_github_token)):
        
    user_info_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if user_info_res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info.")
    
    user_info = user_info_res.json()
    
    print(f"User Info: {user_info}")
    
    return user_info


@router.get("/user/repo")
def get_user_repo_details(token:str = Depends(get_github_token),user_info: Dict[str,any] = Depends(get_user_details)):
    
     repo_url:str = user_info["repos_url"]
     
     if(not repo_url):
            raise HTTPException(status_code=400, detail="Failed to get Repo Url.")
        
     repo_info_res = requests.get(
         repo_url,
        headers={"Authorization": f"Bearer {token}"}
     )
    
     if repo_info_res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info.")
    
     repo_info_res_ans = repo_info_res.json()
    
    
     return repo_info_res_ans



@router.get("/events")
def get_user_events_long(token: str = Depends(get_github_token), user_info: Dict[str, any] = Depends(get_user_details)):
    

    events_url = user_info["events_url"].replace("{/privacy}", "")
    print(events_url)
    
    
    events_res = requests.get(
        events_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Handle response errors
    if events_res.status_code != 200:
        raise HTTPException(status_code=events_res.status_code, detail="Failed to retrieve Events info.")
    
    print(events_res)
    
    events_data = events_res.json()
    
    
    res =  parse_github_events(events_data)
    
    
    return res


@router.get("/user/events")
def get_user_events(token: str = Depends(get_github_token), user_info: Dict[str, any] = Depends(get_user_details)):
    

    events_url = user_info["received_events_url"]
    print(events_url)
    
    
    events_res = requests.get(
        events_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Handle response errors
    if events_res.status_code != 200:
        raise HTTPException(status_code=events_res.status_code, detail="Failed to retrieve Events info.")
    
    print(events_res)
    
    events_data = events_res.json()
    return events_data
     
@router.get("/user/followers")
def get_followers(token: str = Depends(get_github_token), user_info: Dict[str, any] = Depends(get_user_details)):
    
    followers_url = user_info["followers_url"]
    
    followers_res = requests.get(
        followers_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if followers_res.status_code != 200:
        raise HTTPException(status_code=followers_res.status_code, detail="Failed to retrieve followers")
    
    return followers_res.json()

@router.get("/user/following")
def get_following(token: str = Depends(get_github_token), user_info: Dict[str, any] = Depends(get_user_details)):

    following_url = user_info["following_url"].replace("{/other_user}", "")
    
    following_res = requests.get(
        following_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if following_res.status_code != 200:
        raise HTTPException(status_code=following_res.status_code, detail="Failed to retrieve following users")
    
    return following_res.json()

@router.get("/user/starred")
def get_starred_repos(token: str = Depends(get_github_token), user_info: Dict[str, any] = Depends(get_user_details)):

    starred_url = user_info["starred_url"].replace("{/owner}{/repo}", "")
    
    starred_res = requests.get(
        starred_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if starred_res.status_code != 200:
        raise HTTPException(status_code=starred_res.status_code, detail="Failed to retrieve starred repos")
    
    return starred_res.json()



@router.get("/user/subscriptions")
def get_user_subscriptions(token: str = Depends(get_github_token), user_info: Dict[str, any] = Depends(get_user_details)):
    """Get repositories the user is watching"""
    subs_url = user_info["subscriptions_url"]
    
    subs_res = requests.get(
        subs_url,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if subs_res.status_code != 200:
        raise HTTPException(status_code=subs_res.status_code, detail="Failed to retrieve subscriptions")
    
    return subs_res.json()



@router.get("/user/activity")
async def get_activity_summary(
    events: Dict = Depends(get_user_events_long),
):

    
    summary = {
        "pull_requests": 0,
        "issues": 0,
        "commits": 0,
        "code_reviews": 0,
        "comments": 0,
        "repositories_contributed_to": set(),
        "event_counts_by_type": {} 
    }
    

    
    for event_type, event_list in events.items():
        summary["event_counts_by_type"][event_type] = len(event_list)
        
        for event in event_list:
            repo_name = event["repo"]["name"]
            summary["repositories_contributed_to"].add(repo_name)
            
            if event_type == "PullRequestEvent":
                summary["pull_requests"] += 1
                
            elif event_type == "IssuesEvent":
                summary["issues"] += 1
                
            elif event_type == "PushEvent":
                commits_count = len(event["payload"].get("commits", []))
                summary["commits"] += commits_count
                
            elif event_type == "PullRequestReviewEvent":
                summary["code_reviews"] += 1
                
            elif event_type in ["IssueCommentEvent", "CommitCommentEvent", "PullRequestReviewCommentEvent"]:
                summary["comments"] += 1
    
    summary["repositories_contributed_to"] = len(summary["repositories_contributed_to"])
    

    
    return summary