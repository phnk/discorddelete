import json, requests, time

print("--- Discord Channel-Message Deleter ---")
print("Removes messages from a channel which contains defined words")
auth_token = input("Auth Token: ")
channel_id = input("Channel ID: ")
words = input("Words (seperate with whitespaces): ").split(" ")

def get_all_messages(auth, id):
    prev = []
    # lazy way of getting the first messages. Channels with too many messages lead to "recursion depth exceeded".
    messages = json.loads(requests.get("http://canary.discordapp.com/api/v6/channels/" + id + "/messages", headers={"authorization": auth}, params={"limit": 100}).content)
    last = sorted(messages, key=lambda x: x["timestamp"], reverse=True)[-1]["id"]
    prev.append(messages)

    while True:
        messages = json.loads(requests.get("http://canary.discordapp.com/api/v6/channels/" + id + "/messages", headers={"authorization": auth}, params={"before" : last, "limit" : 100}).content)
        prev.append(messages)
        last = sorted(messages, key=lambda x: x["timestamp"], reverse=True)[-1]["id"]
        print("current number of parsed messages: {}".format(len(prev) * 100))
        if len(messages) < 100:
            return prev


def _delete_all(auth, id, messages, words):
    for message in messages:
        for m in message:
            for word in words:
                # to match exact words. will not match "cat" if the message is cathrine.
                if word.lower() in m["content"].lower().split(" "):
                    delete_message(auth, id, m)

def delete_message(auth, id, message):
    isDeleted = False
    print("Deleting message: {}. From user: {}".format(message["content"], message["author"]["username"]))
    while isDeleted == False:
        n = requests.delete("https://discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"], headers={"authorization": auth})
        print(n)
        # if the message doesnt exist, we already deleted it
        if n.status_code == 204 or n.status_code == 404:
            isDeleted = True
        else:
            time.sleep(5.0)

messages = get_all_messages(auth_token, channel_id)
_delete_all(auth_token, channel_id, messages, words=words)