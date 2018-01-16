# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story" data-foo="value">...</p>
</body>
</html>
"""

soup2 = BeautifulSoup(html, "xml")
print soup2

soup = BeautifulSoup(html, "lxml")


# soup = BeautifulSoup(open('index.html'))

# print soup.prettify()

# 遍历子dom
# for child in soup.body.children:
#     print child

# 递归遍历子dom
# for child in soup.body.descendants:
#     print child

# print soup.body.p.attrs, soup.body.p['class'], soup.body.p['name'], soup.body.p.string
# print type(soup.a.string)

# if isinstance(BeautifulSoup.element.Comment, soup.a.string):
# # if type(soup.a.string) == bs4.element.Comment:
#     print 'yes'
#     print soup.a.string

# # 遍历全部文字
# for string in soup.strings:
#     print(repr(string))
# # 遍历全部文字，跳过空行
# for string in soup.stripped_strings:
#     print(repr(string))

# # 获取父dom
# p = soup.p
# print p.parent.name
#
# content = soup.head.title.string
# for parent in content.parents:
#     print parent.name

# # 获取兄弟dom
# print '--' ,soup.p.string, soup.p.next_sibling
# #       实际该处为空白
# print soup.p.prev_sibling
# #None   没有前一个兄弟节点，返回 None
# print soup.p.next_sibling.next_sibling.next_sibling.next_sibling
# for sibling in soup.a.next_siblings:
#     print(repr(sibling))

# # 获取前后节点
# print soup.head.next_element
#
# print soup.p.contents[0], '==='
# for element in soup.p.contents[0].next_elements:
#     print(repr(element))

# # 搜索功能
# print soup.find_all('a')
#
# for tag in soup.find_all(re.compile("^b")):
#     print(tag)
#
# def has_class_but_no_id(tag):
#     return tag.has_attr('class') and not tag.has_attr('id')
#
# print soup.find_all(has_class_but_no_id)

# print soup.find_all(id='link2',class_='sister')
# print soup.find_all(href=re.compile("elsie"))
# print soup.find_all(attrs={"data-foo": "value"})

# print soup.select('title')
#
# print soup.select('.sister')
# print soup.find_all(class_='sister')

# print soup.body.find_all(class_='story')[0].get_text('', strip=True)
#
# for text in soup.stripped_strings:
#     print text









