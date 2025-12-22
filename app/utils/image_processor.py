import base64
from io import BytesIO
import cv2
import numpy as np
import requests
from PIL import Image, ImageEnhance

def get_image_bytes(image_data, max_size=5*1024*1024, timeout=10):
    """
    将不同格式的图像数据转换为字节流
    
    Args:
        image_data: 图片数据（bytes/URL/base64）
        max_size: 最大文件大小（字节）
        timeout: 请求超时时间（秒）
    
    Returns:
        bytes: 图片字节流
    
    Raises:
        ValueError: 不支持的数据类型或文件过大
    """
    if isinstance(image_data, bytes):
        if len(image_data) > max_size:
            raise ValueError(f"图片大小超过限制: {len(image_data)} > {max_size}")
        return image_data
    
    elif isinstance(image_data, str):
        # 判断是否为URL
        if image_data.startswith(('http://', 'https://')):
            try:
                response = requests.get(
                    image_data, 
                    timeout=timeout,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    verify=True,  # 启用 SSL 验证
                    allow_redirects=True,
                    stream=True  # 流式下载，避免大文件问题
                )
                response.raise_for_status()
                
                # 读取内容
                content = b''
                for chunk in response.iter_content(chunk_size=8192):
                    content += chunk
                    if len(content) > max_size:
                        raise ValueError(f"图片大小超过限制: {len(content)} > {max_size}")
                
                return content
            except requests.RequestException as e:
                raise ValueError(f"图片下载失败: {str(e)}")
        
        # 否则当作base64处理
        else:
            try:
                # 移除可能的data URI前缀
                if ',' in image_data and image_data.startswith('data:'):
                    image_data = image_data.split(',', 1)[1]
                
                decoded = base64.b64decode(image_data)
                if len(decoded) > max_size:
                    raise ValueError(f"图片大小超过限制: {len(decoded)} > {max_size}")
                
                return decoded
            except Exception as e:
                raise ValueError(f"Base64解码失败: {str(e)}")
    
    else:
        raise ValueError(f"不支持的图片数据类型: {type(image_data)}")

def preprocess_image(image_bytes, enhance=False, denoise=False, binarize=False):
    """
    图片预处理函数
    
    Args:
        image_bytes: 图片字节流
        enhance: 是否增强对比度和锐度
        denoise: 是否去噪
        binarize: 是否二值化
    
    Returns:
        bytes: 处理后的图片字节流
    """
    try:
        image = Image.open(BytesIO(image_bytes))
        
        # 转换为RGB模式（处理RGBA、灰度等格式）
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        
        if enhance:
            # 增强对比度（调整为更温和的参数）
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            # 增强锐度
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
        
        # 转换为numpy数组用于OpenCV处理
        img_array = np.array(image)
        
        # 确保是3通道图像
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        
        if denoise:
            # 去噪 - 使用更安全的参数
            try:
                img_array = cv2.fastNlMeansDenoisingColored(img_array, None, 3, 3, 7, 21)
            except Exception:
                # 如果去噪失败，跳过此步骤
                pass
        
        if binarize:
            # 转灰度
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            # 自适应二值化（效果更好）
            img_array = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
        
        # 转回bytes
        _, buffer = cv2.imencode('.png', img_array)
        return buffer.tobytes()
    except Exception as e:
        raise Exception(f"图片预处理错误: {e}")

def image_to_base64(image, format='PNG'):
    """将PIL图像转换为Base64字符串"""
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str
