import twitter

api = twitter.Api(consumer_key='qbtL7uSdKCf0iRHjk38mMoDTE', consumer_secret='I7cbfxeDosTjrlnt99eBV2bfa3bYf28u0l00RlpgvNv7nUcof0', access_token_key='827817486145949696-3y565mBYrQvdek4p6XbPskietg69KQo', access_token_secret='KjBRjb4eY1DFgsBuWClv9dDRDyaYFYIvPC4dpBWsGCqme')

def post_update( string ):
    
    try: 
        s = api.PostUpdate(string)
    except twitter.error.TwitterError:
        s = False
    return s

def track( usernames, hashtags ):
    user_ids = []

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

users = [
            "@S1d3Ch4nn3l_",
        ]
hashtags = [
        ]

track( users, hashtags )

