import twitter
import config
import telegrambot

api = twitter.Api(consumer_key='qbtL7uSdKCf0iRHjk38mMoDTE', consumer_secret='I7cbfxeDosTjrlnt99eBV2bfa3bYf28u0l00RlpgvNv7nUcof0', access_token_key='827817486145949696-3y565mBYrQvdek4p6XbPskietg69KQo', access_token_secret='KjBRjb4eY1DFgsBuWClv9dDRDyaYFYIvPC4dpBWsGCqme')

SCORES = []

def create_dic( fichero ):
    d = {}

    with open( fichero ) as f:
        for line in f:

            line = line.rstrip()
            line = line.replace("\t", " ")
            l = line.split(" ")
            mark = l[-1]
            key = " ".join( l[0:-1] )

            d[key] = int(mark)

    return d

dic = create_dic( "dic.txt" )
dic_es = create_dic("dic_es.txt")

def post_update( string ):

    try:
        s = api.PostUpdate(string)
    except twitter.error.TwitterError:
        s = False
    return s


def track( usernames, hashtags):
    user_ids = []
    global dic
    global dic_es
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
        try:
            print( "User: {user}, Tweet: '{tweet}', Lang: '{lang}'".format(user=tweet.user.screen_name, tweet=tweet.text, lang=tweet.lang))
        except:
            pass

        if ( tweet.lang == 'es'):
            print("Utilizando diccionario spanish")
            score = score_analysis(tweet.text, dic_es)
        else:
            score = score_analysis(tweet.text, dic)

        res = [tweet.user.screen_name, tweet.text, tweet.lang, score]

        SCORES.append( score )

        telegrambot.updateLanguage( tweet.lang )
        telegrambot.updateSentiment( sum(SCORES) / len(SCORES) )

def score_analysis( tweet, dic ):
    tokens = tweet.split(" ")
    cont = 0
    accum = 0

    for t in tokens:
        if t.startswith("#"):
            continue

        cont += 1
        v = dic.get(t, 0)
        print t, v
        accum += v
    return accum


if __name__ == "__main__":
    track(config.users, config.hashtags)
