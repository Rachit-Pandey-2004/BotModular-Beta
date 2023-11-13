'''
Author: Rachit-Pandey-2004
licence: None
file: channel Id managment
version: 0.1-beta
support: video-notification
'''
##CONCERN WHAT IF SERVER ID IS NOT INVALID !!!
from json import loads,dumps
from bs4 import BeautifulSoup
from re import search
from requests import Session,get
class run():
    def __init__(self,**kwarg) -> None:
        self.platform=kwarg['server']
        self.ID=kwarg
        
    def ytJson(self,endpoints):
        try:
            soup=BeautifulSoup(Session().get(endpoints,cookies={'CONSENT':"YES+1"}).text,"html.parser")
            ndata=search(r"var ytInitialData = ({.*});",str(soup.prettify())).group(1)
            return loads(ndata)
        except:
            return False

    def validate(self,url):
        remote_data=self.ytJson(url)
        if(remote_data==False):
            return False
        else:
            #return channel ID
            send=remote_data['header']['c4TabbedHeaderRenderer']['channelHandleText']['runs'][0]['text']
            return(send)
        
    def create(self,D):
        try:
            with open("bot/data/channels.json","w")as fs:
                fs.write(dumps(D))
                fs.close()
            return True
        except:
            return False
    def nset(self):
        if('curl'in self.ID):
            if("https://www.youtube.com/channel/" in self.ID['curl']or"https://www.youtube.com/" in self.ID['curl']):
                # link will be validated while getting channelId  
                status=self.validate(self.ID['curl'])
                if(status != False):
                    self.ID['ID']=status
                else:
                    return False
        else:
            if(self.ID['ID'][0]!="@"):
               self.ID['ID']=f'@{self.ID['ID']}'
            #break points   
            if(self.validate(f'https://www.youtube.com/{self.ID['ID']}')==False):
                print("checkpost")
    
                #here checking if wrong channel then it will terminate everything
                return False
        ## @@ every thing is already validated
        with open("bot/data/channels.json","r")as fs:
    
            ofl=loads(fs.read())
            if(self.ID['ID'] not in ofl):
                print("not found")
                #create whole db
                ofl[f'{self.ID['ID']}']={
                    "videos": {
                            "last_checked": "null",
                            "stack": []
                    },
                    "shorts": {
                            "last_checked": "null",
                            "stack": []
                    },
                    "servers": {
                            "discord_channel_Id": [f'{self.platform}']
                        }
                }
                fs.close()
                return(self.create(ofl))
            
            elif(self.ID['ID'] in ofl):
                #add server   ---done
                #but if server is also present
                if(self.platform not in ofl[f'{self.ID['ID']}']['servers']['discord_channel_Id']):
                    ofl[f'{self.ID['ID']}']['servers']['discord_channel_Id'].append(self.platform)
                    return(self.create(ofl))
                fs.close()
                print("server is present")
                return(True)
            else : 
                fs.close()
                return(False)
            
        
#print(run(server='server',curl="https://www.youtube.com/@JennyslecturesCSIT").nset())#https://www.youtube.com/@JennyslecturesCSIT
#print(run(server='server0',ID="@regurmaster3519").nset())
#print(run(server='server0',curl='https://www.youtube.com/watch?v=HKTyOUx9Wf4').nset())  ~failed for video link