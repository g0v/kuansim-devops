# -*- coding: utf-8 -*-
from github import Github
import datetime
import smtplib
from email.Header import Header
from email.mime.text import MIMEText

g = Github()

r = g.get_repo('g0v/kuansim')
dict_issue = r.get_issues(state='open')
dict_label = r.get_labels()

list_issue_backend = []
list_issue_frontend = []
list_issue_feature = []
list_issue_devops = []
list_issue_doc = []
list_issue_other = []
mail_body = ""

for x in dict_issue:
	if not x.assignee:
		for y in x.labels:
			if "backend" in y.name:
				list_issue_backend.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))
				break
			elif "frontend" in y.name:
				list_issue_frontend.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))
				break
			elif "feature" in y.name:
				list_issue_feature.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))
				break
			elif "devops" in y.name:
				list_issue_devops.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))
				break
			elif "doc" in y.name:
				list_issue_doc.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))
				break
			else:
				list_issue_other.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))
				break

mail_body = mail_body + "待認領任務"

# 印出列表任務
def get_str_issue_by_label(list, label):
	str_body = ""
	if len(list) > 0:
		list.sort()
		str_body =  "%s\n%s\n" % (str_body, label)
		for x in list:
			str_body = "%s%s\n" % (str_body, x.encode('utf-8'))
	return str_body


if len(list_issue_backend) > 0:
	list_issue_backend.sort()
	mail_body = mail_body + "\nbackend:\n"
	for x in list_issue_backend:
		mail_body = mail_body + x.encode('utf-8') + "\n"

if len(list_issue_frontend) > 0:
	list_issue_frontend.sort()
	mail_body = mail_body + "\nfrontend:\n"
	for x in list_issue_frontend:
		mail_body = mail_body + x.encode('utf-8') + "\n"

if len(list_issue_feature) > 0:
	list_issue_feature.sort()
	mail_body = mail_body + "\nfeature:\n"
	for x in list_issue_feature:
		mail_body = mail_body + x.encode('utf-8') + "\n"

if len(list_issue_devops) > 0:
	list_issue_devops.sort()
	mail_body = mail_body + "\ndevops:\n"
	for x in list_issue_devops:
		mail_body = mail_body + x.encode('utf-8') + "\n"

if len(list_issue_doc) > 0:
	list_issue_doc.sort()
	mail_body = mail_body + "\ndoc:\n"
	for x in list_issue_doc:
		mail_body = mail_body + x.encode('utf-8') + "\n"

if len(list_issue_other) > 0:
	list_issue_other.sort()
	mail_body = mail_body + "\n其他:\n"
	for x in list_issue_other:
		mail_body = mail_body + x.encode('utf-8') + "\n"

print mail_body

# 寄信
def send_mail_kuansim():
	to = 'kuansim@googlegroups.com'
	gmail_user = raw_input("username:\n")
	gmail_pwd = raw_input("password:\n")
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.login(gmail_user, gmail_pwd)

	today = datetime.date.today()
	strSubject = "待認領任務 (%s)" % (today.strftime('%m/%d'))
	strSubject = Header(strSubject, 'utf-8')
	# header = 'To:' + to + '\n' + 'From:' + gmail_user + '\n' + 'Subject:' + strSubject + '\n'

	msg = MIMEText(mail_body, 'plain', 'utf-8')
	msg['From'] = gmail_user
	msg['To'] = to
	msg['Subject'] = strSubject
	# msg = header + mail_body
	# print msg
	smtpserver.sendmail(gmail_user, to, msg.as_string())
	print 'done!'
	smtpserver.close()
	
send_mail_kuansim()
