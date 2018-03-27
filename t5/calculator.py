#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,csv,getopt,configparser
from datetime import datetime
# 处理命令行参数类
class Args(object):
    def __init__(self):
        self.args={}
        try:
             opts,argsctn= getopt.getopt(sys.argv[1:],'C:c:d:o:h',['help'])
        except getopt.GetoptError:
            print("args is Error")
            exit()
        for flag,ctn in opts:
            if flag in ['h','--help']:
               self.args[flag]="Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata"
               print(self.args[flag])
            else:
               self.args[flag]=ctn
           
    """
    补充代码：
    1. 补充参数读取函数，并返回相应的路径.
    2. 当参数格式出错时，抛出异常.
    """
    def pathByChar(self,flag):
        return self.args[flag]

# 配置文件类
class Config(object):
    def __init__(self,path,secFlag):
        self.maxValue,self.minValue,self.rais = self._read_config(path,secFlag)
    # 配置文件读取内部函数
    def _read_config(self,path,secFlag):
        maxval=0.00
        minval=0.00
        rais=0.00
        try:
            config = configparser.ConfigParser()
            config.read(path)
            for t1,t2 in config.items(secFlag.upper()):
                t2=float(t2)
                if t1 == 'JiShuL':
                    minval=t2
                elif t1=='JiShuH':
                    maxval=t2
                else: 
                    rais+=t2
        except:
            print("config is error!!")
            exit()
        return maxval,minval,rais
        """
        补充代码：
        1. 根据参数指定的配置文件路径，读取配置文件信息，并写入到 config 字典中.
        2. 使用 strip() 和 split() 对读取到的配置文件去掉空格以及切分.
        3. 当格式出错时，抛出异常.
        """


# 用户数据类
class UserData(object):

    def __init__(self,path):
        self.userdata = self._read_users_data(path)

    # 用户数据读取内部函数
    def _read_users_data(self,path):
        userdata = []
        with open(path,'r') as f:
            for a in f.readlines():
                temp=tuple(a.strip().split(','))
                money = 0
                try:
                   money=int(temp[1])
                except:
                   print("Paramiter is Error")
                   exit()
                userdata.append((temp[0], money))
        return userdata
        """
        补充代码：
        1. 根据参数指定的工资文件路径，读取员工 ID 和工资数据.
        2. 可将员工工号和工资数据设置为元组，并存入 userdata 列表中.
        3. 当格式出错时，抛出异常.
        """

# 税后工资计算类
class IncomeTaxCalculator(object):
    def __init__(self,cfgobj,usdata):
        self.cfg = cfgobj
        self.usdata = usdata
	
    # 计算每位员工的税后工资函数
    def calc_for_all_userdata(self):
        data = []
        t=datetime.now()
        for gh,gz in  self.usdata.userdata:
            sheb = self.getSelfShebaoE(gz)
            kous = self.getSelfGeShui(gz)
            zuih = gz-sheb-kous
            str = '{},{},{},{},{},{}'.format(gh,gz,format(sheb,'.2f'),format(kous,'.2f'),format(zuih,'.2f'),datetime.strftime(t,'%Y-%m-%d %H:%M:%S'))
            data.append(str)
        return data
        """
         补充代码：
         1. 计算每位员工的税后工资（扣减个税和社保）.
         2. 注意社保基数的判断.
         3. 将每位员工的税后工资按指定格式返回.
        """
    def getSelfShebaoE(self,money):
        maxval = float(self.cfg.maxValue)
        minval = float(self.cfg.minValue)
        rais  = float(self.cfg.rais)
        if money>0 and money<minval:
            return minval*rais
        elif money>=minval and money <=maxval:
            return money*rais
        elif money>maxval:
            return maxval*rais
        else:
            return 0
    def getSelfGeShui(self,money):
        shebao = self.getSelfShebaoE(money)
        sqe = float(money) - shebao -3500
        if sqe <=0: 
            return 0
        elif sqe>0 and sqe<=1500:
            return sqe*0.03-0
        elif sqe>1500 and sqe<=4500:
            return sqe*0.1-105
        elif sqe>4500 and sqe<=9000:
            return sqe*0.2-555
        elif sqe>9000 and sqe<=35000:
            return sqe*0.25-1005
        elif sqe>35000 and sqe <=55000:
            return sqe*0.3-2755
        elif sqe>55000 and sqe<=80000:
            return sqe*0.35-5505
        elif sqe>80000:
            return sqe*0.45-13505
    # 输出 CSV 文件函数
    def export(self,arg,default='csv'):
        result = self.calc_for_all_userdata()
        with open(arg,'w') as f:
            for lin in result:
                 f.write(lin+'\n')
            #writer = csv.writer(f)
            #writer.writerows(result)
# 执行
if __name__ == '__main__':
    argIni = Args()
    cfg = Config(argIni.pathByChar('-c'),argIni.pathByChar('-C'))
    usrdata = UserData(argIni.pathByChar('-d'))
    jisuan = IncomeTaxCalculator(cfg,usrdata)
    jisuan.calc_for_all_userdata()
    jisuan.export(argIni.pathByChar('-o'))
