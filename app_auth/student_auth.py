import urllib
import urllib.request
import urllib.parse
import urllib.response
import urllib.error
import http.cookiejar
from lxml import etree


# 学生认证，使用学校网站数据
def auth(real_name, id_card, stu_id):
    is_man_input = {0: True, 1: True, 2: False, 3: False}
    is_stu_input = {0: True, 1: False, 2: True, 3: False}
    # 请求数据
    for index in range(0, 4):
        query_res = get_auth_data(
            real_name=real_name,
            id_card=id_card,
            is_man=is_man_input[index],
            is_stu=is_stu_input[index]
        )
        if query_res:
            # 对比学号是否一致
            if query_res['stu_id'] == stu_id:
                return query_res
            else:
                return False


def get_auth_data(real_name, id_card, is_man, is_stu):
    # 创建 cookie 管理器
    cookie = http.cookiejar.CookieJar()
    cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
    # 创建请求对象
    opener = urllib.request.build_opener(cookie_handler)
    urllib.request.install_opener(opener)
    # 构造请求数据
    url = "http://uia.hnist.cn/uiauser/patch/selfServiceQuery.action"
    # roleName 0 就是学生 1 教师
    data = ('domain.name=' + urllib.parse.quote(real_name) +
            '&domain.cardId=' + urllib.parse.quote(id_card) +
            '&genders=' + urllib.parse.quote("男" if is_man else "女") +
            '&roleName=' + urllib.parse.quote('0' if is_stu else '1')
            ).encode(encoding='utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    # 发起请求
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    # 解析html数据
    etree_html = etree.HTML(data)
    nodes = etree_html.xpath('//*[@id="showResult"]/table/tbody/tr[2]/td')
    if nodes[0].text == '暂无数据':
        return False
    else:
        return {
            'real_name': nodes[1].text,
            'stu_id': nodes[2].text,
            'id_card': nodes[3].text,
            'is_man': is_man,
            'is_stu': is_stu,
        }


# print(auth("曾广", "43092119971118577X", "14162400891"))
# print(auth("甘靖", "430602197709281303", "11999481"))
