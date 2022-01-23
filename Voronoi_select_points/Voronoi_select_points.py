# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: YT.wsy
# Created on: 2021/12/3
# Reference:
"""
Description:Python2.7
Usage:
"""
# ---------------------------------------------------------------------------

import arcpy
import numpy
import os
import shapefile
from json import dumps
import json_try as jt



def buiud_area_tiesson(in_points,ts_with_area):
    arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件
    arcpy.env.outputMFlag ="Enabled"

    output_folder = os.getcwd()
    # 创建空白 shp

    inFeatures=in_points+".shp"
    outFeatureClass=in_points+"_x"+".shp"

    Polygon_blank_shp = arcpy.CreateFeatureclass_management(
        output_folder, outFeatureClass, "Polygon", spatial_reference=None)


    outFields="ALL"

    #泰森多边形
    arcpy.CreateThiessenPolygons_analysis(inFeatures, Polygon_blank_shp, outFields)

    #泰森多边形with面积
    area_Polygon_blank_shp = arcpy.CreateFeatureclass_management(
        output_folder, ts_with_area+".shp", "Polygon", spatial_reference=None)
    arcpy.CalculateAreas_stats(Polygon_blank_shp, area_Polygon_blank_shp)



def poly_to_json(thiessen_with_area,ts_point_json):
    reader = shapefile.Reader(thiessen_with_area)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    geojson = open(ts_point_json+".json", "w")
    geojson.write(dumps({"type": "FeatureCollection","features": buffer}, indent=4) + '\n')
    geojson.close()

    # import json
    # dic_ts=json.load("ts_point.json")
    # print dic_ts

def new_point(list_now_objectid,inshp,outshp):
    reader = shapefile.Reader(inshp+".shp")
    # shapes= reader.shape()
    print reader.fields
    for i in range(len(reader.records())):
        print reader.record(i)
        print reader.shape(i).points

    writer = shapefile.Writer(outshp+".shp",shapeType=1)
    writer.field(u'OBJECTID', u'N', 9, 0)
    writer.field(u'Id', u'N', 9, 0)
    writer.field(u'Floor', u'N', 9, 0)

#第一次时 fid 就是 objectid - 1 ，之后不是
    for i in list_now_objectid:
        # i=i-1  #    get_fid
        # writer.point(reader.shape(i).points[0][0],reader.shape(i).points[0][1])
        # writer.record(reader.record(i)[0],reader.record(i)[1],reader.record(i)[2])

        for j in range(len(reader.records())):
            if(reader.record(j)[0] == i):
                writer.point(reader.shape(j).points[0][0], reader.shape(j).points[0][1])
                writer.record(reader.record(j)[0], reader.record(j)[1], reader.record(j)[2])


if __name__ == '__main__':

    i=0
    buiud_area_tiesson("points", "ts_area_" + str(i))
    poly_to_json("ts_area_" + str(i) + ".shp", "ts_json_" + str(i))
    list_now_objectid_and_successful = jt.select_points("ts_json_" + str(i) + ".json")
    new_point(list_now_objectid_and_successful[0], 'points', 'point_' + str(i))
    i+=1

    if (list_now_objectid_and_successful[1] == 0):
        print "选取结果为" + 'point' + "_" + str(i) + ".shp"

    else:
        while(True):
            buiud_area_tiesson("point_"+ str(i),"ts_area_"+str(i))
            poly_to_json("ts_area_"+str(i)+".shp","ts_json_"+str(i))
            list_now_objectid_and_successful=jt.select_points("ts_json_"+str(i)+".json")
            new_point(list_now_objectid_and_successful[0], 'point_' + str(i), 'point_' + str(i+1))

            if (list_now_objectid_and_successful[1] == 0):
                break

            else:
                i+=1

        print "选取结果为"+'point'+"_"+str(i+1)+".shp"





