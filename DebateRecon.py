#    _____       _           _         _____
#   |  __ \     | |         | |       |  __ \
#   | |  | | ___| |__   __ _| |_ ___  | |__) |___  ___ ___  _ __
#   | |  | |/ _ \ '_ \ / _` | __/ _ \ |  _  // _ \/ __/ _ \| '_ \
#   | |__| |  __/ |_) | (_| | ||  __/ | | \ \  __/ (_| (_) | | | |
#   |_____/ \___|_.__/ \__,_|\__\___| |_|  \_\___|\___\___/|_| |_|
#
#  A program to be used at NSDA Districts and similar tournaments with codes in order to collect team codes
#  https://github.com/Adamkadaban
#  https://github.com/Nate8888
#
#  Adam Hassan & Nathan Wilk
#
#  Version 1.0 alpha 2/9/19



#take from end of Tabroom URL if you know how code works
#also comment out the input lines


#import stuff#
try:
    from lxml import html
    import requests
    import argparse
except ImportError as msg:
    print("[!] Library not installed: " + str(msg))
    os.system('python -m pip install requests')
    os.system('python -m pip install argparse')
    os.system('python -m pip install lxml')
    exit()
parser = argparse.ArgumentParser()


parser.add_argument("-t", "--tournament", type=str, help="target link", required=True)
parser.add_argument("-r", "--round", type=str, help="checkbox option id", required=True)

args = parser.parse_args()


tourn_id=args.tournament
round_id=args.round
Lookup=""
#put in school name if you want only one school in the output

##Send me prep if you are thankful that you don't have to do this manually##

##Start of the code that debaters should not look at##


# tourn_id=input("Input the tournament ID from the end of the tabroom link\n")
# round_id=input("Input the round ID from the end to the tabroom link\n")
# Lookup=input("If you want to look up a specific school or team, enter the name. Otherwise, press enter\n")
# print("\n")
def secondRequest(urls):
    response2 = requests.get(urls)
    webpage2 = html.fromstring(response2.content)
    number = (str(webpage2.xpath('//h2/text()'))[10:13])
    name = (str(webpage2.xpath('//h4[@class="nospace semibold"]/text()')))
    school = (str(webpage2.xpath('//h6/text()')))
    school = school.replace("\\n", "")
    school = school.replace("\\t", "")
    school = school.replace("\'", "")
    school = school.replace("[", "")
    school = school.replace("]", "")
    newName = name.replace("\\n", "")
    newName = newName.replace("\\t", "")
    newName = newName.replace("\'", " ")
    newName = newName.replace("[", " ")
    newName = newName.replace("]", " ")

    fun=newName.split("&")
    data=[]
    if Lookup in school:
      try:
        print(number +'{:26}'.format(fun[0])+'{:26}'.format(fun[1]) +'{:26}'.format(fun[2])+school)
      except:
        try:
            print(number +'{:26}'.format(fun[0])+'{:26}'.format(fun[1]) +"\t"+school)
        except:
            print(number + '{:26}'.format(+fun[0])+school)


url = "https://www.tabroom.com/index/tourn/postings/round.mhtml"
querystring = {"tourn_id":tourn_id,"round_id":round_id}


headers = {
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    'cookie': "_ga=GA1.2.114986879.1549734299; _gid=GA1.2.784529514.1549734299; _ga=GA1.2.114986879.1549734299; _gid=GA1.2.784529514.1549734299",
    'cache-control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring)

webpage = html.fromstring(response.content)
buyers = webpage.xpath('//a[@class="white smallish padtop padbottom padleft"]/@href') #This gives me all URLS in the page
for x in range(len(buyers)):
    if not "judge" in buyers[x]: #Some urls were not teams, they were judges urls. Therefore Im sorting here
        string = "https://www.tabroom.com"+buyers[x] #Create string to send 2nd request to fetch data
        secondRequest(string) #MEthod that fetches data