import requests
import json
from time import sleep
from urllib.parse import urlencode
import sys
import os

url1 = "http://1.12.236.116:8282/api/convert-file"
urlstatus = "http://1.12.236.116:8282/api/conversion-status"
url2 = 'http://1.12.236.116:8282/download-file/'
headers = {'content-type':'application/x-www-form-urlencoded'}

def xbstojson():
	# 上传xbs文件	
	s = open('sourceModelList.xbs','rb')
	fileObject = {
		'file': ('sourceModelList.xbs',s,'application/octet-stream')
	}
	req = requests.post(url=url1,files=fileObject)
	req1 = req.json()
	getflag = req1['flag']
	print(getflag)

	# 检测是否上传完成
	param2 ={'flag':getflag}
	while True:
		st1 = requests.post(urlstatus,data=urlencode(param2),headers=headers, verify=False)
		st2 = st1.json()['status']
		print(st2)
		if st2 == 'done':
			break
		sleep(1)
	s.close()
	print("上传完成")
	# 下载文件
	newurl = url2+getflag
	print(newurl)
	wen = requests.get(newurl,stream=True)
	f = open("before.json", "wb")
	for chunk in wen.iter_content(chunk_size=512):
	    if chunk:
	        f.write(chunk)
	print('下载json,over')
	f.close()

def jsontoxbs():
	# 上传xbs文件
	a = open('after.json','rb')
	fileObject = {
	    'file': ('after.json',a,'application/json')
	}
	req = requests.post(url=url1,files=fileObject)
	req1 = req.json()
	getflag = req1['flag']
	print(getflag)
	# 检测是否上传完成
	param2 ={'flag':getflag}
	while True:
		st1 = requests.post(urlstatus,data=urlencode(param2),headers=headers, verify=False)
		st2 = st1.json()['status']
		print(st2)
		if st2 == 'done':
			break
		sleep(1)
	a.close()
	print("上传完成")
	# 下载文件
	newurl = url2+getflag
	print(newurl)
	wen = requests.get(newurl,stream=True)
	f = open("final.xbs", "wb")
	for chunk in wen.iter_content(chunk_size=512):
	    if chunk:
	        f.write(chunk)
	print('下载xbs,over')
	f.close()


def quchong():
	# 打开JSON文件
	with open('before.json', 'r', encoding='utf-8') as file:
	    # 从文件中加载JSON数据
	    json_root = json.load(file)

	result = {}
	    
	for key, value in json_root.items():
	    # 获取当前对象的"type"值
	    current_sourceUrl = value.get("sourceUrl")
	    #print(current_sourceUrl)
	    flag = 1
	    # 在后续遍历中查找具有相同"type"值的对象
	    for result_key, result_value in result.items(): 
	        if result_value.get("sourceUrl") == current_sourceUrl :
	            #更早，需要替换
	            if result_value.get("lastModifyTime") < value.get("lastModifyTime") :
	                result[key] = value
	                del result[result_key]
	                if "password" in result[key] :
	                    del result[key]['password']
	                    
	            print("删除: "+ current_sourceUrl)
	            flag = 0
	            break #结束循环
	            
	    if flag == 1:
	        result[key] = value
	        if "password" in result[key] :
	            del result[key]['password']
	            
	with open('after.json', 'w', encoding='utf-8') as output_file:
	    json.dump(result, output_file, ensure_ascii=False, separators=(',', ':'))
	    
	print("删除完毕")

def main():
   print("开始任务")
   xbstojson()
   print("开始去重")
   quchong()
   print("开始转xbs")
   jsontoxbs()
   print("任务完成")
   os.remove('before.json')
   os.remove('after.json')

 
if __name__ == '__main__':
    main()



