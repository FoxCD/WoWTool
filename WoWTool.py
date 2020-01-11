#-*- coding:utf-8 -*-
import os
import requests
import zipfile
import json

from datetime import datetime

wow_path = ''
targetInterface_list = list()

def log(res):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +': ' + res)

class WoWConfig:
    wow_path=''
    target_list=list()
    saved_list=list()
    download_list=list()
    err_list=list()

    def __init__(self):
        self.wow_path=''
        self.target_list=list()
        self.saved_list=list()

    def loadconfig(self):
        try:
            log('load config...')
            configpath = '经典版请配置这里.txt'
            with open(configpath, 'r') as f:
                lines = f.readlines()
            for l in lines:
                if l.startswith('#'):
                    pass
                elif l.startswith('http'):
                    self.target_list.append(l.strip())
                else:
                    self.wow_path = l.strip()

            #log(self.wow_path)
        except expression as identifier:
            log('config load failed!!')
            pass


    def loadsaveddata(self):
        try:
            log('load saved data....')
            configpath = 'savedInfo.dat'
            with open(configpath, 'r') as f:
                configdata = f.read()
            self.saved_list = json.loads(configdata)
            #print(self.saved_list)
        except:
            log('config saved load failed!!')
            pass


    def getaddonV2(self, doc):
        id = doc['id']
        #log(id)

        name = doc['name']
        #log(name)

        version= 0
        downloadurl=''
        # for lastedversion in doc['gameVersionLatestFiles']:
        #     log(str(lastedversion['projectFileId']))
        #     log(str(lastedversion['gameVersionFlavor']))

        #     if lastedversion['gameVersionFlavor'] == 'wow_classic' and int(lastedversion['projectFileId']) > projectFileId:
        #         projectFileId = lastedversion['projectFileId']
        #         pass
        #     pass

        for lastedfile in doc['latestFiles']:
            if not str(lastedfile['fileName']).find('nolib') >= 0 and lastedfile['gameVersionFlavor'] == 'wow_classic' and int(lastedfile['id']) > version:
                version = int(lastedfile['id'])
                downloadurl = lastedfile['downloadUrl']
                #break
            pass
            
        addon = dict()
        addon['id'] = id
        addon['name'] = name
        addon['version'] = version
        addon['downloadurl'] = downloadurl 
        
        #log(json.dumps(addon))
        return addon
    
    def checkNeedUpdate(self, addonobject):
        res = True
        #log(json.dumps(addonobject))
        for a in self.saved_list:
            #log(str(a))
            if int(a['id']) == int(addonobject['id']) and int(a['version']) == int(addonobject['version']):
                #log(json.dumps(a))
                res = False
                break
            else:
                res = True
        # log(addonobject['name'] + ' need update')
        if res:
            log(addonobject['name'] + ' need update')
        else:
            log(addonobject['name'] + ' not need to update')
        return res

    def preparedownloadinterfaceV2(self):
        self.download_list = list()

        #加载所有插件
        demofile = open('addon.dat','r',encoding='utf-8')
        addon_all = json.load(demofile)
        demofile.close()
        log('load addon completed!')
 
        for t in self.target_list:
            filename = t[t.rindex('/')+1:]
            log('check interface: ' + filename)

            founded = 0
            for a in addon_all:
                #log('read :' + a['name'])

                if str(a['websiteUrl']).lower() == t.lower():
                    founded = 1
                    addonobject = self.getaddonV2(a)
                    if self.checkNeedUpdate(addonobject):
                        self.download_list.append(addonobject)
                        pass                    
                    break
                pass
            pass

            if founded == 0:
                self.err_list.append(t)
                pass
            pass
        #print(self.download_list)
    
    def downloadinterface(self):
        log('===============start downloading===============')
        for a in self.download_list:
            log('downloading :' + a['name'])
            #downloadfile
            #todo download
            aname = str(a['downloadurl'])[str(a['downloadurl']).rindex('/')+1:]
            filename = 'temp_download/' + aname
            r = requests.get(a['downloadurl'])
            with open(filename, "wb") as code:
               code.write(r.content)

            un_zip(filename, wc.wow_path)
            log(a['name'] + ' unziped completed!!')

            isnewaddon = True
            for s in self.saved_list:
                if s['id'] == a['id']:
                    s['version'] = a['version']
                    isnewaddon  = False
                    break
                else:
                    pass
                pass

            if isnewaddon:
                newaddon = dict()
                newaddon['id'] = a['id']
                newaddon['name'] = a['name']
                newaddon['version'] = a['version']
                self.saved_list.append(newaddon)
                pass
            pass
                
        log('===============downloading complete===============')
        # print(self.saved_list)

        #转为json方便存储
        jsonsavedata = json.dumps(self.saved_list)
        # print(jsonsavedata)

        #存储最新的插件数据
        with open('savedInfo.dat', 'wb') as f:
            f.write(jsonsavedata.encode())



def un_zip(file_name, pathname):  
    """unzip zip file"""  
    zip_file = zipfile.ZipFile(file_name)
    
    #log('check '+ pathname)
    if os.path.exists(pathname):
        #log(pathname + '-- exsited!')
        pass  
    else:
        #log('create -- ' + pathname)
        os.mkdir(pathname)
        pass
    
    for names in zip_file.namelist():
        zip_file.extract(names, pathname)  #加入到某个文件夹中 zip_file.extract(names,file_name.split(".")[0])
        pass
    zip_file.close()


if __name__ == '__main__':
    log('===============start V1.1.1===============')

    command = 0
    if os.path.exists('addon.dat'):
        commandstr = input("是否更新插件数据库（更新较慢，失败请重试）：【1】更新；【0】不更新")
        command = int(commandstr)
        pass
    else:
        command = 1
        pass

    dbupdated = 1
    if command == 1:
        log('===============update addon db===============')
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
            url ='https://addons-ecs.forgesvc.net/api/v2/addon/search?categoryId=0&gameId=1&gameVersionFlavor=wow_classic'        
            r = requests.get(url,headers = headers, timeout = 30)
            #log(str(r.status_code))
            with open('addon.dat','wb') as demofile:
                demofile.write(r.content)
            log('===============update addon db succeed===============')
            pass
        except:
            dbupdated = 0
            log('!!!!!!!!!!!!!!!update addon db failed!!!!!!!!!!!!!!!')
            pass
    else:
        pass
    
    if dbupdated == 1:
        path = 'temp_download'
        isExists=os.path.exists(path)

        if not isExists:
            os.mkdir(path)
            log('temp download path created')
        else:
            log('temp download path exist')
        
        wc = WoWConfig()
        wc.loadconfig()
        wc.loadsaveddata()
        wc.preparedownloadinterfaceV2()
        wc.downloadinterface()

        #output err info
        for t in wc.err_list:
            log(t + ' is NOT FOUNDED!!!!!!!!!')
            pass
        
        log('===============complete===============')
        pass
    else:
        pass