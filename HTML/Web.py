#!/usr/bin/env python3

import cgi
import cgitb
import os

cgitb.enable()

form = cgi.FieldStorage()
print(form)
first_name = form.getvalue('first_name')
last_name = form.getvalue('last_name')

print ("Content-Type: text/html;charset=utf-8")
print ("Content-type:text/html\r\n")
print ("<!DOCTYPE html>")
print ("<html lang='en'>")
print ("<head>")
print ("<title>Hello - get CGI Program</title>")
print ("</head>")
print ("<body>")
print ("<h2>Hello %s %s</h2>" % (first_name, last_name))
print ("</body>")
print ("</html>")

