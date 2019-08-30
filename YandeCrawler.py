import requests

def get_url(main_url):
    url_ls = []
    response = requests.get(main_url)
    result = response.text
    begin = result.find('Post.register')
    while (result.find('\"id\"', begin) != -1):
        begin = result.find('\"id\"', begin)
        url_ls.append('https://yande.re/post/show/'+result[begin + 5:result.find(',', begin)])
        begin = result.find('Post.register', begin)
    print(url_ls)
    print(len(url_ls))
    return(url_ls)

def download(url,file_name):
    #url = 'https://yande.re/post/show/561898'
    response = requests.get(url)
    result = response.text
    start=result.find('https://files.yande.re/image')
    end=result.find('jpg',start)+3
    large_url=result[start:end]
    print(large_url)
    response = requests.get(large_url)
    img = response.content
    with open(file_name, 'wb') as f:
        f.write(img)

if __name__ == '__main__':
    start_page=1
    end_page=1
    tags='sakimichan'
    url_ls=[]
    for i in range(end_page-start_page+1):
        main_url='https://yande.re/post?page='+str(i+start_page)+'&tags='+tags
        url_ls.extend(get_url(main_url))
        print('第%d页的图片链接已提取' %(i+start_page))
    print(url_ls)
    print(len(url_ls))
    i=1
    for url in url_ls:
        file_name=str(i)+'.jpg'
        download(url, file_name)
        i=i+1

