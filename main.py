# 导入模块
import os
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange,Font_type




import json
from pyJianYingDraft import Keyframe_property, SEC


import tkinter as tk
from tkinter import filedialog


import pyJianYingDraft as draft
from pyJianYingDraft import Font_type, Text_style, Clip_settings
from pyJianYingDraft.text_segment import Text_border



def get_folder_path():
    # 隐藏 Tkinter 主窗口
    root = tk.Tk()
    root.withdraw()
    
    # 弹出文件夹选择对话框
    folder_path = filedialog.askdirectory()
    
    return folder_path
def get_file_path(type):
    # 隐藏 Tkinter 主窗口
    root = tk.Tk()
    root.withdraw()
    
    # 弹出文件夹选择对话框
    file_path = filedialog.askopenfilename(
        title="选择文件",
        filetypes=[("文本文件", f"*.{type}")])
    
    return file_path



config_path = get_file_path('json')
mp3_file = get_file_path('mp3')
srt_file = get_file_path('srt')
# output_path = get_file_path('json')



# config_path = './config.json'

# 创建剪映草稿
script = draft.Script_file(2048, 2048*0.75) 

# 添加音频、视频和文本轨道
script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)



with open(config_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 输出加载的数据
print(data)

left = 0
right = 0

total_duration = 0



for idx,item in enumerate(data):
    print(idx,item)
    video_material = draft.Video_material(item['filePath'])
    script.add_material(video_material)

    # 计算时常
    curren_duration = sum(k['duration'] for k in item['textList'])/1000
    right = left + curren_duration

  
    video_segment = draft.Video_segment(video_material, trange(f"{left}s", f"{curren_duration}s")) 
    left = right


    

    if idx % 6 == 0:
        video_segment.add_keyframe(Keyframe_property.uniform_scale,0,1.33)
        length = 0.25
        if curren_duration >= 5:
            length = 0.25
        else:
            length = 0.25 * (curren_duration/5)
        video_segment.add_keyframe(Keyframe_property.position_y,0,-length)

        video_segment.add_keyframe(Keyframe_property.position_y,int(video_segment.duration) ,length)

    if idx % 6 == 1:
        video_segment.add_keyframe(Keyframe_property.uniform_scale,0,1.33)
        length = 0.25
        if curren_duration >= 5:
            length = 0.25
        else:
            length = 0.25 * (curren_duration/5)
        video_segment.add_keyframe(Keyframe_property.position_y,0,length)

        video_segment.add_keyframe(Keyframe_property.position_y,int(video_segment.duration) ,-length)
    
    if idx % 6 == 2:
        video_segment.add_keyframe(Keyframe_property.uniform_scale,0,1.43)
        length = 0.08
        if curren_duration >= 5:
            length = 0.08
        else:
            length = 0.08 * (curren_duration/5)
        video_segment.add_keyframe(Keyframe_property.position_x,0,length)

        video_segment.add_keyframe(Keyframe_property.position_x,int(video_segment.duration) ,-length)

    if idx % 6 == 3:
        video_segment.add_keyframe(Keyframe_property.uniform_scale,0,1.43)
        length = 0.08
        if curren_duration >= 5:
            length = 0.08
        else:
            length = 0.08 * (curren_duration/5)
        video_segment.add_keyframe(Keyframe_property.position_x,0,-length)

        video_segment.add_keyframe(Keyframe_property.position_x,int(video_segment.duration) ,length)
    

    if idx % 6 == 5:
        
        scale = 1.53
        if curren_duration >= 5:
            scale = 1.53
        else:
            scale = 0.2 * (curren_duration/5) + 1.33
        video_segment.add_keyframe(Keyframe_property.uniform_scale,0,scale)
        video_segment.add_keyframe(Keyframe_property.uniform_scale,int(video_segment.duration),1.33)
    if idx % 6 == 4:
        
        scale = 1.53
        if curren_duration >= 5:
            scale = 1.53
        else:
            scale = 0.2 * (curren_duration/5) + 1.33
        video_segment.add_keyframe(Keyframe_property.uniform_scale,0,1.33)
        video_segment.add_keyframe(Keyframe_property.uniform_scale,int(video_segment.duration),scale)



    # 将片段1添加到轨道中
    script.add_segment(video_segment)

# 添加音频

audio_material = draft.Audio_material(mp3_file)
script.add_material(audio_material)
audio_segment = draft.Audio_segment(audio_material,trange(f"0s",f"{audio_material.duration/1000000}s"))  
script.add_segment(audio_segment)


# 带下划线、位置及大小类似字幕的浅蓝色文本
seg1 = draft.Text_segment("Subtitle", trange("0s", "10s"),
                          font=Font_type.后现代体,
                          style=Text_style(size=9.0, color=(1, 0.87, 0), align=1),
                          border=Text_border(color=(0,0,0))
                          )

# 字幕
script.import_srt(srt_file,
 track_name="subtitle",
  style_reference=seg1
)


script.dump("E:/jianying/draft/JianyingPro Drafts/7月12日/draft_content.json")
