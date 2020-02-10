import praw
import utils



def main():

    reddit = praw.Reddit('Backer')


    # Obtain an instance of myself
    # Obtain all the subs I've joined
    # Obtain all the multis I've joined or created
    # Obtain all my saved posts
    me = reddit.user.me()
    
    mymultis = me.multireddits()
    for multi in mymultis:
        print(multi)



if __name__ == '__main__':
    main()
