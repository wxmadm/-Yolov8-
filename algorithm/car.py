import cv2
from collections import  defaultdict
import numpy as np
from time import time
import time as tim

from PyQt5.QtGui import QImage, QPixmap
from ultralytics.utils.plotting import Annotator, colors
from utils.playMusic import *
from utils.dataBaseService import DataBaseService,ChaoSu


settings = {
    "MYSQL_HOST":"localhost",
    "MYSQL_DBNAME":"cardatabase",
    "MYSQL_USER":"root",
    "MYSQL_PASSWD":"123456",
    "MYSQL_CHARSET":"utf8",
    "MYSQL_PORT":3306
}
db = DataBaseService.connect(settings)
PlayMusic.music_path='sound'
old_track_ids=[]
im0 = None     #原始图像
annotator = None    #注解器
#区域信息
reg_pts = [(20,400),(1260,400)] #速度计算区域点
region_thickness = 3  #区域线条厚度
#预测/跟踪信息
clss = None #类别
boxes = None #边界框
trk_ids = None #跟踪id
trk_pts = None  #跟踪点
trk_history = defaultdict(list)  #跟踪历史
#速度统计信息
current_time = 0  #当前时间
dist_data = {} #速度数据
trk_idslist = [] #跟踪ID列表
spdl_dist_thresh = 10  #欧式距离阈值
trk_previous_times={}  #先前时间的记录
trk_previous_points={}  #先前点的记录
chaosu=[]  #超速记载
def car(img,results,combo_box,track_history,width,height):

    global old_track_ids
    global chaosu
    global db
    bbox=results[0].boxes.data.cpu().tolist()  # 点的位置
    estimate_speed(img, results, width, height)   # 预估速度算法
    if results[0].boxes.id is not None:
        track_ids = results[0].boxes.id.int().cpu().tolist()
        for id1 in old_track_ids:
            if id1 not in track_ids:
                for i in range(combo_box.count()):
                    if str(combo_box.itemText(i)) == str(id1):
                        combo_box.removeItem(i)
                        break  # 追踪单个目标


        for id2 in track_ids:
            if id2 not in old_track_ids:
                combo_box.addItem(str(id2))
        old_track_ids = track_ids
    preprocess = results[0].speed['preprocess']
    inference = results[0].speed['inference']
    postprocess = results[0].speed['postprocess' ]

    FPS=int(1000/(preprocess+postprocess+inference))    #测fps   (preprocess+postprocess+inference)
    speed=0
    s=0
    re_x=0
    re_y=0

    id = 0

    if bbox != []:
        for temp in bbox:
            if len(temp) == 7:    #=7说明追踪到了
                score = temp[5]
                cls = temp[6]
                id = int(temp[4])

            else:
                score = temp[4]
                cls = temp[5]

            if combo_box.currentText() == str(id):  # 当前框选的是单个车辆
                speed = int(dist_data[id]/150) if id in dist_data else "未过速度检测线"
                re_x = (int(temp[0]) + int(temp[2]))/2  # 中心点x坐标
                re_y = (int(temp[1]) + int(temp[3]))/2  # 中心点y坐标
                s = round(score, 2)

            if combo_box.currentText() == str(id) or combo_box.currentText() == "全体车辆":
                if id in dist_data:
                    if int(dist_data[id]/150)>60:
                        cv2.rectangle(img,(int(temp[0]),int(temp[1])),(int(temp[2]),int(temp[3])),
                                           (0,0,255),2)  #左上角和右下角的位置
                        img = cv2.putText(img,"id:"+str(int(id)) + " " + "class:" + str(
                        "car") + " " + "speed:" + f"{int(dist_data[id]/150)}km/ph",
                                      (int(temp[0]),int(temp[1]) - 5),
                                       cv2.FONT_HERSHEY_SIMPLEX,0.5,(105,237,249),1)

                        if id not in chaosu:
                            PlayMusic.chaosu()
                            localtime = tim.localtime(tim.time())
                            bjtime = str(localtime[0]) + '年' +str(localtime[1])+'月'+str(
                                localtime[2]) + '日' +str(
                                localtime[3]) + '时' +str(localtime[4]) + '分' +str(localtime[5]) + '秒'
                            local = r'output\%sid%s.jpg' % (bjtime,str(id))    #超速的年月日
                            cv2.imencode('.jpg',img)[1].tofile(r'output\%sid%s.jpg' % (bjtime,str(id)))#写图片
                            data =ChaoSu() # 调用数据库算法
                            data.num = id
                            data.speed = int(dist_data[id] / 150)
                            data.time = tim.strftime("%Y-%m-%d %H:%M:%S",tim.localtime())
                            data.local = str(local)
                            db.insertToList(data)
                            chaosu.append(id) # 只截一张图

                    else:
                        cv2.rectangle(img, (int(temp[0]), int(temp[1])), (int(temp[2]), int(temp[3])),
                                      (0, 255, 0), 2)
                        img = cv2.putText(img, "id:" + str(int(id)) + " " + "class:" + str("car") + " " + "speed:"+ f"{int(dist_data[id]/150)}km/ph",      # f"{int(dist_data[id]/3)}km/ph"
                                          (int(temp[0]), int(temp[1]) - 5),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (105, 237, 249), 1)

                else:
                    cv2.rectangle(img, (int(temp[0]), int(temp[1])), (int(temp[2]), int(temp[3])),
                                  (0, 255, 0), 2)
                    img = cv2.putText(img, "id:" + str(int(id)) + " " + "class:" + str("car") + " " +str(round(score,2)),
                                      (int(temp[0]), int(temp[1]) - 5),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (105, 237, 249), 1)
        box_xy = results[0].boxes.xywh.cpu().numpy()

# 画轨迹
        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
            for box,track_id in zip(box_xy,track_ids):
                if combo_box.currentText() == str(track_id) or combo_box.currentText() == "全体车辆":
                    x,y,w,h = box
                    track =track_history[track_id]
                    track.append((float(x),float(y)))
                    if len(track)>15:
                        track.pop(0)
                    points =  np.hstack(track).astype(np.int32).reshape((-1,1,2))
                    cv2.polylines(img,[points],isClosed=False,color=(0,255,0),thickness=10)   # 画线
    return img,id,speed,s,int(re_x),int(re_y),FPS


#提取跟踪信息的方法
def extract_tracks( tracks):
    global boxes
    global trk_ids
    global clss
    boxes = tracks[0].boxes.xyxy.cpu()  # 边界框
    clss = tracks[0].boxes.cls.cpu().tolist()   # 类别
    trk_ids = tracks[0].boxes.id.int().cpu().tolist()   # 跟踪ID

def store_track_info(track_id, box):
    global trk_history
    global trk_pts
    # 存储追踪信息
    track = trk_history[track_id]    # 存在历史的点位，形成追踪的线条
    bbox_center = (float((box[0]+box[2]) / 2), float((box[1]+box[3])/2))  # 中心点的位置
    track.append(bbox_center)

    if len(track) > 30:
        track.pop(0)

    trk_pts = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
    return track

def calculate_speed(trk_id,track):
    global reg_pts
    global spdl_dist_thresh
    global trk_previous_times
    global trk_idslis
    global trk_previous_points
    global dist_data

    if not reg_pts[0][1] < track[-1][1] < reg_pts[1][1]:   # 基准线
        return
    if reg_pts[1][0] - spdl_dist_thresh < track[-1][0] < reg_pts[0][1] + spdl_dist_thresh:
        direction = "known"
    elif reg_pts[0][0] - spdl_dist_thresh < track[-1][0] < reg_pts[0][0] + spdl_dist_thresh:
        direction = "known"
    else:
        direction = "unknown"   # 方向

    if trk_previous_times[trk_id] != 0 and direction != "unknown" and trk_id not in trk_idslist:
        trk_idslist.append(trk_id)

        time_difference = time() - trk_previous_times[trk_id]
        if time_difference>0:
            dist_difference = np.abs(track[-1][0] - trk_previous_points[trk_id][1])
            speed = dist_difference / time_difference    # 速度计算
            dist_data[trk_id] = speed


    trk_previous_times[trk_id] = time()
    trk_previous_points[trk_id] = track[-1]


#  存储追踪信息的方法
def estimate_speed( im0, tracks, width, height):
    global reg_pts
    global boxes
    global trk_ids
    global clss
    global trk_previous_times
    # 计算基于跟踪数据的物体速度
    reg_pts = [(width/2, 0), (width/2, height)]   # 阈值线，计算物体的速度
    im0 =im0
    if tracks[0].boxes.id is not None:
        extract_tracks(tracks)
        annotator = Annotator(im0, line_width=2)
        annotator.draw_region(reg_pts=reg_pts, color=(255, 0, 0), thickness=region_thickness)
        for box, trk_id, cls in zip(boxes, trk_ids, clss):
            track = store_track_info(trk_id, box)
            if trk_id not in trk_previous_times:
                trk_previous_times[trk_id] = 0
            calculate_speed(trk_id, track)