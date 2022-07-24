from bs4 import BeautifulSoup

html = """
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2022年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""
soup = BeautifulSoup(html, "html.parser")
# 获取title对象
print(soup.title)
# 获取title标签名
print(soup.title.name)
# 获取title值
print(soup.title.string)

print(soup.find_all('p'))
print(soup.p['id'])


for a in soup.find_all('a'):
    print(a['href'])
    print(a.string)

