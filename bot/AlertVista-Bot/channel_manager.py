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
    def __init__(self,platform,**id) -> None:
        self.platform=platform
        if("https://www.youtube.com/channel/" in id['curl']or"https://www.youtube.com/" in id['curl']):
            # link will be validated while getting channelId
            self.ID=id['curl']
            return self.validate(self.ID)
        else:
            if(id['ID'][0]!="@"):
               id['ID']=f'@{id['ID']}'
            self.ID=id['ID']
            return self.nset(self)
        #self.set()
    def ytJson(self,endpoints):
        soup=BeautifulSoup(Session().get(endpoints,cookies={'CONSENT':"YES+1"}).text,"html.parser")
        ndata=search(r"var ytInitialData = ({.*});",str(soup.prettify())).group(1)
        json_data=loads(ndata)
        print(json_data)
        pass
    def validate(self,url):
        try:
            status=self.ytJson(url)
        except:
            return(False)

        #here we will pass the link that is possible which is gonna be random pages

        pass
    def create(self,**kwarg):
        try:
            with open("bot/data/channels.json","w")as fs:
                
                fs.close()
            return True
        except:
            return False
    def nset(self):
        with open("bot/data/channels.json","r")as fs:
            ofl=loads(fs.read())
            if(self.ID not in ofl):
                print("not found")
                if(self.validate(f'https://www.youtube.com/{self.ID}/videos')!=None or self.validate(f'https://www.youtube.com/{self.ID}/videos')!=False):
                    return(self.create())
                #first validate then generate and from validate it will jemp to create itself
                pass
            elif(self.ID in ofl):
                #add the user server details where to send the alert
                #instead of modifying it here it will send to create using kwarg
                ofl[f'{self.ID}']['platform']['Discord'].append(f'{self.platform}')
                self.create()
                return(True)
            fs.close()
        pass
    
run('server',ID="",curl="https://www.youtube.com/@JennyslecturesCSIT")#https://www.youtube.com/@JennyslecturesCSIT