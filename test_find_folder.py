from jmcomic import *

cl = JmOption.default().new_jm_client(impl=JmApiClient)
cl.login('login name', 'password')

page = cl.favorite_folder()
for folder_info in page.folder_list:

    fname, fid = folder_info['name'], folder_info['FID']
    print(f'文件夹名: {fname}，文件夹id: {fid} {folder_info}')
    for aid, atitle in cl.favorite_folder(folder_id=fid):
        print(f"{aid}, {atitle}")