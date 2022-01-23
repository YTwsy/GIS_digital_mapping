# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: YT.wsy
# Created on: 2021/12/10
# Reference:
"""
Description:Python2.7
Usage:
"""
# ---------------------------------------------------------------------------

import arcpy
import os

buffer_list=["building1.shp","building2.shp",
             "building3.shp","building4.shp"]

for i in range(4):
    arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件

    output_folder = os.getcwd()
    # 创建空白 shp

    firet_outFeatureClass = "first_buffer_"+buffer_list[i]

    Polygon_blank_shp = arcpy.CreateFeatureclass_management(
        output_folder, firet_outFeatureClass, "Polygon")

    arcpy.Buffer_analysis(in_features=buffer_list[i],
                          out_feature_class=Polygon_blank_shp,
                          buffer_distance_or_field="50 Meter",
                          line_side="FULL",
                          dissolve_option="ALL")

    twice_outFeatureClass = "twice_buffer_"+buffer_list[i]

    Polygon_blank_shp = arcpy.CreateFeatureclass_management(
        output_folder, twice_outFeatureClass, "Polygon")

    arcpy.Buffer_analysis(in_features=firet_outFeatureClass,
                          out_feature_class=Polygon_blank_shp,
                          buffer_distance_or_field="-50 Meter",
                          line_side="FULL",
                          dissolve_option="ALL")



