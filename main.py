import re
import json
import config
import requests
import threading
import praw as praw
from instagrapi import Client


def post_new_meme():
    threading.Timer(3600, post_new_meme).start()
    for submission in reddit.subreddit("memes").top(limit=25, time_filter="day"):
        if submission.url not in buffer:
            buffer.pop()
            buffer.insert(0, submission.url)
            file_name = submission.url.split("/")
            if len(file_name) == 0:
                file_name = re.findall("/(.*?)", submission.url)
            file_name = file_name[-1]
            if "." not in file_name:
                file_name += ".jpg"
            r = requests.get(submission.url)
            with open("./memes/" + file_name, "wb") as meme:
                meme.write(r.content)
            try:
                instagram.photo_upload(path="./memes/" + file_name, caption=submission.title)
                print(f"posted ./memes/{file_name} as {submission.title}")
            except Exception as e:
                print(f"failed ./memes/{file_name} with {e}")
    with open('buffer.json', 'w') as buffer_file:
        json.dump(buffer, buffer_file)


instagram = Client()
instagram.login(config.username, config.password)
reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent)
with open('buffer.json', 'r') as file:
    buffer = json.load(file)

post_new_meme()
