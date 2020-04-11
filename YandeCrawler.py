import requests
import os
import re
from concurrent import futures

def get_url(main_url):
    url_ls = []
    response = requests.get(main_url)
    result = response.text
    id_list=re.findall(r'Post.register\(\{\"id\":([0-9]+)',result,re.M)
    for id in id_list:
        url_ls.append('https://yande.re/post/show/' + id)
    return(url_ls)

def download(url,image_name,i):
    print('第%d张图片正在下载' %(i))
    response = requests.get(url)
    result = response.text
    start=result.find('https://files.yande.re/image')
    end=result.find('\"',start)
    large_url=result[start:end]#获取高清图片的url
    response = requests.get(large_url)
    img = response.content
    with open(image_name+'.'+large_url.split('.')[-1], 'wb') as f:#split分割获取图片格式后缀
        f.write(img)
    print('第%d张图片已完成下载' %(i))

if __name__ == '__main__':
    start_page=1
    end_page=10
    tags='sakimichan'
    num_thread=10
    url_ls=[]
    for i in range(end_page-start_page+1):
        main_url='https://yande.re/post?page='+str(i+start_page)+'&tags='+tags
        url_ls.extend(get_url(main_url))
        print('第%d页的图片链接已提取' %(i+start_page))
    print('一共%d张图片' %(len(url_ls)))
    file_name=tags+str(start_page)+'-'+str(end_page)#文件夹名字，默认与py文件在同一文件夹
    if not os.path.exists(file_name):
        os.mkdir(file_name)
    p = futures.ThreadPoolExecutor(max_workers=num_thread)
    for url in url_ls:
        image_name=file_name+'/'+str(url_ls.index(url)+1)
        future=p.submit(download, url, image_name, url_ls.index(url)+1)
    p.shutdown()
    print("下载完成")
