"""
@FileName：comment.py
@Description：
@Author：xieburou
@Time：2024/11/11/周一 22:40
@Website：wait...
"""

from bs4 import BeautifulSoup
from curl_cffi import requests

headers = {
    "accept": "text/html,*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "device-memory": "8",
    "downlink": "6.65",
    "dpr": "1.25",
    "ect": "4g",
    "origin": "https://www.amazon.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.amazon.com",
    "rtt": "200",
    "sec-ch-device-memory": "8",
    "sec-ch-dpr": "1.25",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"10.0.0"',
    "sec-ch-viewport-width": "1023",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}
cookies = {
    "x-main": "替换为自己的x-main cookie",
}
url = "https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_next_2"  # 接口指纹检测
for i in range(1, 11):
    data = {
        "sortBy": "",
        "reviewerType": "all_reviews",
        "formatType": "",
        "mediaType": "",
        "filterByStar": "",
        "filterByAge": "",
        "pageNumber": "" + str(i),  # 分页
        "filterByLanguage": "",
        "filterByKeyword": "",
        "shouldAppend": "undefined",
        "deviceType": "desktop",
        "canShowIntHeader": "undefined",
        "reftag": "cm_cr_arp_d_paging_btm_next_2",
        "pageSize": "10",
        "asin": "B00CH9QWOU",
        "scope": "reviewsAjax0",
    }

    response = requests.post(
        url,
        cookies=cookies,
        data=data,
        impersonate="chrome101",  # tls指纹
    )
    js_list = response.text.split("&&&")
    for item in js_list:
        cl_it = str(item).strip()
        if cl_it != "":
            cl_it = eval(cl_it)
            if len(cl_it) == 3 and 'data-hook="review"' in cl_it[2]:
                js_com = cl_it[2]
                ht = BeautifulSoup(js_com, "html5lib")
                span = ht.find_all("span")
                span_text = "\t".join(
                    [t.text.strip().replace("\s", "").replace("\n", "") for t in span]
                )
                print(span_text)
