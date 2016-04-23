import urllib.request
import re

cp = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cp)
urllib.request.install_opener(opener)
LoginURL = 'http://59.73.151.11/physlab/s2.php'
#把LoginData中的信息改成自己的学号和密码...
LoginData = b'stu_id=143401010421&stupwd=1234'
InfoURL = 'http://59.73.151.11/physlab/s6.php'
ClassURL = 'http://59.73.151.11/physlab/stuyy_test.php'

def Connect(url, data=b'', timeOut=5, tryTime=5):
	req = urllib.request.Request(url, data)
	while tryTime > 0 :
		print('Connecting...')
		try:
			res = urllib.request.urlopen(req, timeout=timeOut)
			return res
		except:
			tryTime -= 1
	print('Can not connect to server...')
	exit()

#获取用户信息
res = Connect(LoginURL, LoginData)
info = Connect(InfoURL).read().decode('gb2312');
if re.search(r'密码错误', info):
	print('密码错误！')
	exit()
info = [re.search(r'学号[^>]*>[^>]*>([^<]*)', info).group(1), re.search(r'姓名[^>]*>[^>]*>([^<]*)', info).group(1), re.search(r'班级[^>]*>[^>]*>([^<]*)', info).group(1)]
print('学号：' + info[0] + '\n姓名：' + info[1] + '\n班级：' + info[2])

#获取实验列表，并按实验时间排序
input('回车查看可选课程')
info = Connect(ClassURL).read().decode('gb2312').replace('&nbsp;', ' ').replace(' ', '')
info = re.findall(r'value=(\d)name=\'sy_sy\'[^>]*>实验名称：([^<]*)<br>教师：([^时]*)[^>]*>第([^<]*)周[^>]*>[^>]*>星期([^<]*)<[^>]*>[^>]*>第([^<]*)节[^>]*>地点：([^<]*)<', info)
info.sort(key=lambda x: x[3:6])
for item in info:
	print('%3s  %2s-%s-%s  %3s  %s  %s' % (item[0], item[3], item[4], item[5], item[2], item[6], item[1]))

#提交选课信息
while True:
	num = int(input('输入课程编号；'))
	while True:
		info = Connect(ClassURL, ('sy_sy=%d' % num).encode(), timeOut=10).read().decode('gb2312')
		if re.search(r'访问人数', info):
			continue
		elif re.search(r'物理实验每周只能预约', info):
			print('你本周已经选过实验了')
		elif re.search(r'你已经做过该实验的同组实验', info):
			print('你已经做该试验的同组实验')
		elif re.search(r'你已经做过该实验', info):
			print('你已经做过该试验')
		elif re.search(r'你已经预约过该实验', info):
			print('你已经预约过该实验')
		elif re.search(r'该实验已经没有空位', info):
			print('该实验已经没有空位')
		elif re.search(r'添加到数据库中', info):
			print('选课成功！')
			exit()
		else:
			print(info)
			if(input('输入Q继续提交，输入其他重新选择课程')=='q'):
				continue
		break

