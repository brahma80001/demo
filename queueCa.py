#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv # 用于写入 csv 文件
from multiprocessing import Process,Queue
queue = Queue()
# 处理命令行参数类
class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
    """
    补充代码：
    1. 补充参数读取函数，并返回相应的路径.
    2. 当参数格式出错时，抛出异常.
    """
    def pathByChar(self,flag):
        return self.args[self.args.index(flag)+1]

# 配置文件类
class Config(object):
    def __init__(self,path):
        self.config = self._read_config(path)

    # 配置文件读取内部函数
    def _read_config(self,path):
        config = {}
        try:
            with open(path,'r') as f:
                for a in f.readlines():
                    temp=tuple(a.split('='))
                    config[temp[0].strip()]=temp[1].strip()
        except:
            print("file is not found")
            exit()
        return config
        """
        补充代码：
        1. 根据参数指定的配置文件路径，读取配置文件信息，并写入到 config 字典中.
        2. 使用 strip() 和 split() 对读取到的配置文件去掉空格以及切分.
        3. 当格式出错时，抛出异常.
        """
    def get_config(self,tem):
        return self.config[tem]


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
    def __init__(self,cfgobj):
        self.cfg = cfgobj
	
    # 计算每位员工的税后工资函数
    def calc_for_all_userdata(self,temp):
            gh = temp[0]
            gz = temp[1]
            sheb = self.getSelfShebaoE(gz)
            kous = self.getSelfGeShui(gz)
            zuih = gz-sheb-kous
            str = '{},{},{},{},{}'.format(gh,gz,format(sheb,'.2f'),format(kous,'.2f'),format(zuih,'.2f'))
        return str
        """
         补充代码：
         1. 计算每位员工的税后工资（扣减个税和社保）.
         2. 注意社保基数的判断.
         3. 将每位员工的税后工资按指定格式返回.
        """
    def getSelfShebaoE(self,money):
        max = float(self.cfg.get_config('JiShuH'))
        min = float(self.cfg.get_config('JiShuL'))
        lv  = float(self.cfg.get_config('YangLao'))
        lv += float(self.cfg.get_config('YiLiao'))
        lv += float(self.cfg.get_config('ShiYe'))
        lv += float(self.cfg.get_config('GongShang'))
        lv += float(self.cfg.get_config('ShengYu'))
        lv += float(self.cfg.get_config('GongJiJin'))
        if money>0 and money<min:
            return min*lv
        elif money>=min and money <=max:
            return money*lv
        elif money>max:
            return max*lv
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
    # 输出 CSV 文件函
    
class ExportUtil(object):
    def __init__(self):
        pass
    def export(self,arg,temp,default='csv'):
        with open(arg,'a') as f:
            f.write(lin+'\n')
            #writer = csv.writer(f)
            #writer.writerows(result)
            
def huoUserData(user):
   for tt in userdata.userdata:
       queue.put(tt)
def huoCalData(jisuan):
   temp=[]
   while Queue.empty(queue):
       temp.append(jisuan.calc_for_all_userdata(queue.get()))
   for tt in temp:
       queue.put(tt)
def xieru():
    argIni = Args()
    argIni.pathByChar('-o')
    xieru = ExportUtil()
    while Queue.empty(queue):
        xieru.export(argIni.pathByChar('-o'),queue.get())
# 执行
if __name__ == '__main__':
    argIni = Args()
    cfg = Config(argIni.pathByChar('-c'))
    usrdata = UserData(argIni.pathByChar('-d'))
    jisuan = IncomeTaxCalculator(cfg)
    Process(target=huoUserData,args=(userdata,)).start()
    Process(target=huoCalData,args=(jisuan,)).start()
    Process(target=xieru).start()
   
