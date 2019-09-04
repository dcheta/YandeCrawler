import requests
import os
from concurrent import futures

def get_url(main_url):
    url_ls = []
    response = requests.get(main_url)
    result = response.text
    begin = result.find('Post.register')
    while (result.find('\"id\"', begin) != -1):
        begin = result.find('\"id\"', begin)
        url_ls.append('https://yande.re/post/show/'+result[begin + 5:result.find(',', begin)])
        begin = result.find('Post.register', begin)
    return(url_ls)

def download(url,file_name,i):
    print('第%d张图片正在下载' %(i))
    response = requests.get(url)
    result = response.text
    start=result.find('https://files.yande.re/image')
    end=result.find('jpg',start)+3
    large_url=result[start:end]
    response = requests.get(large_url)
    img = response.content
    with open(file_name, 'wb') as f:
        f.write(img)
    print('第%d张图片已完成下载' %(i))

if __name__ == '__main__':
    start_page=1
    end_page=1
    tags='sakimichan'
    num_thread=5
    url_ls=[]
    for i in range(end_page-start_page+1):
        main_url='https://yande.re/post?page='+str(i+start_page)+'&tags='+tags
        url_ls.extend(get_url(main_url))
        print('第%d页的图片链接已提取' %(i+start_page))
    print(url_ls)
    print(len(url_ls))
    if not os.path.exists(tags):
        os.mkdir(tags)
    p = futures.ThreadPoolExecutor(max_workers=num_thread)
    for url in url_ls:
        file_name=tags+'/'+str(url_ls.index(url))+'.jpg'
        #download(url, file_name)
        future=p.submit(download, url, tags+'/'+str(url_ls.index(url)+1)+'.jpg', url_ls.index(url)+1)
    p.shutdown()
    print("下载完成")


