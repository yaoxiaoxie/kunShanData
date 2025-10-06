# _*_ coding : utf-8 _*_
# @Time : 14/4/2024 上午10:02
# @Author : Yao-Xie
# @File    : Ai_byd
# @Project : autosendemail
# @Product : PyCharm
# Des : 从JSON读取case信息→分组→批量爬取case详情并保存HTML

import json
import os
import re
import urllib.request
from lxml import etree
from urllib.parse import urlparse, parse_qs  # 用于解析URL中的caseId



def create_request(caseTrueId):
    if(caseId == 1):
        url = 'https://tdms.lenovo.com/tdms/caseMgtAction!clickTree.do?cid=2309&cname=Subsystem&pid=2301&lv=4&r=4&sysPageId=page_test_caselibrary_view'
    else:
        url = 'https://tdms.lenovo.com/tdms/testCaseAction!loadCase.do?sysPageId=page_test_case_view&oper=0&caseType=1&cid=&cname=&caseId='+str(caseTrueId)+'&currentCategoryRole=4&entry=0'

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
        response = urllib.request.urlopen(request,timeout=10)
        content = response.read().decode('UTF-8')
        return content
    except Exception as e:
        print(f"❌获取内容出错:{e}")
        return None


def get_data_name(content):
    try:
        tree = etree.HTML(content)
        case_name = tree.xpath('//td/input[@name="caseBO.caseName"]/@value')
        return case_name[0] if case_name else "Unknown"
    except Exception as e:
        print(f"⚠️提取caseName出错:{e}")
        return "Unknown"

def save_to_html(content, caseId,caseName):
    """将数据保存到JSON文件"""
    try:
        # 确保保存目录存在
        save_dir = 'case_files/2025-EnhancedFunction-Subsystem'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 处理非法文件名字符
        safeCaseName = re.sub(r'[\\/:*?"<>|]', '_', caseName)
        safeCaseId = re.sub(r'[\\/:*?"<>|]', '_', caseId)

        filename = f'{safeCaseId}+{safeCaseName}.html'

        # 构建完整路径
        file_path = os.path.join(save_dir, filename)

        # 写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅已保存:{file_path}")
        return True
    except Exception as e:
        print(f"❌保存HTML出错:{e}")
        return False

def get_fromJson(jsonPath):
    try:
        with open(jsonPath, 'r', encoding='utf-8') as f:
            case_list = json.load(f)
    except Exception as e:
        print(f"❌无法读取JSON文件:{jsonPath}，错误：{e}")
        return

    print(f"\n📄共加载{len(case_list)}个用例（来自{os.path.basename(jsonPath)}）")

    valid_cases = []

    # 逐个处理
    for idx, case in enumerate(case_list, 1):
        caseTrueId = case.get("caseTrueId")
        caseId = case.get("caseId")

        print(f"\n[{idx}/{len(case_list)}] 正在处理: {caseId} (ID={caseTrueId})")

        if not caseId or not caseTrueId:
            print("⚠️缺少caseTrueId或caseId，跳过")
            print(f"⚠️第{idx}个用例缺少字段，跳过")
            continue

        valid_cases.append({"caseTrueId": caseTrueId, "caseId": caseId})

    return valid_cases


if __name__ == '__main__':

        jsonPath='renBaoCaseId.json'
        caseList = get_fromJson(jsonPath)
        for idx, case in enumerate(caseList, 1):
            caseTrueId = case["caseTrueId"]
            caseId = case["caseId"]
            print(f"\n[{idx}/{len(caseList)}]正在处理:{caseId}(ID={caseTrueId})")
            try:
                request = create_request(caseTrueId)
                content = get_content(request)
                if not content:
                    print("⚠️无法获取网页内容，跳过")
                    continue
                caseName = get_data_name(content)
                save_to_html(content,caseId,caseName)
            except Exception as e:
                print(f"❌处理{caseId}出错:{e}")

            print(f"\n🎉文件 {os.path.basename(jsonPath)}处理完成！")
        print("\n✅所有JSON文件处理完毕！")