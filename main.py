import praw, requests, re, json, os
from instabot import Bot

reddit = praw.Reddit(client_id="*********", client_secret="**************************", user_agent="*********")
insta = Bot()
insta.login(username="*********", password="**************************")
postList = []

with open('postlist.txt', 'r') as filehandle:
    postList = json.load(filehandle)

#clear#

for submission in reddit.subreddit("memes").top(limit=25, time_filter="day"):
    title = submission.title
    if title not in postList:
        try:
            postList.pop()
            postList.insert(0, submission.title)
            file_name = submission.url.split("/")
            if len(file_name) == 0:
                file_name = re.findall("/(.*?)", submission.url)
            file_name = file_name[-1]
            if "." not in file_name:
                file_name += ".jpg"
            r = requests.get(submission.url)
            with open("pic/" + file_name, "wb") as f:
                f.write(r.content)
            print("New Post: " + submission.title + "\nPicture: " + file_name)
            insta.upload_photo("pic/" + file_name, caption=submission.title)
        except:
            pass

with open('postlist.txt', 'w') as filehandle:
    json.dump(postList, filehandle)
