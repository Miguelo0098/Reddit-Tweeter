import twitter
import os
import time
import csv 
import praw
from getmedia import get_media

# Default values
CACHE_CSV = 'cache.csv' # Cache file to log tweets
DELAY_BETWEEN_TWEETS = 60*60 # Seconds between tweets
POST_LIMIT = 15 #Number of posts to get from the subreddit

# Reddit related variables
SUBREDIT_TO_MONITOR = ''
REDDIT_AGENT = ''
REDDIT_CLIENT_SECRET = ''
REDDIT_CLIENT_ID = ''

# Twitter related variables
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

# Gets a post dictionary from a certain subreddit
def get_reddit_posts(subreddit):
    post_dict = {}
    print('[ OK ] Getting post from r/', subreddit)

    # Iterating submissions
    for submission in subreddit.hot(limit=POST_LIMIT):
        if submission.stickied:
            # Stickied submissions are skipped
            print('[ OK ] Skipping ', submission.id, ' because it is stickied')
            continue
        else:
            # Adds submission to the dictionary
            post_dict[submission.id] = submission  
    return post_dict

# Makes a twitter caption from a reddit submission
def get_twitter_caption(submission):
    # Gets the max number of characters for a tweet
    twitter_length = 280 - len(submission.shortlink) - len('(Via: )') - 4
    # A caption equals the title + the link of the reddit submission
    if len(submission.title) < twitter_length:
        twitter_caption = submission.title + ' (Via: ' + submission.shortlink + ')'
    else:
        twitter_caption = submission.title[:twitter_length] + ' (Via: ' + submission.shortlink + ')'
    return twitter_caption

# Gets a subreddit object
def setup_connection_reddit(subreddit):
    print('[ OK ] Setting up connection with Reddit...')
    r = praw.Reddit(user_agent=REDDIT_AGENT,
                    client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_CLIENT_SECRET)
    return r.subreddit(subreddit)

# Checks if a submission was already posted
def duplicate_check(id):
    value = False
    with open(CACHE_CSV, 'rt', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        # Iterates the cache file to check if the submission id is there
        for row in reader:
            if id in row:
                value = True
    f.close()
    return value

# Saves the id, time and url of the post in the cache file
def log_post(id, post_url):
    with open(CACHE_CSV, 'a', newline='') as cache:
        date = time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")
        wr = csv.writer(cache, delimiter=',')
        wr.writerow([id, date, post_url])
    cache.close()

# Tweets every post in the post dictionary with an image
def make_post(post_dict):
    for post in post_dict:
        post_id = post_dict[post].id
        if not duplicate_check(post_id):
            # Gets the media file from the url
            media_file = get_media(post_dict[post].url)
            try:
                api = twitter.Api(CONSUMER_KEY,
                                  CONSUMER_SECRET,
                                  ACCESS_TOKEN,
                                  ACCESS_TOKEN_SECRET)
                caption = get_twitter_caption(post_dict[post])
                if media_file:
                    print('[ OK ] Posting this on twitter with media: ', caption)
                    tweet = api.PostUpdate(caption, media=media_file)
                    try:
                        os.remove(media_file)
                        print('[ OK ] Media File deleted: ', media_file)
                    except BaseException as e:
                        print('[EROR] Error while deleting media file: ', str(e))

                log_post(post_id, post_dict[post].shortlink)
                print('[ OK ] Sleeping for', DELAY_BETWEEN_TWEETS, 'seconds')
                time.sleep(DELAY_BETWEEN_TWEETS)
            except BaseException as e:
                print('[EROR] Error while posting tweet: ', str(e))
                # The post is logged in order to not repeat the same error
                log_post(post_id, post_dict[post].shortlink)
        else:
            print('[ OK ] Skipping', post_id, 'because it was already posted')
    pass


# Main process
while True:
    # Creates a log file if it does not exists
    if not os.path.exists(CACHE_CSV):
        with open(CACHE_CSV, 'w', newline='') as cache:
            default = ['Reddit post ID', 'Date and time', 'Post link']
            wr = csv.writer(cache)
            wr.writerow(default)
        print('[ OK ] Cache file not found, created a new one')
        cache.close()
    # Gets posts and tweets them
    try:
        subredit = setup_connection_reddit(SUBREDIT_TO_MONITOR)
        post_dict = get_reddit_posts(subredit)
        make_post(post_dict)
    except BaseException as e:
        print('[EROR] Error in main process: ', str(e))
        print(e.args)
        exit()
    print('[ OK ] Restarting main process...')
