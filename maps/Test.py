import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    # 保存当前的样式状态
    saved_style_state = plt.rcParams.copy()

    # 检查文件是否存在并加载数据
    if os.path.isfile("../set9/trees-with-species-and-dimensions-urban-forest.csv"):
        filepath = "../set9/trees-with-species-and-dimensions-urban-forest.csv"
        print("Loading from file")
    else:
        filepath = "http://www.osr.nsw.gov.au/sites/default/files/file_manager/penalty_data_set_0.csv"
        print("Loading from the internet")

    tdf = pd.read_csv(filepath)

    # 创建图形
    fig0 = plt.figure(figsize=(10, 6), num=1)
    fig0_ax1 = fig0.add_subplot(111)

    # 读取和绘制 shapefile
    mel_prop = gpd.read_file("property-boundaries/property-boundaries.shp")

    # 确保坐标系一致
    if mel_prop.crs != "EPSG:4326":
        mel_prop = mel_prop.to_crs("EPSG:4326")

    # 绘制 GeoPandas 数据
    mel_prop.plot(ax=fig0_ax1)

    # 绘制散点图
    scatter = fig0_ax1.scatter(tdf["Longitude"], tdf["Latitude"],
                               c=tdf["Diameter Breast Height"],
                               cmap="rainbow", s=0.5)

    # 计算并标记最大值和平均值
    tree_dia_mean = tdf["Diameter Breast Height"].mean()
    tree_dia_max = tdf["Diameter Breast Height"].max()
    street_max_items = tdf[tdf["Diameter Breast Height"] == tree_dia_max]
    fig0_ax1.scatter(street_max_items["Longitude"], street_max_items["Latitude"],
                     c='red', marker="*", s=60, label="Max Diameter")

    # 添加文本框
    text_str = f'Mean: {tree_dia_mean:.2f}cm\nMax: {tree_dia_max:.2f}cm'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig0_ax1.text(0.70, 1.1, text_str, transform=fig0_ax1.transAxes, fontsize=12,
                  verticalalignment='top', bbox=props)

    # 设置标题和标签
    fig0_ax1.set_title("All Tree Diameter")
    fig0_ax1.set_xlabel("Longitude")
    fig0_ax1.set_ylabel("Latitude")

    # 添加图例
    fig0_ax1.legend()

    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=fig0_ax1)
    cbar.set_label('Diameter Breast Height')

    # 显示图形
    plt.show()
