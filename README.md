# WoWTool
魔兽世界怀旧版插件更新器

安装步骤：

1.下载并安装python，地址：https://www.python.org/getit/ 安装最新的版本即可（我只测试了3.7.4）

2.下载本项目，点击下载 "Clone or download"->"Download Zip" ，经典怀旧版修改项目中的“经典版请配置这里.txt”文件

3.下面对“经典版请配置这里.txt”进行详细的说明，下面是默认的“经典版请配置这里.txt”内容

    G:\World of Warcraft\_classic_\Interface\AddOns
    https://www.curseforge.com/wow/addons/Bagnon
    https://www.curseforge.com/wow/addons/omni-cc


- 其中第一行是魔兽世界的安装路径，尽量使用英文。经典怀旧版本一般是"_classic_"
- 从第二行开是单体插件在curseforge上的网址，你可以通过 https://www.curseforge.com/wow/addons 来查询自己想要的插件。 
- 目前配置文件只能识别 https://www.curseforge.com/wow/addons/xxxxxx 这种格式的网址。通过 https://www.curseforge.com/wow/addons 搜索到的插件地址都满足这个要求。
- 你需要多少插件，就加多少行插件的网址在这个txt文件里，不需要的插件删掉该行即可。
    
4.双击 运行.bat 开始运行脚本。  
5.等待脚本下载并安装插件。  
6.日后可以随时双击 运行.bat，脚本会自动更新有必要更新的插件。  
7.如果运行脚本的过程中发生网络报错，可能是暂时被封，换个时间重新运行脚本继续下载即可。  
8.强制下载/更新全部插件：清空savedInfo.dat文件，再运行脚本。  
9.下载的插件zip包放在了 temp_download 文件夹内。
10.如果暂时不想更新某个插件，可以在插件地址的前面加上 # 符号
