"""定义片段基类及部分比较通用的属性类"""

import uuid

from typing import Optional, Dict, List, Any

from .time_util import Timerange
from .keyframe import Keyframe_list

class Base_segment:
    """片段基类"""

    segment_id: str
    """片段全局id, 由程序自动生成"""
    material_id: str
    """使用的素材id"""
    target_timerange: Timerange
    """片段在轨道上的时间范围"""

    common_keyframes: List[Keyframe_list]
    """各属性的关键帧列表"""

    def __init__(self, material_id: str, target_timerange: Timerange):
        self.segment_id = uuid.uuid4().hex
        self.material_id = material_id
        self.target_timerange = target_timerange

        self.common_keyframes = []

    @property
    def start(self) -> int:
        """片段开始时间, 单位为微秒"""
        return self.target_timerange.start
    @start.setter
    def start(self, value: int):
        self.target_timerange.start = value

    @property
    def duration(self) -> int:
        """片段持续时间, 单位为微秒"""
        return self.target_timerange.duration
    @duration.setter
    def duration(self, value: int):
        self.target_timerange.duration = value

    @property
    def end(self) -> int:
        """片段结束时间, 单位为微秒"""
        return self.target_timerange.end

    def overlaps(self, other: "Base_segment") -> bool:
        """判断是否与另一个片段有重叠"""
        return self.target_timerange.overlaps(other.target_timerange)

    def export_json(self) -> Dict[str, Any]:
        """返回通用于各种片段的属性"""
        return {
            "enable_adjust": True,
            "enable_color_correct_adjust": False,
            "enable_color_curves": True,
            "enable_color_match_adjust": False,
            "enable_color_wheels": True,
            "enable_lut": True,
            "enable_smart_color_adjust": False,
            "last_nonzero_volume": 1.0,
            "reverse": False,
            "track_attribute": 0,
            "track_render_index": 0,
            "visible": True,
            # 写入自定义字段
            "id": self.segment_id,
            "material_id": self.material_id,
            "target_timerange": self.target_timerange.export_json(),

            "common_keyframes": [kf_list.export_json() for kf_list in self.common_keyframes],
            "keyframe_refs": [],  # 意义不明
        }

class Speed:
    """播放速度对象, 目前只支持固定速度"""

    global_id: str
    """全局id, 由程序自动生成"""
    speed: float
    """播放速度"""

    def __init__(self, speed: float):
        self.global_id = uuid.uuid4().hex
        self.speed = speed

    def export_json(self) -> Dict[str, Any]:
        return {
            "curve_speed": None,
            "id": self.global_id,
            "mode": 0,
            "speed": self.speed,
            "type": "speed"
        }

class Clip_settings:
    """素材片段的图像调节设置"""

    alpha: float
    """图像不透明度, 0-1"""
    flip_horizontal: bool
    """是否水平翻转"""
    flip_vertical: bool
    """是否垂直翻转"""
    rotation: float
    """顺时针旋转的**角度**, 可正可负"""
    scale_x: float
    """水平缩放比例"""
    scale_y: float
    """垂直缩放比例"""
    transform_x: float
    """水平位移, 单位为半个画布宽?"""
    transform_y: float
    """垂直位移, 单位为半个画布高?"""

    def __init__(self, *, alpha: float = 1.0,
                 flip_horizontal: bool = False, flip_vertical: bool = False,
                 rotation: float = 0.0,
                 scale_x: float = 1.0, scale_y: float = 1.0,
                 transform_x: float = 0.0, transform_y: float = 0.0):
        """初始化图像调节设置, 默认不作任何图像变换

        Args:
            alpha (float, optional): 图像不透明度, 0-1. 默认为1.0.
            flip_horizontal (bool, optional): 是否水平翻转. 默认为False.
            flip_vertical (bool, optional): 是否垂直翻转. 默认为False.
            rotation (float, optional): 顺时针旋转的**角度**, 可正可负. 默认为0.0.
            scale_x (float, optional): 水平缩放比例. 默认为1.0.
            scale_y (float, optional): 垂直缩放比例. 默认为1.0.
            transform_x (float, optional): 水平位移, 单位为半个画布宽. 默认为0.0.
            transform_y (float, optional): 垂直位移, 单位为半个画布高. 默认为0.0.
                参考: 剪映导入的字幕似乎取此值为-0.8
        """
        self.alpha = alpha
        self.flip_horizontal, self.flip_vertical = flip_horizontal, flip_vertical
        self.rotation = rotation
        self.scale_x, self.scale_y = scale_x, scale_y
        self.transform_x, self.transform_y = transform_x, transform_y

    def export_json(self) -> Dict[str, Any]:
        clip_settings_json = {
            "alpha": self.alpha,
            "flip": {"horizontal": self.flip_horizontal, "vertical": self.flip_vertical},
            "rotation": self.rotation,
            "scale": {"x": self.scale_x, "y": self.scale_y},
            "transform": {"x": self.transform_x, "y": self.transform_y}
        }
        return clip_settings_json

class Media_segment(Base_segment):
    """媒体片段基类"""

    source_timerange: Optional[Timerange]
    """截取的素材片段的时间范围, 对贴纸而言不存在"""
    speed: Speed
    """播放速度设置"""
    volume: float
    """音量"""

    extra_material_refs: List[str]
    """附加的素材id列表, 用于链接动画/特效等"""

    def __init__(self, material_id: str, source_timerange: Optional[Timerange], target_timerange: Timerange, speed: float, volume: float):
        super().__init__(material_id, target_timerange)

        self.source_timerange = source_timerange
        self.speed = Speed(speed)
        self.volume = volume

        self.extra_material_refs = [self.speed.global_id]

    def export_json(self) -> Dict[str, Any]:
        """返回通用于音频和视频片段的默认属性"""
        ret = super().export_json()
        ret.update({
            "source_timerange": self.source_timerange.export_json() if self.source_timerange else None,
            "speed": self.speed.speed,
            "volume": self.volume,
            "extra_material_refs": self.extra_material_refs,
        })
        return ret
