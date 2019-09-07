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

requested_function = ""

if source:
    conn = pymysql.connect("localhost", "coderush", "coderush", "coderush")
    c = conn.cursor()
    c.execute("select username, admin from users where username=%s and password=%s", (source["username"], source["password"]))
    r = c.fetchall()
    conn.close()
    if not len(r) or not r[0][1]:
        print("Location: login.py")
        print()
        os.sys.exit(0)

    if "usermanage" in form:
        requested_function = '''<!-- Create/Update User -->
        <div id="superset">
            <form method="post" action="''' + html.escape(os.environ["SCRIPT_NAME"]) + '''" enctype="multipart/form-data" autocomplete="on">
                <p>Create/Update User</p>
                <input placeholder="New Username" name="newusername" required="required" />
                <br />
                <br />
                <input type="password" placeholder="New Password" name="newpassword" required="required" />
                <br />
                <br />
                <input type="checkbox" id="newadmin" name="newadmin" value="1" />
                <label for="newadmin"><span><span></span></span>Administrator</label>
                <br />
                <br />
                <div class="bottom">
                    <input class="button bottom" type="submit" value="Done" />
                </div>
            </form>
        </div>
'''

    if "list" in form:
        requested_function ='''<table>
                <tr>
                    <th>Username</th>
                    <th>Level</th>
                    <th>Question</th>
                    <th>Language</th>
                    <th>Time</th>
                </tr>
'''

        conn = pymysql.connect("localhost", "coderush", "coderush", "coderush")
        c = conn.cursor()
        c.execute("select username, level, ques, language, curtime from submit")
        r = c.fetchall()
        conn.close()

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
            <form method="post" action="''', html.escape(os.environ["SCRIPT_NAME"]), '''" enctype="multipart/form-data" autocomplete="on">
                <input class="button" id="usermanage" type="submit" name="usermanage" value="Create/Update User" />
            </form>
            <form method="post" action="''', html.escape(os.environ["SCRIPT_NAME"]), '''" enctype="multipart/form-data" autocomplete="on">
                <input class="button" id="list" type="submit" name="list" value="List Submissions" />
            </form>
            <form method="post" action="''', html.escape(os.environ["SCRIPT_NAME"]), '''" enctype="multipart/form-data" autocomplete="on">
                <input class="button" id="dlsubmit" type="submit" name="dlsubmit" value="Download Submissions" />
            </form>
        </div>
        ''', requested_function, '''
    </body>
</html>
''',
sep = "", end = "")
