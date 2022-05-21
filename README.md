# FFXIV_logs_modifier

## use at your own risk. The purpose of this repo is for studying.



## introduction (下有中文)
this script modify the logs txt file from Advanced combat tracker (ACT) for FFXIV. Support both international server and chinese server. 
You could potentially increase your general ability damage or the date of combat or basically everything in the report.   
But when you modified a lot,  your report may get blacklisted by the logs website.  

## Tutorial
- get the codes downloaded. Install python interpreter
- change the parameters at the end of the script. For example, you need to input your character name and path to the logs file 
- run the script, a file with modified postfix will be generated. 

## 介绍
这个代码用于修改ACT产生的logs记录txt文件。 你基本上可以自动修改伤害和战斗时间等一系列数据，或者进行逐行精确修改。但是如果你修改了很多，你的报告可能会失效。  
该脚本与FF14游戏不产生任何程度互动，更不属于游戏第三方插件。

## 教程
- 下载代码，从python官网安装python解释器
- 在main.py的结尾，修改一些参数，比如你需要指定你的角色名，和你要修改的logs文件的路径
- 运行脚本，logs文件目录下会生成带有modified后缀的文件
