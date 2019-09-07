#!/usr/bin/env python3

'''DEBUG SECTION'''
import cgitb
cgitb.enable()
'''REMOVE BEFORE DEPLOYMENT'''

import urllib, http, pymysql, cgi, os, html, time
from http import cookies

form = cgi.FieldStorage()
crumbs = {}

if "HTTP_COOKIE" in os.environ:
    cks = os.environ["HTTP_COOKIE"]
    cks = cks.split("; ")
    for ck in cks:
        ck = ck.split("=")
        crumbs[ck[0]] = urllib.parse.unquote(ck[1])

source = None

if "username" in crumbs and "password" in crumbs:
    source = crumbs
else:
    print("Location: login.py")
    print()
    os.sys.exit(0)

if source:
    conn = pymysql.connect("localhost", "coderush", "coderush", "coderush")
    c = conn.cursor()
    c.execute("select username, admin from users where username=%s and password=%s", (source["username"], source["password"]))
    r = c.fetchall()
    conn.close()
    if not len(r) or r[0][1]:
        print("Location: login.py")
        print()
        os.sys.exit(0)

ext_permit = {"c", "h", "lzma", "7z", "zip"}
upload_status = ""

if "level" in form and "ques" in form and "ans" in form:
    upfile = form["ans"]

    if upfile.file:
        ufn = os.path.basename(upfile.filename)
        ulang = os.path.splitext(ufn)[1]
        if ulang:
            ulang = ulang[1:]
        if ulang not in ext_permit:
            upload_status = "<div id=\"note\">Unsupported Format</div>"
    else:
        upload_status = "<div id=\"note\">Upload Failed</div>"

    if not upload_status:
        udata = upfile.file.read(65535)
        conn = pymysql.connect("localhost", "coderush", "coderush", "coderush")
        c = conn.cursor()
        c.execute("insert into submit (username, level, ques, filename, language, ans, curtime) values(%s, %s, %s, %s, %s, %s, now()) on duplicate key update filename=%s, language=%s, ans=%s", (source["username"], form["level"].value, form["ques"].value, ufn, ulang, udata, ufn, ulang, udata))
        conn.commit()
        conn.close()
        upload_status = "<div id=\"note\">File Uploaded</div>"

print("Content-Type: text/html")
print("Expires: Wed, 13 Dec 1995 05:43:00 GMT");
print("Last-Modified:", time.strftime("%a, %d %b %Y %T GMT", time.gmtime()));
print("Cache-Control: private, no-store, max-age=0, no-cache, must-revalidate, post-check=0, pre-check=0");
print()

print('''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
    <head>
        <meta charset="UTF-8" />
        <meta name="theme-color" content="#300a24" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Code Uploader</title>
        <link rel="stylesheet" type="text/css" href="css/style.css" />
    </head>
    <body spellcheck="false">
        <h1>CodeRush</h1>
        <div id="superset">
            <h2><div class="truncate" title="''', html.escape(source["username"]), '''">''', html.escape(source["username"]), '''</div>
                <form method="post" action="''', "login.py" ,'''" enctype="multipart/form-data" autocomplete="on">
                    <input class="button" id="logout" type="submit" name="logout" value="Logout" />
                </form>
            </h2>
            ''', upload_status, '''
            <form method="post" action="''', html.escape(os.environ["SCRIPT_NAME"]), '''" enctype="multipart/form-data" autocomplete="on">
                <input placeholder="Level" name="level" maxlength="1" pattern="^[1-3]{1}$" title="1, 2, or 3" required="required" />
                <br />
                <br />
                <input placeholder="Question" name="ques" maxlength="2" pattern="^[0-9]{1,2}$" title="Maximum of 2 digits" required="required" />
                <br />
                <br />
                <input type="file" name="ans" required="required" />
                <div class="bottom">
                    <input class="button bottom" type="submit" value="Done" />
                </div>
            </form>
        </div>
    </body>
</html>
''',
sep = "", end = "")
