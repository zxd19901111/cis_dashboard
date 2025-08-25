import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
from folium.plugins import Draw, Search

# 设置页面标题
st.set_page_config(page_title="交互式地图数据可视化", layout="wide")
st.title("动态地图数据可视化工具")

# 侧边栏配置
with st.sidebar:
    st.header("地图配置")
    center_lat = st.number_input("中心纬度", value=31.2304, format="%.6f")
    center_lng = st.number_input("中心经度", value=121.4737, format="%.6f")
    zoom_level = st.slider("初始缩放级别", 5, 18, 12)

    st.header("数据添加")
    add_marker = st.checkbox("添加标记点")
    add_polygon = st.checkbox("添加多边形区域")
    add_heatmap = st.checkbox("添加热力图")

# 创建地图
m = folium.Map(
    location=[center_lat, center_lng],
    zoom_start=zoom_level,
    tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
    attr='高德地图'
)

# 添加绘图工具
Draw(
    export=True,
    position='topleft',
    draw_options={
        'polyline': True,
        'rectangle': True,
        'circle': True,
        'marker': True,
        'circlemarker': False,
    }
).add_to(m)

# 添加示例数据（可替换为你的数据）
if add_marker:
    markers = [
        {"lat": 31.2304, "lng": 121.4737, "name": "人民广场", "info": "<b>人民广场</b><br>黄浦区核心区域"},
        {"lat": 31.2272, "lng": 121.4817, "name": "上海博物馆", "info": "<b>上海博物馆</b><br>馆藏丰富"},
    ]
    for marker in markers:
        folium.Marker(
            location=[marker["lat"], marker["lng"]],
            popup=folium.Popup(marker["info"], max_width=300),
            tooltip=marker["name"]
        ).add_to(m)

if add_polygon:
    folium.Polygon(
        locations=[
            [31.2140, 121.4630], [31.2140, 121.4900],
            [31.2350, 121.4900], [31.2350, 121.4630], [31.2140, 121.4630]
        ],
        popup="<b>黄浦区</b><br>上海市中心城区",
        tooltip="黄浦区",
        fill_color="blue",
        fill_opacity=0.3
    ).add_to(m)

if add_heatmap:
    heat_data = [
        [31.2304, 121.4737, 100], [31.2272, 121.4817, 80],
        [31.2154, 121.4583, 90], [31.2220, 121.4700, 60]
    ]
    plugins.HeatMap(heat_data).add_to(m)

# 在Streamlit中显示地图
st_folium(m, width="100%", height=600)

# 说明文本
st.markdown("""
### 使用说明
1. 地图支持缩放、平移、点击查看详情
2. 左侧工具栏可手动绘制点、线、多边形
3. 侧边栏可配置地图中心、缩放级别和添加的数据类型
4. 点击右上角「Deploy」可生成分享链接
""")
