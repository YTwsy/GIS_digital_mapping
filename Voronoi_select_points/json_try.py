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
import json

def takeFirst(elem):
    return elem[0]

def select_points(json_name):
    f=open(json_name)
    dic_ts=json.load(f)
    print len(dic_ts["features"])
    dic_ts_all_polygons=dic_ts["features"]
    for i in range(len(dic_ts_all_polygons)):
        dic_ts_all_polygons[i]["selected"] = 0

    yudin_points_count=274          #548/2

    # last_max_weight_point=-1
    all_points_weight_and_objectid=list()
    for i in range(len(dic_ts_all_polygons)):
        weight = dic_ts_all_polygons[i]["properties"]["Floor"] * dic_ts_all_polygons[i]["properties"]["F_AREA"]
        list_on_weight_and_objectid=list()
        list_on_weight_and_objectid.append(weight)
        list_on_weight_and_objectid.append(dic_ts_all_polygons[i]["properties"]["OBJECTID"])
        all_points_weight_and_objectid.append(list_on_weight_and_objectid)

    # 指定第 1 个元素排序
    all_points_weight_and_objectid.sort(key=takeFirst)

    # 输出类别
    print('排序列表：')
    print(all_points_weight_and_objectid)

    while(len(dic_ts_all_polygons)>yudin_points_count):
        if(len(all_points_weight_and_objectid)==0):
            print "最终剩余的点都被固定，而点数仍然大于预定限值，需要继续进行综合工作"

            list_now_objectid = list()
            for i in range(len(dic_ts_all_polygons)):
                list_now_objectid.append(dic_ts_all_polygons[i]["properties"]["OBJECTID"])
            print list_now_objectid
            return list_now_objectid , 1
            break
        #是否所有点被固定
        flag_select=1   #都固定
        for p in range(len(dic_ts_all_polygons)):
            if (dic_ts_all_polygons[p]["selected"]==0):
                flag_select=0
                break

        if (flag_select==1):
            print "所有点被固定"
            break

        print "当前有"+str(len(dic_ts_all_polygons))+"个点"
        # max_weight=0
        # # max_weight_point=-1
        # for i in range(len(dic_ts_all_polygons)):
        #     weight=dic_ts_all_polygons[i]["properties"]["Floor"] * dic_ts_all_polygons[i]["properties"]["F_AREA"]
        #     if (weight>max_weight and dic_ts_all_polygons[i]["selected"]==0):
        #         max_weight=weight
        #         max_weight_point=dic_ts_all_polygons[i]["properties"]["OBJECTID"]
        #


        max_weight=all_points_weight_and_objectid[-1][0]
        max_weight_point=all_points_weight_and_objectid[-1][1]
        print max_weight
        print max_weight_point
        all_points_weight_and_objectid.pop(-1)

        set_one=list()

        max_weight_point_index=-1
        for i in range(len(dic_ts_all_polygons)):
            if (dic_ts_all_polygons[i]["properties"]["OBJECTID"]==max_weight_point):

                print dic_ts_all_polygons[i]["geometry"]["coordinates"][0]
                set_one=dic_ts_all_polygons[i]["geometry"]["coordinates"][0]
                max_weight_point_index=i
                break


        set_two=list()
        set_two_one=list()
        for i in range(len(dic_ts_all_polygons)):
            if (dic_ts_all_polygons[i]["properties"]["OBJECTID"]==max_weight_point):
                continue

            else:
                set_two=dic_ts_all_polygons[i]["geometry"]["coordinates"][0]
                for j in set_one:
                    for k in set_two:
                        if (j==k):
                            print dic_ts_all_polygons[i]["properties"]["OBJECTID"]
                            set_two_one.append(dic_ts_all_polygons[i]["properties"]["OBJECTID"])

        print sorted(set(set_two_one), key=set_two_one.index)
        set_two_one=sorted(set(set_two_one), key=set_two_one.index) #[491, 484, 265, 481]

        flag=0   #默认都是自由的
        for i in set_two_one:
            for j in range(len(dic_ts_all_polygons)):
                if (dic_ts_all_polygons[j]["properties"]["OBJECTID"]==i):

                    if(dic_ts_all_polygons[j]["selected"]==0):    #自由的
                        continue
                    else:
                        flag=1  #有固定点
                        continue

        print flag
        if(flag==0):
            #如果该点及其一阶邻近点都是“自由”的，将其从点群中删除，然后将该点的一阶邻近点标记为“固定”
            print dic_ts_all_polygons.pop(max_weight_point_index)
            for o in set_two_one:
                for k in range(len(dic_ts_all_polygons)):
                    if (dic_ts_all_polygons[k]["properties"]["OBJECTID"] == o):
                        dic_ts_all_polygons[k]["selected"] =1


        # else:
        #     print dic_ts_all_polygons.pop(max_weight_point_index)
        #     #否则，不进行处理
        #     #但重要性点不可以再有它

    print "未删除的点即为选取结果:"

    list_now_objectid = list()
    for i in range(len(dic_ts_all_polygons)):
        list_now_objectid.append(dic_ts_all_polygons[i]["properties"]["OBJECTID"])
    print list_now_objectid
    return list_now_objectid ,0





if __name__ == '__main__':
    select_points("ts_point.json")




