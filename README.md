# Reddit Tweeter

![issues](https://img.shields.io/github/issues/Miguelo0098/Reddit-Tweeter?style=flat-square) ![forks](https://img.shields.io/github/forks/Miguelo0098/Reddit-Tweeter?style=flat-square) ![stars](https://img.shields.io/github/stars/Miguelo0098/Reddit-Tweeter?style=flat-square) ![license](https://img.shields.io/github/license/Miguelo0098/Reddit-Tweeter?style=flat-square) ![twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2Fmiguelo0098)

Reddit Tweeter is a Twitter bot that uploades images from Reddit. It is based on [tootbot](https://github.com/corbindavenport/tootbot) made by [corbindavenport](https://github.com/corbindavenport).

## Requirements

For Reddit Tweeter to work, you need the following requirements:

- A Twitter developer account
- Access to the Reddit API
- Python3

## Setup

First, clone or download this repository.

```
git clone git@github.com:Miguelo0098/Reddit-Tweeter.git
```

Then, install the dependencies using pip.

```
pip3 install -r requirements.txt
```

After that, you can add the access tokens for Twitter and Reddit to [reddit-tweeter.py](reddit-tweeter.py).

```
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
```

Finally, run [reddit-tweeter.py](reddit-tweeter.py) on a terminal.

```
python3 reddit-tweeter.py
```

## License

----
This project is licensed under the GNU GPL v3 License - see the [LICENSE](LICENSE) file for details.