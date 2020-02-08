from InstagramAPI import InstagramAPI
import requests
import time
import random
import json
from tkinter import Tk, Label, Button, Entry


class RaffleGramGUI:

    def __init__(self, master):
        self.master = master
        master.title("RaffleGram")

        self.username_label = Label(master, text="Username:")
        self.username_entry = Entry(master)
        self.password_label = Label(master, text="Password:")
        self.password_entry = Entry(master)
        self.mediaid_label = Label(master, text="Post URL:")
        self.mediaid_entry = Entry(master)
        self.result_label = Label(master)
        self.go_button = Button(master, text="Submit", command=self.pick_user)

        self.username_label.grid(row=0)
        self.username_entry.grid(row=1)
        self.password_label.grid(row=2)
        self.password_entry.grid(row=3)
        self.mediaid_label.grid(row=4)
        self.mediaid_entry.grid(row=5)
        self.result_label.grid(row=6)
        self.go_button.grid(row=7)

    def pick_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        media_id = get_media_id(self.mediaid_entry.get())

        api = connect(username, password)
        comments = get_comments(api, media_id)
        comments_json = convert_to_json(comments)
        usernames = get_usernames(comments_json)
        self.result_label['text'] = random.choice(usernames)


def connect(username, password):
    api = InstagramAPI(username, password)
    api.login()
    return api


def get_media_id(url):
    req = requests.get('https://api.instagram.com/oembed/?url={}'.format(url))
    media_id = req.json()['media_id']
    return media_id


def get_comments(api, media_id):
    has_more_comments = True
    max_id = ''
    comments = []

    # TODO: Clean this up, I don't even know how it works
    while has_more_comments:
        _ = api.getMediaComments(media_id, max_id=max_id)
        # comments' page come from older to newer, lets preserve desc order in full list
        for comment in reversed(api.LastJson['comments']):
            comments.append(comment)
        has_more_comments = api.LastJson.get('has_more_comments', False)

        if has_more_comments:
            max_id = api.LastJson.get('next_max_id', '')
            #time.sleep(2)
    return comments


def convert_to_json(data):
    json_data = json.loads(json.dumps(data))
    return json_data


def get_usernames(data):
    usernames = []
    for comment in data:
        usernames.append(comment['user']['username'])
    return usernames


def main():
    root = Tk()
    RaffleGramGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
