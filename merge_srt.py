import pysrt

# 合并字幕文件的函数
def merge_srt(files):
    all_subtitles = []  # 用于存储所有字幕
    last_end_time = None  # 最后的结束时间，初始为None
    index_offset = 0  # 用于调整第二个文件及之后文件的字幕序号

    for idx,file in enumerate(files):
        subs = pysrt.open(file)  # 使用pysrt打开字幕文件
        
        for sub in subs:
            # 如果前面有字幕，则将当前字幕的开始时间设为前一个字幕的结束时间
            if last_end_time:
                 # 设置当前字幕的开始时间
                sub.end = last_end_time  + (sub.end - sub.start)  # 保持当前字幕的时长，并计算结束时间
                sub.start = last_end_time 
            # if idx == 1:
            #     print(sub.end,last_end_time)
            #     exit()
            last_end_time = sub.end  # 更新最后的结束时间为当前字幕的结束时间
            
            # 更新字幕的序号，确保序号连续
            sub.index = index_offset
            index_offset+=1

            all_subtitles.append(sub)  # 将当前字幕添加到结果列表

        # 更新序号偏移量，确保下一个文件的字幕序号从当前文件的最后一个字幕序号开始
        # index_offset = all_subtitles[-1].index

    # 创建一个pysrt对象来保存合并后的字幕
    merged_subs = pysrt.SubRipFile(all_subtitles)
    
    # 保存合并后的字幕到新文件
    output_file = './output/merge.srt'
    merged_subs.save(output_file, encoding='utf-8')
    return output_file
# 示例使用
if __name__ == "__main__":
    srt_files = ['./input/1.srt', './input/2.srt']  # 请替换为实际的文件路径
    merged_file = merge_srt(srt_files)
    print(f'Merged subtitles saved to: {merged_file}')
