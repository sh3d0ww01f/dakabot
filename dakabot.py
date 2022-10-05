import requests
import json
import datetime
dev_token="4dd716b4f73d24aae8569481dc7f156a9ed1c8f54a2adb01d5df9e4731857e76"
token="df40f4031bfbd19e065e28fa6a4b169e802e6ad01ff0eeff5fe723227f9f8dd8"

def GetWDKUSER():
    print("[+] 正在获取未打卡成员数据")
    flag=False
    wdkuser=[]
    headers={
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; zh-CN; 22041211AC Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.22.1.233 Mobile Safari/537.36 AliApp(DingTalk/6.5.40) com.alibaba.android.rimet/25926245 Channel/700159 language/zh-CN abi/64 UT4Aplus/0.2.25 colorScheme/light",
    "Cookie": "insert_cookie=60617797; userid=423452111632539485; level=1"
    }
    now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

    data={
    "rq":str(now.year)+"-"+"0"*(len(str(now.month))%2)+str(now.month)+"-"+"0"*(len(str(now.day)))+str(now.day),
    "userid":"423452111632539485"
    }
    url="http://fk.nbcc.cn/fxsq/mrdk/getWdkUserWfxALL.htm"
    resp=requests.post(url=url,data=data,headers=headers)
    if(resp.status_code==200):
        flag=True
        print("[+] 获取成功")
    else:
        print("[-] 获取失败")
        exit(0)
    raw_data=resp.text
    data=json.loads(raw_data)
    for user in data["xtsz_User"]:
        
        wdkuser.append(user["phone"].replace("18975983500","19189622296").replace("18435897369","19564836983"))
    
    return  wdkuser
def dingtalk_send(token,users):
    users_incontent=""
    for user in users:
        users_incontent=users_incontent+"@"+user
    #print(users_incontent)
    headers = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    api_url = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
    json_text = {
        "msgtype": "markdown",  # 信息格式
        "markdown":{
           "title":"今日未打卡人员",
           "text":'''
![](https://tse4-mm.cn.bing.net/th/id/OIP-C.fuIiwudEfIMw7ABm80mr3AAAAA?pid=ImgDet&rs=1)
# -------打卡小助手------
## 今天这小子还没打卡:
### <font color=red>{}</font> 
 \n\n
**每天11点前记得打卡**\n
[点我去打卡](http://fk.nbcc.cn/fxsq/addnew/daka_list.html)

'''.format(users_incontent),
        },
        "at":{
        "atMobiles":users,
            "isAtAll": False
        }
        
    }
    resp = requests.post(api_url, json.dumps(json_text), headers=headers)
    if(resp.status_code==200):
        print("[+] 钉钉机器人发送提醒打卡信息成功 提醒成员如下")
        for user in users:
            print("[+] {}".format(user))
    else:
        print("[-] 钉钉机器人发送提醒打卡信息失败")
    print("[+] Done!")
    #return resp.text
if __name__=='__main__':
        user=[]
        user=GetWDKUSER()
        #print(user)
        dingtalk_send(token,user)
