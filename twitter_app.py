#!/usr/bin/python
from tweepy import Stream
import sys
import tweepy
import argparse
import json
import time
from tweepy.streaming import StreamListener

#globalne premenne
slovo=" "
cas=" "
p_tweet=0
akt_cas=0
fdat=" "
prepinac1=False
prepinac2=False
#main s funkcionalitou argumentparseru
def Main():
        parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=
        '''Ahoj, toto je aplikacia vytvorena pre stahovanie 
        tweetov na zaklade zadaneho slova a nasledne ukladanie 
        do databazi''')
        parser.add_argument('--slovo',help='zadaj slovo pre vyhladavanie',type=str)
        parser.add_argument('--cas',help='zadaj ako dlho ma zber trvat v sec',type=int)
        parser.add_argument('--fdat',help='priepustnost dat',type=int)

	args=parser.parse_args()
        if (args.slovo and args.cas):
		global slovo
		slovo=args.slovo
		global cas
		cas=args.cas
		global prepinac1
		prepinac1=True
        elif (args.fdat and args.cas):
                global fdat
                fdat=args.fdat
		global cas
		cas=args.cas
		global akt_cas
		akt_cas+=fdat
		global prepinac2
		prepinac2=True
	else:
		parser.print_help()
		sys.exit()

if __name__=='__main__':
	Main()

#prihlasenie sa do tweepy api
class Prihlasenie:
        def __init__(self):
                consumer_key="tjThRWOOJ6Uiw9KDXDU5CrOs2"
                consumer_secret="Jefkrrf3yPqI7VW9UKyjSqjDXlArTuzvszD8MPsPNOKzbpMGL8"
                access_token="781103825499328514-5CTT6I7fSorI7F7Y2ugRQg3cjX0fxKu"
                access_secret="92tqcCJu5m56nvgr9qsuS1bUnZErZFZ4gRvNZH0aVAs42"

                self.auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
                self.auth.set_access_token(access_token,access_secret)
                self.api=tweepy.API(self.auth)
                #print(self.api.me().name)
		print("zbieram data")
pri=Prihlasenie()

#samotne spracovavanie dat
class StdOutListener(StreamListener):
	#ako dlho bude stream prichadzat a ako dlho apka pojde v s
	def __init__(self,time_limit=cas):
		self.start_time=time.time()
		self.limit=time_limit
		super(StdOutListener,self).__init__()
       	def on_data(self,data):
#		if(time.time()-self.start_time)>self.limit:
#			return False
		#spracovanie dat s dourazom na slovo
		if (prepinac1==True):
			if(time.time()-self.start_time)>self.limit:
                        	return False
	          	all_data=json.loads(data)
			if slovo in all_data["text"].lower():
				with open("data_NO_SW.json","a")as f:
	                       		f.write(data)
		#vztvaranie zaznamu s frekvenciou dat
		if (prepinac2==True):
	                if(time.time()-self.start_time)>self.limit:
	                        with open("zaznam_US.txt", "a")as f:
					f.write(str(time.time()-self.start_time)+" : "+str(p_tweet)+"\n")
				return False
			global p_tweet
	                p_tweet +=1
	                if((time.time()-self.start_time)/akt_cas)>=1:
				global akt_cas
				akt_cas+=fdat
	                        global p_tweet
	                        with open("zaznam_US.txt", "a")as f:
	                                f.write(str(time.time()-self.start_time)+" : "+str(p_tweet)+"\n")
	                        p_tweet=0 
              	return True
       	def on_error(self,status):
               	print(status)
		return True
       	def on_timeout(self):
               	print()

stream= Stream(pri.auth,StdOutListener())
#prvotne triedenie podla lokacie NO_SW vytvoreny stvorec zo suradnic 
stream.filter(locations=[-124.40918,32.517174,-68.510742,46.65547])
