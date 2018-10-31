from lxml import etree
import requests
import execjs
import time
import os
import multiprocessing as mp

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}
url = "http://jandan.net/ooxx"

def main():
    t1 = time.time()
    pool = mp.Pool(4)
    for _offset in range(10):
        pool.apply_async(func=task, args=(_offset, ))
    pool.close()
    pool.join()

    cost = time.time() - t1
    line = "Jandan进程池爬取10页时间: " + str(cost)
    with open("ooxx_spiders.txt", "w") as txt:
        txt.write(line)

def task(_offset):
    global headers, url
    html = requests.get(url=url, headers=headers).text
    tree = etree.HTML(html)
    current_page = int(tree.xpath('//span[@class="current-comment-page"]/text()')[0][1:-1])

    my_page = current_page - _offset
    html = requests.get(url=''.join([url, '/page-', str(my_page)]), headers = headers).text
    tree = etree.HTML(html)
    img_hash = tree.xpath('//div[@class="text"]//span[@class="img-hash"]/text()')

    count = 0
    for each in img_hash:
        with open("./func.js", encoding='UTF-8') as f:
            line = f.readline()
            func = ''
            while line:
                func += line
                line = f.readline()

        ctx = execjs.compile(func)
        img_url = (ctx.call("jandan_load_img", each))

        if not os.path.exists(os.getcwd()+'/ooxx_jandan'):
            os.mkdir(os.getcwd()+'/ooxx_jandan')
        with open(''.join([os.getcwd()+'/ooxx_jandan', '/', str(_offset), '_', str(count), img_url[-4:]]), 'wb') as f:
            f.write(requests.get(''.join(['http:', img_url])).content)
            count += 1

    return True

if __name__ == "__main__":
    main()

