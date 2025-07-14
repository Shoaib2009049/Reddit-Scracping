import requests
import praw
import json

# Initialize Reddit API client
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='YOUR_USER_AGENT')

def scrape_user_profile(url):
    username = url.split('/')[-1]
    user = reddit.redditor(username)
    
    # Fetch comments and submissions
    comments = list(user.comments.new(limit=10))  # Adjust limit as needed
    submissions = list(user.submissions.new(limit=10))  # Adjust limit as needed
    
    return comments, submissions

def build_user_persona(comments, submissions):
    persona = {
        "username": comments[0].author.name if comments else "Unknown",
        "comments": [],
        "submissions": [],
        "interests": set(),
        "cited_posts": []
    }
    
    # Analyze comments
    for comment in comments:
        persona["comments"].append(comment.body)
        persona["cited_posts"].append(f"Comment on {comment.subreddit}: {comment.body[:30]}...")
        persona["interests"].add(comment.subreddit.display_name)
    
    # Analyze submissions
    for submission in submissions:
        persona["submissions"].append(submission.title)
        persona["cited_posts"].append(f"Submission in {submission.subreddit}: {submission.title}...")
        persona["interests"].add(submission.subreddit.display_name)
    
    persona["interests"] = list(persona["interests"])
    
    return persona

def output_user_persona(persona, filename='user_persona.txt'):
    with open(filename, 'w') as f:
        json.dump(persona, f, indent=4)

def main():
    url = input("Enter the Reddit user profile URL: ")
    comments, submissions = scrape_user_profile(url)
    persona = build_user_persona(comments, submissions)
    output_user_persona(persona)
    print(f"User  persona saved to user_persona.txt")

if __name__ == "__main__":
    main()
