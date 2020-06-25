from pyecharts.charts import Pie,Bar
from pyecharts import options as opts
import requests

from pyecharts.options.global_options import ThemeType
import json
import pprint



url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
response=requests.get(url)
data = json.loads(requests.get(url=url).json()['data'])  #json.loads()方法将字符串类型转换成字典类型
china = data['areaTree'][0]['children']

pprint.pprint(china)

province_distribution = {}

i = 0
while i <= 33:
    key = china[i]['name']   #china[0]['北京']
    province_distribution[key]=province_distribution.get(key,0)+china[i]['total']['confirm']
    i += 1

pie=Pie(init_opts=opts.InitOpts(width='900px',height='900px'))
pie.add('12',data_pair=province_distribution.items())
pie.set_global_opts(title_opts=opts.TitleOpts(title='coronavirus'))
pie.render('piecorona.html')


a=list(province_distribution)
b=list(province_distribution.values())
bar=Bar(init_opts=opts.InitOpts(width='1200px',height='700px',bg_color='rgba(255,250,205,0.2'))
bar.add_xaxis(a)
bar.add_yaxis('city',b)
bar.set_global_opts(title_opts=opts.TitleOpts(title='coronavirus china city situation'))
bar.render('bar.html')
print(a,b)