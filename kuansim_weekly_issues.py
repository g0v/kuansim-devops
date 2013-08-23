# -*- coding: utf-8 -*-
from github import Github
import sys
import datetime
import smtplib
from email.Header import Header
from email.mime.text import MIMEText

# 印出列表任務
def get_str_issue_by_label(list, label):
	str_body = ""
	if len(list) > 0:
		list.sort()
		str_body =  "%s\n%s:\n" % (str_body, label)
		for x in list:
			str_body = "%s%s\n" % (str_body, x.encode('utf-8'))
	return str_body

# 寄信
def send_mail_to_kuansim(user, pwd):
	to = 'kuansim@googlegroups.com'
	gmail_user = user
	gmail_pwd = pwd
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.login(gmail_user, gmail_pwd)

	today = datetime.date.today()
	strSubject = "待認領任務 (%s)" % (today.strftime('%m/%d'))
	strSubject = Header(strSubject, 'utf-8')

	msg = MIMEText(mail_body, 'plain', 'utf-8')
	msg['From'] = gmail_user
	msg['To'] = to
	msg['Subject'] = strSubject
	smtpserver.sendmail(gmail_user, to, msg.as_string())
	print 'done!'
	smtpserver.close()

# ============ 程式流程部分 ============
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
		if x.labels:
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
		else:
			list_issue_other.append("%s\t %s (https://github.com/g0v/kuansim/issues/%s)" % (x.number, x.title, x.number))

mail_body = mail_body + "待認領任務"

mail_body = mail_body + get_str_issue_by_label(list_issue_backend, "backend")
mail_body = mail_body + get_str_issue_by_label(list_issue_frontend, "frontend")
mail_body = mail_body + get_str_issue_by_label(list_issue_feature, "feature")
mail_body = mail_body + get_str_issue_by_label(list_issue_devops, "devops")
mail_body = mail_body + get_str_issue_by_label(list_issue_doc, "doc")
mail_body = mail_body + get_str_issue_by_label(list_issue_other, "其他")

print mail_body

if len(sys.argv) >= 3 and sys.argv[1] and sys.argv[2]:
	send_mail_to_kuansim(sys.argv[1], sys.argv[2])
else:
	user = raw_input("username:")
	pwd = raw_input("password:")
	send_mail_to_kuansim(user, pwd)