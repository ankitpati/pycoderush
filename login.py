#!/usr/bin/env python3

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
login_reason = ""

if "logout" in form:
    cks = cookies.SimpleCookie()
    cks["username"] = ""
    cks["password"] = ""
    print(cks)
    login_reason = "<div id=\"note\">Logged Out</div>"
elif "username" in form and "password" in form:
    source = dict(username = form["username"].value, password = form["password"].value)
    login_reason = "<div id=\"note\">Incorrect Credentials</div>"
elif "username" in crumbs and "password" in crumbs:
    source = crumbs

if source:
    conn = pymysql.connect("localhost", "coderush", "coderush", "coderush")
    c = conn.cursor()
    c.execute("select username, admin from users where username=%s and password=%s", (source["username"], source["password"]))
    r = c.fetchall()
    conn.close()
    if len(r):
        if "username" in form:
            cks = cookies.SimpleCookie()
            cks["username"] = urllib.parse.quote(source["username"])
            cks["password"] = urllib.parse.quote(source["password"])
            print(cks)
        if r[0][1]:
            print("Location: admin.py")
            print()
        else:
            print("Location: uploader.py")
            print()
        os.sys.exit(0)

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
        <title>CodeRush</title>
        <link rel="stylesheet" type="text/css" href="css/style.css" />
    </head>
    <body spellcheck="false">
        <h1>CodeRush</h1>
        <div id="superset">
            ''', login_reason, '''
            <h2>Login</h2>
            <form method="post" action="''', html.escape(os.environ["SCRIPT_NAME"]), '''" enctype="multipart/form-data" autocomplete="on">
                <input placeholder="Username" name="username" required="required" />
                <br />
                <br />
                <input type="password" placeholder="Password" name="password" required="required" />
                <br />
                <br />
                <div class="bottom">
                    <input class="button bottom" type="submit" value="Done" />
                </div>
            </form>
        </div>
    </body>
</html>
''',
sep = "", end = "")
