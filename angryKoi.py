# 愤怒的锦鲤
# 入口>京东首页>领券>锦鲤红包
# 环境变量JD_COOKIE，多账号用&分割
# 环境变量kois中填入需要助力的pt_pin，有多个请用 '@'或'&'或空格 符号连接,不填默认全部账号内部随机助力
# 环境变量wy_AsyncConcurrent规定是否启用高并发，yes或no,不填默认no不启用高并发
# 脚本内或环境变量填写，优先环境变量
# export JD_COOKIE="第1个cookie&第2个cookie"
# export kois=" 第1个cookie的pin & 第2个cookie的pin "
# export wy_AsyncConcurrent="yes"      
# 11 10 22:00 应要求更改cdn


import os,json,random,time,re,string,functools,asyncio
import sys
sys.path.append('../../tmp')
sys.path.append(os.path.abspath('.'))
try:
    import aiohttp
except Exception as e:
    print(e, "\n请更新pip版本：pip3 install --upgrade pip \n缺少aiohttp 模块，请执行命令安装: pip3 install aiohttp\n")
    exit(3) 
try:
    import requests
except Exception as e:
    print(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")
requests.packages.urllib3.disable_warnings()


run_send='yes'              # yes或no, yes则启用通知推送服务
run_getUserInfo='no'        # yes或no, yes则启用检查账号有效性
wy_AsyncConcurrent='no'    # 是否启用高并发，环境变量优先


# 检查python版本
def python_version():
    if sys.version_info < (3, 8):
        print('你的python版本小于3.8')
        exit()
python_version()


# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')


# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/ql/config/config.sh')
            except:
                a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/jd/config/config.sh')
            except:
                a=eval(env)
        else:
            a=eval(env)
    except:
        a=''
    return a

# v4
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c


# 随机ua
def ua():
    sys.path.append(os.path.abspath('.'))
    try:
        from jdEnv import USER_AGENTS as a
    except:
        a='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return a

# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000))

## 获取cooie
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)):
            cookie_list=self.v4_cookie()
        else:
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量JD_COOKIE\n')    
        return cookie_list

    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except:
                    pass
        return a
cookie_list=Judge_env().main_run()


## 获取通知服务
class Msg(object):
    def getsendNotify(self, a=1):
        try:
            url = 'https://mirror.ghproxy.com/https://raw.githubusercontent.com/xpqdudu/oemScripts/main/sendNotify.py'
            response = requests.get(url,timeout=3)
            with open('sendNotify.py', "w+", encoding="utf-8") as f:
                f.write(response.text)
            return
        except:
            pass
        

    def main(self,f=1):
        global send,msg,initialize
        sys.path.append(os.path.abspath('.'))
        for n in range(3):
            try:
                from sendNotify import send,msg,initialize
                break
            except:
                pass
        l=['BARK','SCKEY','TG_BOT_TOKEN','TG_USER_ID','TG_API_HOST','TG_PROXY_HOST','TG_PROXY_PORT','DD_BOT_TOKEN','DD_BOT_SECRET','Q_SKEY','QQ_MODE','QYWX_AM','PUSH_PLUS_TOKEN','PUSH_PLUS_USER']
        d={}
        for a in l:
            try:
                d[a]=eval(a)
            except:
                pass
        try:
            initialize(d)
        except:
            self.getsendNotify()
            if f < 5:
                f += 1
                return self.main(f)
            else:
               pass
#Msg().main()   # 初始化通知服务   

# 异步检查账号有效性
nickname_findall=re.compile(r'"nickname":"(.+?)"')
async def getUserInfo_list(cookie_list):
    async def getUserInfo(cookie):
        nonlocal session,cookie_ok_list
        if not (pin:=get_pin(cookie)):
            return
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback='
        headers = {
            'Cookie': cookie,
            'Accept': '*/*',
            'Connection': 'close',
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'me-api.jd.com',
            'User-Agent': ua(),
            'Accept-Langua()ge': 'zh-cn'
        }
        try:
            async with session.get(url, headers=headers, timeout=60) as res:
                res =await res.text()        
            if '"retcode":"0"' in res:
                if nickname := nickname_findall.findall(res):  # 账号名
                    cookie_ok_list.append(cookie)
            else:
                msg(f"账号 {pin} Cookie 已失效！请重新获取。\n")
        except Exception:
            msg(f"账号 {pin} Cookie 已失效！请重新获取。\n")

    cookie_ok_list=list()
    async with aiohttp.ClientSession() as session:
        tasks=[getUserInfo(cookie) for cookie in cookie_list]
        await asyncio.wait(tasks)
    return [cookie for cookie in cookie_ok_list if cookie]
if run_getUserInfo=='yes':
    cookie_list=asyncio.run(getUserInfo_list(cookie_list))      # 初始化cookie


async def taskPostUrl(functionId, body, cookie):
    url=f'https://api.m.jd.com/api?appid=jinlihongbao&functionId={functionId}&loginType=2&client=jinlihongbao&t={gettimestamp()}&clientVersion=10.1.4&osVersion=-1'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://happy.m.jd.com',
        'referer': 'https://happy.m.jd.com/babelDiy/zjyw/3ugedFa7yA6NhxLN5gw2L3PF9sQC/index.html?channel=9&un_area=4_134_19915_0',
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    data=f"body={json.dumps(body)}"
    for n in range(3):
        try:
            async with session.post(url, headers=headers,data=data) as res:
                res =await res.text()
                return res
        except:
            if n==2:
                msg('API请求失败，请检查网路重试❗\n')  

# 开启助力
code_findall=re.compile(r'"code":(.*?),')
async def h5launch(cookie):
    body={"followShop":1,"random":''.join(random.sample(string.digits, 6)),"log":"4817e3a2~8,~1wsv3ig","sceneid":"JLHBhPageh5"}
    res=await taskPostUrl("h5launch", body, cookie)
    if not res:
        return
    if Code:=code_findall.findall(res):
        str(Code:=Code[0])=='0'
        msg(f"账号 {get_pin(cookie)} 开启助力码成功\n")
    else:
        msg(f"账号 {get_pin(cookie)} 开启助力码失败")
        msg(res)

# 获取助力码
id_findall=re.compile(r'","id":(.+?),"')
async def h5activityIndex(cookie):
    global inviteCode_list
    body={"isjdapp":1}
    res=await taskPostUrl("h5activityIndex", body, cookie)
    if not res:
        return
    if inviteCode:=id_findall.findall(res):
        inviteCode=inviteCode[0]
        inviteCode_list.append(inviteCode)
        msg(f"账号 {get_pin(cookie)} 的锦鲤红包助力码为 {inviteCode}\n")
    else:
        msg(f"账号 {get_pin(cookie)} 获取助力码失败\n")

# 助力
statusDesc_findall=re.compile(r',"statusDesc":"(.+?)"')
async def jinli_h5assist(cookie,redPacketId):
    body={"redPacketId":redPacketId,"followShop":0,"random":''.join(random.sample(string.digits, 6)),"log":"42588613~8,~0iuxyee","sceneid":"JLHBhPageh5"}
    res=await taskPostUrl("jinli_h5assist", body, cookie)
    msg(f'账号 {get_pin(cookie)} 去助力{redPacketId}')
    if not res:
        return
    if statusDesc:=statusDesc_findall.findall(res):
        statusDesc=statusDesc[0]
        msg(f"{statusDesc}\n")
    else:
        msg(f"错误\n{res}\n")

# 开红包
biz_msg_findall=re.compile(r'"biz_msg":"(.*?)"')
discount_findall=re.compile(r'"discount":"(.*?)"')
async def h5receiveRedpacketAll(cookie):
    body={"random":''.join(random.sample(string.digits, 6)),"log":"f88c05a0~8,~1iqo16j","sceneid":"JLHBhPageh5"}
    res=await taskPostUrl("h5receiveRedpacketAll", body, cookie)
    msg(f'账号 {get_pin(cookie)} 开红包')
    if not res:
        return
    try:
        biz_msg=biz_msg_findall.findall(res)[0]
    except:
        print(res)
        return
    if discount:=discount_findall.findall(res):
        discount=discount[0]
        msg(f"恭喜您，获得红包 {discount}\n")
        return await h5receiveRedpacketAll(cookie)
    else:
        msg(f"{biz_msg}\n")


async def asyncmain():

    if debug_pin:=get_env('kois'):
        # print(debug_pin)
        cookie_list_pin=[cookie for cookie in cookie_list if get_pin(cookie) in debug_pin]
    else:
        cookie_list_pin=cookie_list

    global inviteCode_list
    inviteCode_list=list()

    global session
    async with aiohttp.ClientSession() as session:

        msg('***************************开启助力码***************\n')
        if (wy_AsyncConcurrent:=get_env('wy_AsyncConcurrent'))=='no':
            [await h5launch(cookie) for cookie in cookie_list]
        else:
            tasks=[h5launch(cookie) for cookie in cookie_list]
            await asyncio.wait(tasks)

        msg('***************************获取助力码***************\n')
        if wy_AsyncConcurrent=='no':
            [await h5activityIndex(cookie) for cookie in cookie_list_pin]
        else:
            tasks=[h5activityIndex(cookie) for cookie in cookie_list_pin]
            await asyncio.wait(tasks)



        msg('*******************助力**************************\n')
        if inviteCode_list:
            if wy_AsyncConcurrent=='no':
                [await jinli_h5assist(cookie,inviteCode) for inviteCode in inviteCode_list for cookie in cookie_list]
            else:
                tasks=[jinli_h5assist(cookie,inviteCode) for inviteCode in inviteCode_list for cookie in cookie_list]
                await asyncio.wait(tasks)
        else:
            msg('没有需要助力的锦鲤红包助力码\n')

        msg('*******************开红包**************************\n')
        if wy_AsyncConcurrent=='no':
            [await h5receiveRedpacketAll(cookie) for cookie in cookie_list]
        else:
            tasks=[h5receiveRedpacketAll(cookie) for cookie in cookie_list]
            await asyncio.wait(tasks)





