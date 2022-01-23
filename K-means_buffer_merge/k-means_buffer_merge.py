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
import shapefile
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt


arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件

output_folder = os.getcwd()
# 创建空白 shp

inFeatures="buildings.shp"
outFeatureClass = "building_feature_to_point.shp"

Point_blank_shp = arcpy.CreateFeatureclass_management(
    output_folder, outFeatureClass, "Point")

arcpy.FeatureToPoint_management(inFeatures, Point_blank_shp, "INSIDE")

reader = shapefile.Reader(outFeatureClass)
# shapes= reader.shape()
print reader.fields

points_xy_list=list()

for i in range(len(reader.records())):
    print reader.record(i)
    print reader.shape(i).points
    points_xy_fields_list=list()
    points_xy_list.append(reader.shape(i).points[0])

print points_xy_list

# w=open("buildings_point.txt","w")
# for i in range(len(points_xy_list)):
#     w.writelines(str(points_xy_list[i][0])+","+str(points_xy_list[i][1])+"\n")
#
# w.close()

X=np.array(points_xy_list)
print X

kmeans = KMeans(n_clusters=4, random_state=0,n_init=15,algorithm="full").fit(X)

C=kmeans.labels_ #输出原始数据的聚类后的标签值
print C

plt.figure()
plt.scatter(X[:, 0], X[:, 1], c=C)
plt.show()

arcpy.AddField_management(inFeatures, "my_class", "TEXT", field_length=5)
with  arcpy.da.UpdateCursor(inFeatures, ["my_class"]) as cursor:
    class_i=0
    for row in cursor:
        row[0] = C[class_i]
        # print "更改完成"
        cursor.updateRow(row)
        class_i+=1

del cursor

arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件

output_folder = os.getcwd()
# 创建空白 shp

firet_outFeatureClass = "first_buffer_" + inFeatures

Polygon_blank_shp = arcpy.CreateFeatureclass_management(
    output_folder, firet_outFeatureClass, "Polygon")

arcpy.Buffer_analysis(in_features=inFeatures,
                      out_feature_class=Polygon_blank_shp,
                      buffer_distance_or_field="50 Meter",
                      line_side="FULL",
                      dissolve_option="LIST",
                      dissolve_field="my_class")

twice_outFeatureClass = "twice_buffer_" + inFeatures

Polygon_blank_shp = arcpy.CreateFeatureclass_management(
    output_folder, twice_outFeatureClass, "Polygon")

arcpy.Buffer_analysis(in_features=firet_outFeatureClass,
                      out_feature_class=Polygon_blank_shp,
                      buffer_distance_or_field="-50 Meter",
                      line_side="FULL",
                      dissolve_option="ALL"
                      )







