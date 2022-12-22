#coding = utf-8
import os,sys
try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests && python file.py')
logo="""
               88.88 88   88                  88.         88
         88                     88.            88.          88 88
      88   ##    ##         88        88.            88.    88
      88    ##    ##    #   88    88.             88.       88
        88 88 88    ## ##    88.                88.         88
                      88    ##   88   88.           88. 88 88 88
                     88    ## 88         88.       88.              88
        88 88 88          88               88.   88.               88
--------------------------------------------------
 Author:BOLBIZUA
 Version: 1.0
--------------------------------------------------"""
def update():
    try:
        check_update = requests.get('https://raw.githubusercontent.com/hop09/extract_ids/main/version.txt').text
        if float(check_update) == 1.0:
            main()
        else:
            print('\n An new version is available, fetching new version please wait ...')
            os.system('rm -rf file32 file64 && python file.py')
    except:
        print('\n No internet connection !')
        exit()
def main():
    try:
        accessToken = open('token.txt','r').read()
        cookies = open('cookie.txt','r').read()
    except FileNotFoundError:
        login()
    prepare_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Cookie':cookies}
    try:
        me = requests.get(f'https://b-graph.facebook.com/me?access_token={accessToken}',headers=prepare_headers).json()
        name = me['name']
        iid = me['id']
    except KeyError:
        print(' Cannot parse login details, try another cookie & token !')
        os.system('rm -rf token.txt cookie.txt')
        time.sleep(2)
        login()
    os.system('clear')
    print(logo)
    print(' Logged in user: '+name)
    print(' Logged in id: '+iid)
    print(50*'-')
    print(' [1] Friendlist extract (auto)')
    print(' [2] Friendlist extract (simple-multi)')
    print(' [3] Post reactions extract (public group)')
    print(' [4] Login another id')
    print(' [5] Exit')
    opt = input(' Select option: ')
    if opt == '1':
        auto(prepare_headers,accessToken)
    elif opt == '2':
        multi(prepare_headers,accessToken)
    elif opt == '3':
        post(prepare_headers,accessToken)
    elif opt == '4':
        os.system('rm -rf cookie.txt token.txt')
        exit()
    else:
        exit()
def auto(prepare_headers,accessToken):
    total = []
    os.system('clear & rm -rf .txt .temp.txt')
    print(logo)
    try:
        ids_limit = int(input(' How many ids do you want to add: '))
        for hop in range(ids_limit):
            idt = input(f' Put id no {hop+1}: ')
            try:
                list_one = requests.get(f'https://b-graph.facebook.com/v9.0/{idt}/friends?limit=5000&summary=true&access_token={accessToken}',headers=prepare_headers).json()
                for ids in list_one['data']:
                    uid = ids['id']
                    open('.txt','a').write(uid+'\n')
            except KeyError:
                print(' No friends found !')
            except requests.exceptions.ConnectionError:
                print(' No internet connection ! ')
        print(50*'-')
        exlimit = int(input(' How many ids do want to extract: '))
        for el in range(exlimit):
            sid = input(f' Put id no {el+1}: ')
            os.system('cat .txt | grep "'+sid+'" > .temp.txt')
        print(50*'-')
        print(' Path example: /sdcard/hop.txt')
        sf = input(' Put path to save file: ')
        file = open('.temp.txt','r').read().splitlines()
        print(50*'-')
        print(' Total ids: '+str(len(file)))
        print(' Grabbing process has started')
        print(50*'-')
    except ValueError:
        print('\n Limit should be in digits i.e 2,4,6,4 etc')
        exit()
    for mid in file:
        friendlist = requests.get(f'https://b-graph.facebook.com/v9.0/{mid}/friends?limit=5000&summary=true&access_token={accessToken}',headers=prepare_headers)
        print(friendlist.request.url)
        try:
            for feelings in friendlist['data']:
                hello = feelings['id']
                broken = feelings['name']
                total.append(hello+'|'+broken)
               # open(sf,'a').write(hello+'|'+broken+'\n')
                sys.stdout.write(f'\r Collected ids: {len(total)}');sys.stdout.flush()
            open(sf,'a').write(hello+'|'+broken+'\n')
        except Exception as e:
            print(e)
        except KeyError:
            continue
        except requests.exceptions.ConnectionError:
            print(' No internet connection ')
            break
    print(50*'-')
    print(' The process has been completed')
    print(50*'-')
    exit()
def multi(prepare_headers,accessToken):
    os.system('clear')
    print(logo)
    try:
        ids_limit = int(input(' How many ids do you want to add: '))
        print(' Path example: /sdcard/hop.txt')
        sf = input(' Put path to save file: ')
        for hop in range(ids_limit):
            idt = input(f' Put id no {hop+1}: ')
            try:
                list_one = requests.get(f'https://b-graph.facebook.com/v9.0/{idt}/friends?limit=5000&summary=true&access_token={accessToken}',headers=prepare_headers).json()
                for ids in list_one['data']:
                    uid = ids['id']
                    name = ids['name']
                    open(sf,'a').write(uid+'|'+name+'\n')
            except KeyError:
                print(' No friends found !')
            except requests.exceptions.ConnectionError:
                print(' No internet connection ! ')
    except ValueError:
        print(' Limit should be in digits i.e 2,4,6,8 etc')
        exit()
    print(50*'-')
    print(' Ids extracted successfully')
    print(50*'-')
def post(prepare_headers,accessToken):
    os.system('clear')
    print(logo)
    try:
        ids_limit = int(input(' How many posts do you want to add: '))
        print(' Path example: /sdcard/hop.txt')
        sf = input(' Put path to save file: ')
        for hop in range(ids_limit):
            idt = input(f' Put post id no {hop+1}: ')
            try:
                key='reactions'
                list_one = requests.get(f'https://b-graph.facebook.com/v9.0/{idt}/{key}?limit=5000&summary=true&access_token={accessToken}',headers=prepare_headers).json()
                for ids in list_one['data']:
                    uid = ids['id']
                    name = ids['name']
                    open(sf,'a').write(uid+'|'+name+'\n')
            except KeyError:
                print(' No reactions found !')
            except requests.exceptions.ConnectionError:
                print(' No internet connection ! ')
    except ValueError:
        print(' Limit should be in digits i.e 2,4,6,8 etc')
        exit()
    print(50*'-')
    print(' Ids extracted successfully')
    print(50*'-')
def login():
    os.system('clear')
    print(logo)
    print(' Watch this video for cookie and token: https://www.facebook.com/groups/615593866896958/permalink/669196731536671/?app=fbl')
    print(50*'-')
    access_token = input(' Put access token: ')
    if 'EAAB' in access_token:
        pass
    else:
        print(' Cannot parse access token, invalid token format !')
        exit()
    cookie = input(' Paste cookie here: ')
    prepare_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Host':'b-graph.facebook.com','Cookie':cookie}
    try:
        me = requests.get(f'https://b-graph.facebook.com/me?access_token={access_token}',headers=prepare_headers).json()
        print(me)
        name = me['name']
        open('token.txt','w').write(access_token)
        open('cookie.txt','w').write(cookie)
        print('\n Logged in successfully !')
        time.sleep(1)
        main()
    except KeyError:
        print('\n Your account has checkpoint !')
        exit()
    except AttributeError:
        print('\n Invalid cookies !')
        exit()
if __name__ == '__main__':
    update()
