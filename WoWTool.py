#-*- coding:utf-8 -*-
import os
import cfscrape
import requests
import zipfile
import json

from pyquery import PyQuery as pq
from datetime import datetime



wow_path = ''
targetInterface_list = list()
#scraper = cfscrape.create_scraper() 

def log(res):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +': ' + res)

class WoWConfig:
    wow_path=''
    target_list=list()
    saved_list=list()
    download_list=list()

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

    def getaddon(self, doc):
        id = doc('.overflow-tip.truncate').eq(0).attr('data-id')
        #log(id)

        name = doc('.font-bold.text-lg.break-all').text()
        #log(name)

        ex_url = 'https://www.curseforge.com'
        originurl = ''
        wowversioncount = len(doc('.e-sidebar-subheader.overflow-tip.mb-1'))
        if wowversioncount == 2:
            originurl = doc('.button.button--icon-only.button--sidebar').eq(1).attr('href')
        else:
            wowversionstring = doc('.e-sidebar-subheader.overflow-tip.mb-1').children('a').eq(0).text().strip()
            if wowversionstring == 'WoW Classic':
                originurl = doc('.button.button--icon-only.button--sidebar').eq(0).attr('href')
        
        version = originurl[originurl.rindex('/') + 1:]
        #log(version)

        downloadurl = ex_url + originurl + "/file";	
        #log(url)
        addon = dict()
        addon['id'] = id
        addon['name'] = name
        addon['version'] = version
        addon['downloadurl'] = downloadurl 
        return addon

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

            # with open('addon.dat','r',encoding='utf-8') as demofile:
            #     # while True:
            #         # lines = demofile.read() # 整行读取数据
            #         # if not lines:
            #         #     break
            #         #     pass
            #         #p_tmp, E_tmp = [float(i) for i in lines.split()] # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            #         #pos.append(p_tmp)  # 添加新读取的数据
            #         #Efield.append(E_tmp)
            #         #log(lines)
            #         jj = json.load(demofile)
            #         pass
            #     #pos = np.array(pos) # 将数据从list类型转换为array类型。
            #     #Efield = np.array(Efield)
            # pass
        #print(jj[0]['name'])


        #scrapertemp = cfscrape.create_scraper() 
        for t in self.target_list:
            filename = t[t.rindex('/')+1:]
            log('check interface: ' + filename)

            for a in addon_all:
                #log('read :' + a['name'])

                if str(a['websiteUrl']).lower() == t.lower():
                    addonobject = self.getaddonV2(a)
                    if self.checkNeedUpdate(addonobject):
                        self.download_list.append(addonobject)
                        pass                    
                    break
                pass
            pass

        pass

        #print(self.download_list)

    def preparedownloadinterface(self):
        self.download_list = list()
        scrapertemp = cfscrape.create_scraper() 
        for t in self.target_list:
            filename = t[t.rindex('/')+1:]
            log('check interface: ' + filename)

            #先写文件，从文件读取，便于测试
            # web_data = scraper.get(t).content
            # with open(filename+'.html','wb') as demofile:
            #     demofile.write(web_data)
            #doc = pq(filename=filename+'.html')

            #实际从网页读取
            web_data = scrapertemp.get(t).content
            sourcecode = str(web_data, encoding='utf-8')
            doc = pq(sourcecode)

            addonobject = self.getaddon(doc)
            if self.checkNeedUpdate(addonobject):
                self.download_list.append(addonobject)
            else:
                pass
        #print(self.download_list)
    
    def downloadinterface(self):
        log('===========start downloading============')
        scrapertemp = cfscrape.create_scraper() 
        for a in self.download_list:
            log('downloading :' + a['name'])
            #downloadfile
            #todo download
            aname = str(a['downloadurl'])[str(a['downloadurl']).rindex('/')+1:]
            filename = 'temp_download/' + aname
            r = scrapertemp.get(a['downloadurl'])
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
            if isnewaddon:
                newaddon = dict()
                newaddon['id'] = a['id']
                newaddon['name'] = a['name']
                newaddon['version'] = a['version']
                self.saved_list.append(newaddon)
        
        log('===========downloading complete============')
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
    
    for names in zip_file.namelist():
        zip_file.extract(names, pathname)  #加入到某个文件夹中 zip_file.extract(names,file_name.split(".")[0])
    zip_file.close()


def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize
     
    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')

# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)



if __name__ == '__main__':
    log('===========start============')

    command = 0
    if os.path.exists('addon.dat'):
        commandstr = input("是否更新现有插件信息（更新较慢，不要经常更新，可能会被封）：【1】更新；【0】不更新")
        command = int(commandstr)
    else:
        command = 1
        pass

    
    if command == 1:
        log('===========update new addon info============')
        t='https://addons-ecs.forgesvc.net/api/v2/addon/search?categoryId=0&gameId=1&gameVersionFlavor=wow_classic'        
        scraper = cfscrape.create_scraper() 
        web_data = scraper.get(t).content
        with open('addon.dat','wb') as demofile:
            demofile.write(web_data)
        log('!!!!!!!!!!!!!!!update new addon info end!!!!!!!!!!!!!!!')
    else:
        pass
    
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

    log('===========complete============')
    
