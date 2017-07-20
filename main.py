import json, requests, time

print "--- Discord Channel-Message Deleter ---"
print "clears all of your messages in a channel"
print "in order for this script to work properly the channel id, auth token, and username is required"
username = raw_input("Username: ")
auth_token = raw_input("Auth Token: ")
channel_id = raw_input("Channel ID: ")
delete_from_all_users = True if raw_input("Delete messages from other users (y/n): ") == "y" else False

def get_all_messages(auth, id, last="", prev=[]): # recursively find all messages in a channel, 100 at a time
    if not last: # first method call, start from beginning (might be able to remove)
        messages = json.loads(requests.get("http://canary.discordapp.com/api/v6/channels/" + id + "/messages", headers={"authorization": auth}, params={"limit": 100}).content)
    else:
        messages = json.loads(requests.get("http://canary.discordapp.com/api/v6/channels/" + id + "/messages", headers={"authorization": auth}, params={"before" : last, "limit" : 100}).content)

    prev = prev + messages

    if len(messages) < 100:
        print "Got to end of channel at " + str(len(prev)) + " messages"
        return prev
    else:
        oldest = sorted(messages, key=lambda x: x["timestamp"], reverse=True)[-1]
        return get_all_messages(auth, id, last=oldest["id"], prev=prev)

def delete_all(auth, id, user, messages):
    print "Deleting all messages in Channel ID [" + id + "] from the Username: " + user
    for message in messages:
        time.sleep(2.0) 
        if delete_from_all_users:
            isDeleted = False
            
            while isDeleted == False:
                print "Message: ["+ message["id"] + "], deleting..."
                n = requests.delete("http://canary.discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"], headers={"authorization": auth})
                print n
                if n.status_code == 204:
                    isDeleted = True
                else:
                    time.sleep(5.0) 
        else:
            print "Message: ["+ message["id"] + "], deleting..."
            if (message["author"]["username"] == user):
                isDeleted = False
            
                while isDeleted == False:
                    n = requests.delete("http://canary.discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"], headers={"authorization": auth})
                    print n
                    if n.status_code == 204:
                        isDeleted = True
                    else:
                        time.sleep(5.0) 
    print "all messages deleted"

delete_all(auth_token, channel_id, username, get_all_messages(auth_token, channel_id))
