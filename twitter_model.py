import twitter
import config
import telegrambot

api = twitter.Api(consumer_key='qbtL7uSdKCf0iRHjk38mMoDTE', consumer_secret='I7cbfxeDosTjrlnt99eBV2bfa3bYf28u0l00RlpgvNv7nUcof0', access_token_key='827817486145949696-3y565mBYrQvdek4p6XbPskietg69KQo', access_token_secret='KjBRjb4eY1DFgsBuWClv9dDRDyaYFYIvPC4dpBWsGCqme')

SCORES = []

def create_dic():
    d = {}

    with open("dic.txt") as f:
        for line in f:
        
            l = line.split(" ")
            mark = l[-1]
            key = " ".join( l[0:-1] ) 

            d[key] = int(mark)

    return d

dic = create_dic()

def post_update( string ):

    try:
        s = api.PostUpdate(string)
    except twitter.error.TwitterError:
        s = False
    return s

def track( usernames, hashtags):
    user_ids = []
    global dic
    global SCORES

    if len( usernames ):
        for user in usernames:
            u = api.GetUser( screen_name=user )
            print("User ID: " + str(u.id) )
            user_ids.append( str(u.id) )

    stream =  api.GetStreamFilter( follow = user_ids, track=hashtags )

    for line in stream:

        if 'in_reply_to_status_id' in line:
            tweet = twitter.Status.NewFromJsonDict( line )

        #print(tweet)
        print( "User: {user}, Tweet: '{tweet}', Lang: '{lang}'".format(user=tweet.user.screen_name, tweet=tweet.text, lang=tweet.lang))
        

        score = score_analysis(tweet.text, dic)
        res = [tweet.user.screen_name, tweet.text, tweet.lang, score]
        
        SCORES.append( score )
       
        telegrambot.updateFlag( tweet.lang )
        telegrambot.updateSentiment( sum(SCORES) / len(SCORES) )
        print(res)
    

def score_analysis( tweet, dic ):
    tokens = tweet.split(" ")
    cont = 0
    accum = 0

    for t in tokens:
        cont += 1
        v = dic.get(t, 0)
        accum += v
        accum = accum / cont

    return accum
        

if __name__ == "__main__":
    track(config.users, config.hashtags)

    
