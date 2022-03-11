
from tweepy import Client
from json import load,dump
errors = {}
def get_api_data() -> None :
    f = open('config.json')
    api_data = load(f)
    f.close()
    global API_KEY,API_KEY_SECRET,BEARER_TOKEN,ACCESS_TOKEN,ACCESS_TOKEN_SECRET
    API_KEY = api_data['API_KEY']
    API_KEY_SECRET = api_data['API_KEY_SECRET']
    BEARER_TOKEN = api_data['BEARER_TOKEN']
    ACCESS_TOKEN = api_data['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = api_data['ACCESS_TOKEN_SECRET']

def get_client() -> Client:
    client = Client(
                consumer_key = API_KEY,
                consumer_secret = API_KEY_SECRET,
                bearer_token = BEARER_TOKEN,
                access_token = ACCESS_TOKEN,
                access_token_secret = ACCESS_TOKEN_SECRET
                )
    return client

def get_tweets(client:Client,account_id:str) -> dict:
    query = f"from:{account_id} is:retweet" # only gives retweets for all tweets remove is:retweet.
    # query = "from:{account_id} -is:retweet" # To exclude  retweets # replace -is to is for only retweets
    res =client.search_recent_tweets(query=query,max_results = 100,expansions = ['referenced_tweets.id'])
    tweets = {} 
    for tweet in res.data:
        for referenced_tweet in tweet.referenced_tweets:
            tweets.update({tweet.id:referenced_tweet.id})
    return tweets

# delete a tweet
def delete_tweets(client:Client,tweets:dict) -> None:
    for tweet_id in tweets.keys():
        res = client.delete_tweet(id=tweet_id)
        if res.data['deleted'] :
            print(tweet_id,"deleted successfully.") 
        else:
            print(tweet_id, "deleted unsuccessfully.")
            errors.update({tweet_id:'deleted unsuccessfully.'})

# retweet a tweet 
def retweet_tweets(client:Client,tweets:dict) -> None:
    for tweet_id in tweets.values():
        res = client.retweet(tweet_id=tweet_id,user_auth=True)
        if res.data['retweeted'] :
            print(tweet_id, "retweeted successfully.") 
        else:
            print(tweet_id, "retweeted unsuccessfully.")
            errors.update({tweet_id:'retweeted unsuccessfully.'})

def log_errors() -> None: # log errors to error log.txt
    f = open('error log.txt','w')
    dump(errors,f)
    f.close()

if __name__ == '__main__':
    account_id = "realDonaldTrump"
    get_api_data()
    client = get_client()
    tweets = get_tweets(client,account_id)
    delete_tweets(client,tweets)
    retweet_tweets(client,tweets)
    if len(errors.items()) != 0:
        log_errors()


