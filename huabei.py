# -*- coding: utf-8 -*-

import requests
import json
import time

class HuaBei:

    def __init__(self):
        return

    time_type = {
        'a1': '10点前',
        'n1': '10~12点',
        'n2': '12~14点',
        'p1': '14点后'
    }

    #雪场照片
    __api_snow_pack_list = 'https://api.fenxuekeji.com/api/pw/photo_walls'
    #雪场推荐照片墙
    __api_snow_pack_recommend_photo_walls = 'https://api.fenxuekeji.com/api/pw/photo_walls/%s/recommend_list'
    #雪场每日列表
    __api_snow_pack_day_list = 'https://api.fenxuekeji.com/api/pw/photo_walls/%s/dailies'
    #雪场某天照片墙
    __api_snow_pack_photo_walls_by_day = 'https://api.fenxuekeji.com/api/pw/photo_walls/%s/daily'

    #公用网络请求
    def __request(self, url, params, method = 'GET'):
        if method == 'GET':
            return requests.get(url, params = params, verify = False)
        return requests.post(url, data = params, verify = False)

    #获取雪场列表
    def get_snow_pack_list(self, page = 1):
        params = {'able_type': 'ski_ranch', 'lat': 39.97696126302083, 'lng': '116.4195960828993', 'page': page}
        data = self.__request(self.__api_snow_pack_list, params)

        ret = {'has_next_page': False, 'list': []}
        if isinstance(data.json(), dict):
            data = data.json()['data']
            ret['has_next_page'] = True if data['pagination']['current_page'] < data['pagination']['total_pages'] else False

            for item in data['photo_walls']:
                ret['list'].append({
                    'name': item['name'],
                    'update_time': time.strftime("%m-%d %H:%M", time.localtime(int(item['updated_at']))),
                    'uuid': item['uuid'],
                    'photos_count': item['photos_count'],
                    'description': item['description'],
                    'cover': item['cover']['x400'],
                })

        return ret

    #获取雪场日期列表(PC照片)
    def get_snow_pack_day_list(self, uuid, page = 1):
        params = {'device': 'pc', 'page': page}
        data = self.__request(self.__api_snow_pack_day_list %uuid, params)
        ret = {'title': '', 'has_next_page': False, 'list': []}
        if isinstance(data.json(), dict):
            data = data.json()['data']
            ret['title'] = data['photo_wall']['name']
            ret['has_next_page'] = True if data['page'] < data['total_pages'] else False
            for item in data['dailies']:
                ret['list'].append({
                    'date': item['date'],
                    'count': item['count'],
                    'cover': item['cover']['x500'],
                })
        return ret

    #雪场某天照片列表
    def get_snow_pack_photo_walls_by_day(self, uuid, date_string, apn, page = 1):
        params = {'apn': apn, 'datestring': date_string, 'device': 'pc', 'page': page}
        data = self.__request(self.__api_snow_pack_photo_walls_by_day %uuid, params)
        ret = {'title': self.time_type[apn], 'has_next_page': False, 'list': []}
        if isinstance(data.json(), dict):
            data = data.json()['data']
            ret['has_next_page'] = True if data['page'] < data['total_pages'] else False
            for item in data['photos']:
                ret['list'].append({
                    'cover': item['image']['x500'],
                    'src': item['image']['x1000'].split('!')[0],
                })
        return ret


    #雪场推荐照片
    def get_photo_walls(self, uuid, page = 1):
        api_url = self.__ApiPhotoWalls %uuid
        params = {'page': page}
        data = self.__request(api_url, params)
        ret = {'title': '', 'has_next_page': False, 'list': []}
        if isinstance(data.json(), dict):
            data = data.json()['data']
            ret['has_next_page'] = True if data['pagination']['current_page'] < data['pagination']['total_pages'] else False
            for item in data['recommend_list']:
                ret.append({
                    'cover': item['image']['x400'],
                    #watermark
                    'src': item['image']['x1000'].split('!')[0],
                })
        return ret
