# 1. 自定义plugin类
from jmcomic import * #JmOptionPlugin, JmModuleConfig, FindUpdatePlugin, JmModuleConfig
from my_find_update_plugin.json_helper import load_json, save_json

update_list = dict()


# 自定义一个类，继承JmOptionPlugin
class MyFindUpdatePlugin(FindUpdatePlugin):
    # 指定你的插件的key
    plugin_key = 'my_find_update'

    # 实现invoke方法
    # 方法的参数可以自定义，这里假设方法只有一个参数 json_path
    def invoke(self, json_path, download_all) -> None:
        album_dict = dict()
        global update_list

        update_list = load_json(json_path)
        jm_log('MyFindUpdateInvoke',f'调取需要更新的json data')

        #搜索文件夹
        self.look_up_folder()

        #reconstruct update_list to album:photo id pairs.
        update_list['LastUpdate'] = ''
        for index, album in update_list['UpdateList'].items():
            if download_all:  #重新全抓取
                album["first_download"] = True
            if album["first_download"] or (not album['completed']):  #抓第一次下载的， 或者是未完结的漫画, 
                album_dict[index] =  album['photo_id']
        self.download_album_with_find_update(album_dict or {})

        save_json(json_path, update_list)
        jm_log('MyFindUpdateInvoke',f'保存更新后的json data')
        
    def look_up_folder(self):
        # global update_list
        #登录搜索收藏夹，如果json数据里没有收藏夹本子，那就加入下载队列。登录信息从plugins里面查找。
        for after_init_plugin in self.option.plugins._data['after_init']: 
            if after_init_plugin['plugin'] == 'login':
                login_info = after_init_plugin['kwargs']
        cl = JmOption.default().new_jm_client(impl=JmApiClient)
        cl.login(login_info['username'], login_info['password'])

        page = cl.favorite_folder()
        for folder_info in page.folder_list:
            fname, fid = folder_info['name'], folder_info['FID']
            update_list['FolderList'][fid] = fname #更新folder列表
            albums_in_folder = cl.favorite_folder(folder_id=fid)
            for aid, atitle in albums_in_folder:
                if aid not in update_list['UpdateList'].keys():
                    update_list['UpdateList'][str(aid)] = {
                        "photo_id":str(aid),
                        "title": atitle,
                        "completed": False,
                        "first_download": True,
                        "folder_id": fid}

    def download_album_with_find_update(self, dic: Dict[str, int]):
        from jmcomic.api import download_album
        from jmcomic.jm_downloader import JmDownloader

        # 带入漫画id, 章节id(第x章)，寻找该漫画下第x章节後的所有章节Id
        def find_update(album: JmAlbumDetail):
            if album.album_id not in dic:
                return album

            photo_ls = []
            photo_begin = int(dic[album.album_id]) 
            is_new_photo = False

            for photo in album:
                if is_new_photo:
                    photo_ls.append(photo)

                if int(photo.photo_id) == photo_begin:
                    is_new_photo = True
            return photo_ls

        class FindUpdateDownloader(JmDownloader):
            def do_filter(self, detail):
                global update_list
                if not detail.is_album():
                    return detail

                detail: JmAlbumDetail

                #如果不是第一次下载就只更新，否则下载全本
                return find_update(detail) if not update_list['UpdateList'][detail.id]["first_download"] else detail 
            
            def before_album(self, album: JmAlbumDetail):
                # 设定自定义路径字段folder的值，例如 baseDir/韩漫/Album/
                JmModuleConfig.AFIELD_ADVICE['folder'] = lambda album: f'{update_list['FolderList'][update_list['UpdateList'][album.album_id]['folder_id']]}'
                super().before_album(album)
                self.download_success_dict.setdefault(album, {})
                self.option.call_all_plugin(
                    'before_album',
                    album=album,
                    downloader=self,
                )

            @property
            def all_success(self) -> bool:
                """
                是否成功下载了全部图片

                该属性需要等到downloader的全部download_xxx方法完成后才有意义。
                覆盖原函数，这样即使使用filter也可以返回true
                """
                if len(self.download_failed_list) != 0:
                    return False
                return True
            
            def after_album(self, album: JmAlbumDetail):
                super().after_album(album)
                if not self.all_success: #记录下失败的章节图片
                    for failed_image in self.download_failed_list:
                        update_list['FailedList'][f'{album.album_id}-{album.name}-{failed_image[0].aid}-{failed_image[0].filename}'] = failed_image[0].download_url
                else:  #只有更新成功了才update json数据库
                    update_list['UpdateList'][album.album_id]['latest_title'] = f'{album[-1].index}-{album[-1].name}'
                    # 如果发现完结标签，将作品标为完结
                    if not update_list['UpdateList'][album.album_id]['completed'] and ('完結' in album.tags or '完结' in album.tags):
                        update_list['UpdateList'][album.album_id]['completed'] = True
                    
                    if update_list['UpdateList'][album.album_id]['photo_id'] != album[-1].photo_id: # Update newest chapter in json date
                        update_list['UpdateList'][album.album_id]['photo_id'] = album[-1].photo_id
                        update_list['LastUpdate'] += f'{album.name} 更新至 {album[-1].index}-{album[-1].name}\n'
                        jm_log('after_album,',f'{album.name} 更新至 {album[-1].index}-{album[-1].name}')
                    # 更新漫画为非第一次下载
                    update_list['UpdateList'][album.album_id]['first_download'] = False
                self.option.call_all_plugin(
                    'after_album',
                    album=album,
                    downloader=self,
                )

        # 调用下载api，指定option和downloader
        download_album(
            jm_album_id=dic.keys(),
            option=self.option,
            downloader=FindUpdateDownloader,
        )
