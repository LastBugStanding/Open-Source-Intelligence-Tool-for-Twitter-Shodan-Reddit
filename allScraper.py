import pandas as pd
import time
import datetime as dt
import csv
import re

SEL=input('--------------- WELCOME --------------------\n'+'TYPE shodan FOR SHODAN SEARCH\n'+
          'TYPE twitter FOR TWITTER SEARCH\n'+
          'TYPE reddit FOR SUBREDDITS SEARCH'+
          'TYPE ANYTHING ELSE TO EXIT\n >> ')
type(SEL)

text_dict={
        'tweets_text': []
        }


results_dict = {
        'query(ALL)': [],
        'keyword(ALL)': [],
        'data_source(ALL)': [],
        'username(Twitter) || title(Reddit) || organization(Shodan)': [],
        'name(Twitter) || ID(Reddit) || domain(Shodan)': [],
        'location(Twitter)': [],
        'creation_date(ALL)': [],
        'text_data(ALL)': [],
        'transport_protocol(Shodan)': [],
        'Match_Check(ALL)': [],
        'isp(Shodan)': [],
        'ip(Shodan)': [],
        'Used_Port(Shodan)': [],
        'post_url(Reddit)': [],
        'post_score(Reddit)': [],
        'hour_of_day(ALL)':[],
        'tweet_score': []
}
#keyword=input('Enter Keyword to Match (Searches for text_data) : \n')
#type(keyword)

kword = []

if SEL == 'shodan':
    #! /usr/bin/python3.6
    #! coding: utf8

    import shodan

    SHODAN_API_KEY = "SHODAN_API_KEY"

    api = shodan.Shodan(SHODAN_API_KEY)

    query=input("Please Enter Search Query : \n")
    type(query)
    data_source = 'SHODAN'
    
    keyword=input('Enter Keyword to Match (Searches for text_data) : \n')
    type(keyword)
    
    results = api.search(query)
    

    for service in results['matches']:
        kword.append(keyword)
        results_dict['query(ALL)'].append(query)
        results_dict['keyword(ALL)'].append(keyword)
        results_dict['data_source(ALL)'].append(data_source)
        results_dict['text_data(ALL)'].append(service['data'].replace("\n","|"))
        results_dict['name(Twitter) || ID(Reddit) || domain(Shodan)'].append(service['domains'])
        results_dict['username(Twitter) || title(Reddit) || organization(Shodan)'].append(service['org'])
        results_dict['ip(Shodan)'].append(service['ip_str'])
        results_dict['Used_Port(Shodan)'].append(service['port'])
        results_dict['transport_protocol(Shodan)'].append(service['transport'])
        results_dict['isp(Shodan)'].append(service['isp'])
        
        post_list = results_dict['text_data(ALL)']
        
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(service['timestamp'],'%Y-%m-%dT%H:%M:%S.%f'))
        results_dict['creation_date(ALL)'].append(ts)
        
        hod = time.strftime('%H:%M:%S', time.strptime(service['timestamp'],'%Y-%m-%dT%H:%M:%S.%f'))
        results_dict['hour_of_day(ALL)'].append(hod)

        results_dict['location(Twitter)'].append("---")
        results_dict['post_url(Reddit)'].append("---")
        results_dict['post_score(Reddit)'].append("---")
        results_dict['tweet_score'].append('---')
        matcher = [keyword in s for s in post_list]

    for item in matcher:
        if item ==True:
            results_dict['Match_Check(ALL)'].append('!!!Match!!!')
        elif item == False:
            results_dict['Match_Check(ALL)'].append('---Neatural---')
            


    results_data = pd.DataFrame(results_dict)


    results_data.to_csv('/home/batu/Desktop/project/allData.csv',sep="¶", index=False, encoding="utf-8",header=True, quotechar="'")

#-----------------------------------------------------------------------------------------------------------------------------------------

elif SEL == 'twitter':
    import twitter
    
    api = twitter.Api(consumer_key='consumer_key',
                      consumer_secret='consumer_secret',
                      access_token_key='access_token_key',
                      access_token_secret='access_token_secret')




    selection=input('------------- Welcome ---------------\n 1-) Status Search (Start to Type with # for hashtag Search)\n2-) User Search \n')
    type(selection)

    #--------------------------------------------------------------------------------------------------------------------------------------

    if selection == '1':
        data_source= 'TWITTER'
        query=input("Please Enter The Term You Want to Search(start with # to search a hashtag) : \n")
        type(query)

        keyword=input('Enter Keyword to Match (Searches for text_data) : \n')
        type(keyword)

        no=input("Number of Results (Max 100) : \n")
        type(no)

        dil=input('Language of Search(Default is None. Exp => en,tr,ru...): \n')
        type(dil)

        tip=input('Type of results. mixed, recent or popular. Default is mixed :\n')
        type(tip)


        results = api.GetSearch(term=query, count=no, lang=dil, result_type=tip, include_entities=True, return_json=True)
        #print(results)

       # ------------------ TO IMPORT KEYWORD FROM EXTERNAL CSV DATA TO ANALYZE AND MATCH PRE-DEFINED KEYWORDS -----------------------------
        keywords = [] 
        
        key_sel=input('Please Select a File to Load Keywords for Matching\n1-) negative-words.txt\n2-) positive-words.txt\n>>')
        type(key_sel)

        if key_sel == '1':
            with open(r'/home/batu/Desktop/project/negative-words.txt') as f:
                for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
                    keywords += row
        if key_sel == '2':
            with open(r'/home/batu/Desktop/project/positive-words.txt') as f:
                for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
                    keywords += row

#-----------------------------------------------------------------------------------   TWEET SCORE CREATING ----------------
        
#--------------------------------------------------------------------------------------------------------     
        i=0
        for service in results['statuses']: 
            results_dict['Match_Check(ALL)'].append('---')
            results_dict['keyword(ALL)'].append(keyword)
            results_dict['query(ALL)'].append(query)
            results_dict['data_source(ALL)'].append(data_source)
            abc = service['user']
            results_dict['username(Twitter) || title(Reddit) || organization(Shodan)'].append(abc['screen_name'])
            results_dict['name(Twitter) || ID(Reddit) || domain(Shodan)'].append(abc['name'])
            
            
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(service['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            results_dict['creation_date(ALL)'].append(ts)
            
            hod = time.strftime('%H:%M:%S', time.strptime(service['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            results_dict['hour_of_day(ALL)'].append(hod)
            
            results_dict['location(Twitter)'].append(abc['location'])
            results_dict['text_data(ALL)'].append(service['text'].replace("\n","|"))
            post_list = results_dict['text_data(ALL)']

            results_dict['transport_protocol(Shodan)'].append("---")
            results_dict['isp(Shodan)'].append("---")
            results_dict['ip(Shodan)'].append("---")
            results_dict['Used_Port(Shodan)'].append("---")
            results_dict['post_url(Reddit)'].append("---")
            results_dict['post_score(Reddit)'].append("---")
            results_dict['tweet_score'].append('---')
#            i+=1
        results_data = pd.DataFrame(results_dict)
#---------------------------------------------------------------------------------------------
        for service in results['statuses']:
            text_dict['tweets_text'].append(service['text'])
        td=pd.DataFrame(text_dict)
        rx = '(?i)(?P<keywords>{})'.format('|'.join(re.escape(kw) for kw in keywords))

        matches = td['tweets_text'].str.extractall(rx)

        dummies = pd.get_dummies(matches).max(level=0)
        
        result = results_data.join(dummies, how='left')

        result['tweet_score'] = dummies.sum(axis=1).astype(int).astype(str)

        tweet_scores = result["tweet_score"].tolist()
        
        results_dict = {
        'query(ALL)': [],
        'keyword(ALL)': [],
        'data_source(ALL)': [],
        'username(Twitter) || title(Reddit) || organization(Shodan)': [],
        'name(Twitter) || ID(Reddit) || domain(Shodan)': [],
        'location(Twitter)': [],
        'creation_date(ALL)': [],
        'text_data(ALL)': [],
        'Match_Check(ALL)': [],
        'transport_protocol(Shodan)': [],
        'isp(Shodan)': [],
        'ip(Shodan)': [],
        'Used_Port(Shodan)': [],
        'post_url(Reddit)': [],
        'post_score(Reddit)': [],
        'hour_of_day(ALL)':[],
        'tweet_score': []
}
        
        
        i=0
        for service in results['statuses']: 

            results_dict['keyword(ALL)'].append(keyword)
            results_dict['query(ALL)'].append(query)
            results_dict['data_source(ALL)'].append(data_source)
            abc = service['user']
            results_dict['username(Twitter) || title(Reddit) || organization(Shodan)'].append(abc['screen_name'])
            results_dict['name(Twitter) || ID(Reddit) || domain(Shodan)'].append(abc['name'])
            
            
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(service['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            results_dict['creation_date(ALL)'].append(ts)
            
            hod = time.strftime('%H:%M:%S', time.strptime(service['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            results_dict['hour_of_day(ALL)'].append(hod)
            
            results_dict['location(Twitter)'].append(abc['location'])
            results_dict['text_data(ALL)'].append(service['text'].replace("\n","|"))
            post_list = results_dict['text_data(ALL)']

            results_dict['transport_protocol(Shodan)'].append("---")
            results_dict['isp(Shodan)'].append("---")
            results_dict['ip(Shodan)'].append("---")
            results_dict['Used_Port(Shodan)'].append("---")
            results_dict['post_url(Reddit)'].append("---")
            results_dict['post_score(Reddit)'].append("---")
            results_dict['tweet_score'].append(tweet_scores[i])
            i+=1
        
        
        matcher = [keyword in s for s in post_list]

        for item in matcher:
            if item ==True:
                results_dict['Match_Check(ALL)'].append('!!!Match!!!')
            elif item == False:
                results_dict['Match_Check(ALL)'].append('---Neatural---')
        
        
        results_data = pd.DataFrame(results_dict)

        results_data.to_csv('/home/batu/Desktop/project/allData.csv',sep="¶", index=False, encoding="utf-8",header=True, quotechar="'")
    #-----------------------------------------------------------------------------------------------

    if selection == '2':
        
        data_source= 'TWITTER_USER'
        screenName=input('Enter User name with @ : \n')
        type(screenName)

        keyword= 'abc'

        userResults = api.GetUser(screen_name=screenName, return_json=True)
        results_dict['query(ALL)'].append(screenName)
        results_dict['data_source(ALL)'].append(data_source)
        
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(userResults['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        results_dict['creation_date(ALL)'].append(ts)
        
        hod = time.strftime('%H:%M:%S', time.strptime(userResults['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        results_dict['hour_of_day(ALL)'].append(hod)
        
        results_dict['text_data(ALL)'].append(userResults['description'])
        results_dict['location(Twitter)'].append(userResults['location'])
        results_dict['name(Twitter) || ID(Reddit) || domain(Shodan)'].append(userResults['name'])
        results_dict['username(Twitter) || title(Reddit) || organization(Shodan)'].append(userResults['screen_name'])
        kword.append(keyword)
        results_dict['keyword(ALL)'].append("---")
        

        results_dict['transport_protocol(Shodan)'].append("---")
        results_dict['isp(Shodan)'].append("---")
        results_dict['ip(Shodan)'].append("---")
        results_dict['Used_Port(Shodan)'].append("---")
        results_dict['post_url(Reddit)'].append("---")
        results_dict['post_score(Reddit)'].append("---")
        results_dict['tweet_score'].append('---')
        
        post_list = results_dict['text_data(ALL)']
        
        matcher = [keyword in s for s in post_list]

        for item in matcher:
            if item ==True:
                results_dict['Match_Check(ALL)'].append('!!!Match!!!')
            elif item == False:
                results_dict['Match_Check(ALL)'].append('---Neatural---')

        results_data = pd.DataFrame(results_dict)
        results_data.to_csv('/home/batu/Desktop/project/allData.csv',sep="¶", index=False, encoding="utf-8",header=True, quotechar="'")

#-------------------------------------------------------------------------------------------------------------------------------------------------

elif SEL == 'reddit':
    #! /usr/bin/python3.6
    # coding: utf8
    import praw
    data_source= 'REDDIT'
    query=input("Please Enter The Subreddit You Want to Search : \n")
    type(query)

    keyword=input('Enter Keyword to Match (Searches for text_data) : \n')
    type(keyword)

    gettit = praw.Reddit(client_id='client_id',
                         client_secret='client_secret-foY',
                         password='password',
                         user_agent='user_agent',
                         username='username')


    subreddit = gettit.subreddit(query)

    search_subreddit = subreddit.search(query)


    #for submission in subreddit.search(query):
     #   print(submission.title, submission.id)


    for submission in search_subreddit:

       kword.append(keyword)
       results_dict['data_source(ALL)'].append(data_source)
       results_dict['keyword(ALL)'].append(keyword)
       post_list = results_dict['text_data(ALL)']
       results_dict["query(ALL)"].append(query)

       if submission.title == "":
           results_dict["username(Twitter) || title(Reddit) || organization(Shodan)"].append("N.D")
       else:
           results_dict["username(Twitter) || title(Reddit) || organization(Shodan)"].append(submission.title.replace("\n","|"))


       if submission.score == "":
           results_dict["post_score(Reddit)"].append(0)
       else:
           results_dict["post_score(Reddit)"].append(submission.score)

       if submission.id == "":
           results_dict["name(Twitter) || ID(Reddit) || domain(Shodan)"].append("N.D")
       else:
           results_dict["name(Twitter) || ID(Reddit) || domain(Shodan)"].append(submission.id)

       if submission.created == "":
           results_dict["creation_date(ALL)"].append("-")
       else:
           date = dt.datetime.utcfromtimestamp(submission.created)
           results_dict["creation_date(ALL)"].append(date)
           hod = time.strftime('%H:%M:%S', time.strptime(str(date),'%Y-%m-%d %H:%M:%S'))
           results_dict['hour_of_day(ALL)'].append(hod)

       if submission.selftext == "":
           results_dict["text_data(ALL)"].append("N.D")
       else:
           results_dict["text_data(ALL)"].append(submission.selftext.replace("\n","|"))

       if submission.url == "":
           results_dict["post_url(Reddit)"].append("N.D")
       else:
           results_dict["post_url(Reddit)"].append(submission.url)


       results_dict['location(Twitter)'].append("---")
       results_dict['transport_protocol(Shodan)'].append("---")
       results_dict['isp(Shodan)'].append("---")
       results_dict['ip(Shodan)'].append("---")
       results_dict['Used_Port(Shodan)'].append("---")
       results_dict['tweet_score'].append('---')


       matcher = [keyword in s for s in post_list]

    for item in matcher:
        if item ==True:
            results_dict['Match_Check(ALL)'].append('!!!Match!!!')
        elif item == False:
            results_dict['Match_Check(ALL)'].append('---Neatural---')
            

    #change number for end of the file to log different files. output to the same folder and in config file as a path use /home/batu/Data/*.csv to log every new document
    results_data = pd.DataFrame(results_dict)

    results_data.to_csv('/home/batu/Desktop/project/allData.csv',sep="¶", index=False, encoding="utf-8",header=True, quotechar="'")
#-------------------------------------------------------------------------------------------------------------------------------------


else:
    print ("------------- GOODBYE ----------\n --------------- EXITING --------------")
    exit()
