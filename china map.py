from pyecharts.charts import Map
from pyecharts import options as opts
import requests
import json
import pprint
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
response=requests.get(url)
data = json.loads(requests.get(url=url).json()['data'])  #json.loads()方法将字符串类型转换成字典类型
china = data['areaTree'][0]['children']

pprint.pprint(china)

province_distribution = {}
tip_distribution={}
i = 0
while i <= 33:
    key = china[i]['name']   #china[0]['北京']
    province_distribution[key]=province_distribution.get(key,0)+china[i]['total']['confirm']
    tip_distribution[key]=str(tip_distribution.get(key,0))+china[i]['today']['tip']
    i += 1


map = Map(init_opts=opts.InitOpts(width="1300px", height="900px")) #全局配置 初始化图片的大小

map.set_global_opts(
 title_opts=opts.TitleOpts(title="实时疫情地图 %s\n\n累计确诊 %d\n现有疑似 %d\n累计治愈 %d\n累计死亡 %d" #%s打印字符串 %d打印整形数组\
                           %(data['lastUpdateTime'],data['chinaTotal']['confirm'],\
                             data['chinaTotal']['suspect'],data['chinaTotal']['heal'],data['chinaTotal']['dead'])),
 visualmap_opts=opts.VisualMapOpts(max_=3600, is_piecewise=True,
          pieces=[
          {"max": 1999999, "min": 10000, "label": "10000人及以上", "color": "#8A0808"},
          {"max": 9999, "min": 1000, "label": "1000-9999人", "color": "#B40404"},
          {"max": 999, "min": 500, "label": "500-999人", "color": "#DF0101"},
          {"max": 499, "min": 100, "label": "100-499人", "color": "#F78181"},
          {"max": 99, "min": 10, "label": "10-99人", "color": "#F5A9A9"},
          {"max": 9, "min": 0, "label": "1-9人", "color": "#FFFFCC"},
          ], )
 )
map.add("确诊", data_pair=province_distribution.items(),maptype="china", is_roam=True)
map.render('chinacoronavirus.html')