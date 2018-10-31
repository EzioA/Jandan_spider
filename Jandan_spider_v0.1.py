from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import execjs
import time
import multiprocessing as mp

headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
url = 'http://jiandan.net/ooxx'
##processings = []
##current_page = 0      在多进程执行中，子进程使用这种定义在主进程中的全局变量会出现奇怪的问题（fork出子进程时生成的全局变量怕不是直接从代码段拷贝过去了 XD）

def main():
        t1 = time.time()
##        for _offset in range(10):
##                processing = mp.Process(target = func, args = (soup, opener, _offset, current_page), name = 'T'+str(_offset))
##                processings.append(processing)
##                processing.start()
##        for _offset in range(10):
##                processings[_offset].join()

##        for _ in range(4):
##                processings[_].join()
##                print("hello, world")
        pool = mp.Pool(4)
        for _offset in range(10):
                pool.apply_async(func = task, args = (_offset,))
        pool.close()
        pool.join()
##        pool.map(func, args)
##        for each in threads:
##                each.start()
##                each.join()
##        func(soup, opener)
        temp = time.time() - t1
        line = "煎蛋进程池爬10页时间:"+str(temp)
        with open("jandan_pools.txt", 'w') as txt:
                txt.write(line)
        
def task(_offset):
        global headers, url     ##由于这两个变量我们不会进行修改，不存在fork出的进程与父全局变量之间的问题
        opener = urllib.request.build_opener()
        opener.add_handler = [headers]
        html = opener.open(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        current_page = int(soup.find(class_ = 'current-comment-page').text[1:-1])
        
        my_page = current_page - _offset
        html = opener.open(''.join([url, '/page-', str(my_page)])).read()
        print("Open")
        soup = BeautifulSoup(html, 'html5lib')
        ol = soup.find(name = 'ol', class_ = "commentlist")
        li = ol.find_all(name = 'li')
        count = 0

        for each in li:
                if each.has_attr('id') and not each.has_attr('class'):
                        img = each.find(name = 'img')
                        img_hash = img.next_sibling.text

                        ##调用JS代码
                        with open("./func1.js", encoding='UTF-8') as f:
                                line = f.readline()
                                func = ''
                                while line:
                                        func += line
                                        line = f.readline()
                        ctx = execjs.compile(func)
                        img_url = (ctx.call("jandan_load_img", img_hash))
                        
                        with open(''.join([r"C:/Users/ezio7/Desktop/img/", str(_offset), '_', str(count), img_url[-4:]]), 'wb') as f:
                                print("T"+str(_offset))
                                f.write(opener.open(''.join(['http:', img_url])).read())
                                count += 1
        return 1
                
        
if __name__ == "__main__":
        main()
