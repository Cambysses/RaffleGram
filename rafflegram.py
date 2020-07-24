from InstagramAPI import InstagramAPI
import requests
import random
import json
from tkinter import Tk, Label, Button, Entry, Checkbutton, IntVar


class RaffleGramGUI:

    def __init__(self, master):
        self.master = master
        master.title("RaffleGram")
        self.users = []

        self.username_label = Label(master, text="Username:")
        self.username_entry = Entry(master)
        self.password_label = Label(master, text="Password:")
        self.password_entry = Entry(master)
        self.mediaid_label = Label(master, text="Post URL:")
        self.mediaid_entry = Entry(master)
        self.result_label = Label(master)
        self.removeDuplicates_checkVar = IntVar()
        self.removeDuplicates_check = Checkbutton(master, text="Remove duplicates", variable=self.removeDuplicates_checkVar)
        self.go_button = Button(master, text="Submit", command=self.pick_user)
        self.refresh_button = Button(master, text="Refresh", command=self.refresh)

        self.username_label.grid(row=0, columnspan=2)
        self.username_entry.grid(row=1, columnspan=2)
        self.password_label.grid(row=2, columnspan=2)
        self.password_entry.grid(row=3, columnspan=2)
        self.mediaid_label.grid(row=4, columnspan=2)
        self.mediaid_entry.grid(row=5, columnspan=2)
        self.result_label.grid(row=6, columnspan=2)
        self.removeDuplicates_check.grid(row=7)
        self.go_button.grid(row=8, column=0)
        self.refresh_button.grid(row=8, column=1)

    def pick_user(self):
        api = connect(self.username_entry.get(), self.password_entry.get())
        comments = get_comments(api, get_media_id(self.mediaid_entry.get()))
        comments_json = convert_to_json(comments)
        self.users = get_usernames(comments_json)

        # Remove duplicate entries if checkbox checked.
        if self.removeDuplicates_checkVar.get():
            self.remove_duplicates()

        # Get new random name from existing list.
        self.refresh()

        for u in self.users: print(u)

    def refresh(self):
        self.result_label['text'] = random.choice(self.users)

    def remove_duplicates(self):
        self.users = list(dict.fromkeys(self.users))


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

    while has_more_comments:
        _ = api.getMediaComments(media_id, max_id=max_id)
        for comment in api.LastJson['comments']:
            comments.append(comment)
        has_more_comments = api.LastJson.get('has_more_comments', False)

        if has_more_comments:
            max_id = api.LastJson.get('next_max_id', '')

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
