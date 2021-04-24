import praw
import json
from colorama import Fore, Style
import time

t     = time.localtime(time.time())
year  = t.tm_year
month = t.tm_mon
day   = t.tm_mday

date = '{}-{}-{}'.format(year, month, day)

MULTISF = '../data/multis-{}.json'.format(date)
SUBSF   = '../data/subs-{}.json'.format(date)
SAVEDF  = '../data/saved-{}.json'.format(date)


subs   = []
multis = []
saved  = []

reddit = praw.Reddit('Backer')
me     = reddit.user.me()

def retrieveSubs():
    print(Fore.BLUE + "[*] ", end='')
    print(Style.RESET_ALL, end='')
    print("Fetching subreddits...")
    for sub in reddit.user.subreddits(limit=None):
        subs.append(sub.display_name)
    print(Fore.GREEN + "[+] ", end='')
    print(Style.RESET_ALL, end='')
    print("done with subreddits")


def retrieveMultis():
    print('')
    print(Fore.BLUE + "[*] ", end='')
    print(Style.RESET_ALL, end='')
    print("Fetching multis...")

    for multi in me.multireddits():
        multisubs = {}
        name = multi.name.split('/')[-1] # Keep the name only
        subs = getSubsForMulti(multi)
        multisubs[name]  = subs
        multisubs["num"] = len(subs) 
        multis.append(multisubs)

    print(Fore.GREEN + "[+] ", end='')
    print(Style.RESET_ALL, end='')
    print("done with multis")


def getSubsForMulti(multi):
    return [sub.display_name for sub in multi.subreddits]


def retrieveSaves():
    print('')
    print(Fore.BLUE + "[*] ", end='')
    print(Style.RESET_ALL, end='')
    print("Fetching saved posts...")

    for post in me.saved(limit=None):
        try:
            data = {}
            data["id"]        = post.id
            data["title"]     = post.title
            data["permalink"] = post.permalink
            data["sub"]       = post.subreddit.display_name
            data["url"]       = post.url
            data["author"]    = post.author.name
            saved.append(data)
        except AttributeError: # Post was deleted
            pass

    print(Fore.GREEN + "[+] ", end='')
    print(Style.RESET_ALL, end='')
    print("done with saved posts")


def writeToFile():
    print('')
    print(Fore.MAGENTA + "[v] ", end='')
    print(Style.RESET_ALL, end='')
    print("Writing to files...")

    with open(MULTISF, 'w') as m:
        json.dump(multis, m)
        

    with open(SUBSF, 'w') as s:
        json.dump(subs, s)
        s.write("\n")
        s.write(str(len(subs)))

    with open(SAVEDF, 'w') as p:
        json.dump(saved, p)
        p.write("\n")
        p.write(str(len(saved)))

    print(Fore.GREEN + ":) ", end='')
    print(Style.RESET_ALL, end='')
    print("Files created succesfully")


def main():
    retrieveSubs()
    retrieveMultis()
    retrieveSaves()
    writeToFile()

if __name__ == '__main__':
    main()
