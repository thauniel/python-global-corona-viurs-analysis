from pyecharts.charts import Map
from pyecharts import options as opts
import requests
import parsel

url="https://ncov2019.live/"
html=requests.get(url)
k=html.text
selector = parsel.Selector(k)
def worlddata():
    worldrows = selector.css('#sortable_table_world tbody tr')
    worldname = worldrows.css('.save-button::attr(data-name)').getall()
    for name in worldname:
        if name=='South Sudan':
            worldname[worldname.index(name)]='S. Sudan'
    for name in worldname:
        if name=='Central African Republic':
            worldname[worldname.index(name)]='Central African Rep.'
    for name in worldname:
        if name=='DR Congo':
            worldname[worldname.index(name)]='Dem. Rep. Congo'
    for name in worldname:
        if name=='Western Sahara':
            worldname[worldname.index(name)]='W. Sahara'

    worldconfirmed = list(
        map(lambda x: x.strip().replace(',', ''), worldrows.css('td:nth-child(2)::text').getall()))
    worldconfirmed.pop(0)
    worlddata = dict(zip(worldname, worldconfirmed))
    print(worlddata)
    return worlddata

def australiadata():
    australiarows=selector.css('#sortable_table_australia tbody tr')
    australianame = australiarows.css('.save-button::attr(data-name)').getall()
    australianame.append('Australia')
    australiaconfirmed = list(map(lambda x: x.strip().replace(',', ''), australiarows.css('td:nth-child(2)::text').getall()))
    australiaconfirmed.append(7436)
    australiaconfirmed.pop(0)
    australiadata = dict(zip(australianame, australiaconfirmed))
    print(len(australianame), len(australiaconfirmed))
    print(australiadata)
    return australiadata

def eudata():
    eurows=selector.css('#sortable_table_europe tbody tr')
    euname = eurows.css('.save-button::attr(data-name)').getall()
    euname.append('Greenland')
    euconfirmed = list(map(lambda x: x.strip().replace(',', ''), eurows.css('td:nth-child(2)::text').getall()))
    euconfirmed.append(13)
    euconfirmed.pop(0)
    eudata = dict(zip(euname, euconfirmed))
    return eudata

# def afdata():
#     afrows=selector.css('#sortable_table_africa tbody tr')
#     afname = afrows.css('.save-button::attr(data-name)').getall()
#     for name in afname:
#         if name=='South Sudan':
#             afname[afname.index(name)]='S.Sudan'
#     afname[6] = 'Central African Rep'
#     afconfirmed = list(map(lambda x:x.strip().replace(',',''),afrows.css('td:nth-child(2)::text').getall()))
#     a=dict(zip(afname,afconfirmed))
#     return a

def asdata():
    asrows=selector.css('#sortable_table_asia tbody tr')
    asname = asrows.css('.save-button::attr(data-name)').getall()
    asname.append('Korea')
    asconfirmed = list(map(lambda x: x.strip().replace(',', ''), asrows.css('td:nth-child(2)::text').getall()))
    asconfirmed.append('1277')
    asconfirmed.pop(0)
    asdata = dict(zip(asname, asconfirmed))

    return asdata
def combinedata():
    dict2={}
    # dict2.update(afdata())
    dict2.update(asdata())
    dict2.update(eudata())
    dict2.update(australiadata())
    dict2.update(worlddata())
    print(dict2)
    return dict2.items()


image = Map( init_opts=opts.InitOpts(width="1900px", height="900px", bg_color="#ADD8E6",
	page_title="全球疫情确诊人数",theme="white"))
image.set_global_opts(
visualmap_opts=opts.VisualMapOpts(max_=3600, is_piecewise=True,
          pieces=[
          {"max": 5000000, "min": 999999, "label": "10000人及以上", "color": "#8A0808"},
          {"max": 999999, "min": 99999, "label": "1000-9999人", "color": "#B40404"},
          {"max": 99999, "min": 10000, "label": "500-999人", "color": "#DF0101"},
          {"max": 10000, "min": 9999, "label": "100-499人", "color": "#F78181"},
          {"max": 9999, "min": 1000, "label": "10-99人", "color": "#F5A9A9"},
          {"max": 1000, "min": 0, "label": "1-9人", "color": "#FFFFCC"},
          ], )
)
image.add('confirmed people',is_map_symbol_show=False,data_pair=combinedata(),is_roam=True,
    maptype="world")

image.render('world_map.html')
combinedata()