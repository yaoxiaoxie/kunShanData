# _*_ coding : utf-8 _*_
# @Time : 14/4/2024 上午10:02
# @Author : Yao-Xie
# @File    : Ai_byd
# @Project : autosendemail
# @Product : PyCharm
# Des : 获取主页面的caseID


import json
import os
import re
import urllib.request
from lxml import etree


def create_request(page):
    if(page == 1):
        url = 'https://tdms.lenovo.com/tdms/caseMgtAction!clickTree.do?cid=2309&cname=Subsystem&pid=2301&lv=4&r=4&sysPageId=page_test_caselibrary_view'
    else:
        url = 'https://sc.chinaz.com/tupian/qinglvtupian_' + str(page) + '.html'

    headers = {
        ##'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        'Cookie': '151=1; 152=0; 236=1; 237=1; blackbird={pos:1,size:0,load:null}; leid=1.xaRQszGnO68; JSESSIONID=89AC850AF9B11ED83F2C802FC67C2BD3',
        # 'Host': 'tdms.lenovo.com',
        # 'Referer': 'https://tdms.lenovo.com/tdms/caseMgtAction!clickTree.do?cid=1786&cname=Lenovo%20SW%20Test%20Case%202025%20Architecture&pid=1&lv=1&r=4&sysPageId=page_test_caselibrary_view',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }

    request = urllib.request.Request(url = url, headers = headers)
    return request


def get_content(request):
    try:
        with urllib.request.urlopen(request,timeout=10) as response:
            return response.read().decode('UTF-8')
    except Exception as e:
        print(f"❌获取网页内容失败:{e}")
        return None


def get_data(content:str):

    tree = etree.HTML(content)
    # 获取所有a标签元素
    a_elements = tree.xpath('//*[@id="caseList"]//a')

    data_list = []
    for a in a_elements:
        # 获取href属性
        href = a.xpath('./@href')[0] if a.xpath('./@href') else ''
        # 获取文本内容
        text = a.xpath('./text()')[0].strip() if a.xpath('./text()') else ''

        # 提取 caseid 中的数字部分
        match = re.search(r"fxviewCase\('(\d+)'\)", href)
        caseTrueId = match.group(1) if match else None

        if caseTrueId and text:
            data_list.append({
                'caseTrueId': caseTrueId,
                'caseId': text
            })

    return data_list

def save_to_json(data, filename="renBaoCaseId.json"):
    """将数据保存到JSON文件"""
    try:
        # 确保保存目录存在
        if not os.path.exists('data_files'):
            os.makedirs('data_files')

        # 构建完整路径
        file_path = os.path.join('data_files', filename)

        # 写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            # indent=2 让JSON格式更易读
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅数据已保存到{file_path}")
        return True
    except Exception as e:
        print(f"❌保存JSON文件出错:{e}")
        return False


if __name__ == '__main__':
        request = create_request(1)
        content = get_content(request)

        if content:
            case_data = get_data(content)
            print(f"✅共获取到{len(case_data)}条数据")
            save_to_json(case_data)
        else:
            print("⚠️未能获取有效的网页内容")





