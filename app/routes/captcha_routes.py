from flask import request, jsonify, current_app
from app.routes import api_bp
from app import limiter
from app.utils.stats import track_stats
from app.services.captcha_service import CaptchaService
from app.middleware.auth import require_api_key

# 初始化服务
captcha_service = CaptchaService()

@api_bp.route('/capcode', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('capcode')
@require_api_key
def capcode():
    """
    滑块验证码识别
    ---
    tags:
      - 验证码识别
    security:
      - ApiKeyAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            slidingImage:
              type: string
              description: 滑块图片（base64/URL）
            backImage:
              type: string
              description: 背景图片（base64/URL）
            simpleTarget:
              type: boolean
              default: true
              description: 是否使用简单目标模式
            preprocess:
              type: boolean
              default: false
              description: 是否预处理图片
    responses:
      200:
        description: 识别结果
      400:
        description: 请求参数错误
      500:
        description: 服务器错误
    """
    try:
        data = request.get_json()
        
        # 参数验证
        if not data:
            return jsonify({'error': '请求体不能为空'}), 400
        if 'slidingImage' not in data or 'backImage' not in data:
            return jsonify({'error': '缺少必需参数: slidingImage 和 backImage'}), 400
        
        result = captcha_service.slide_match(
            data['slidingImage'],
            data['backImage'],
            data.get('simpleTarget', True),
            data.get('preprocess', False)
        )
        
        if result is None:
            return jsonify({'error': '识别失败，请检查图片格式和内容'}), 500
        
        return jsonify({'success': True, 'result': result})
    except KeyError as e:
        return jsonify({'error': f'缺少必需参数: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        current_app.logger.error(f"滑块识别错误: {e}", exc_info=True)
        return jsonify({'error': '服务器内部错误'}), 500

@api_bp.route('/slideComparison', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('slideComparison')
@require_api_key
def slide_comparison():
    """滑块对比识别"""
    try:
        data = request.get_json()
        result = captcha_service.slide_comparison(
            data['slidingImage'],
            data['backImage']
        )
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/classification', methods=['POST'])
@limiter.limit("50 per minute")
@track_stats('classification')
@require_api_key
def classification():
    """
    OCR文字识别
    ---
    tags:
      - 验证码识别
    security:
      - ApiKeyAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            image:
              type: string
              description: 图片数据（base64/URL）
            preprocess:
              type: boolean
              default: false
              description: 是否预处理图片
    responses:
      200:
        description: 识别结果
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': '缺少必需参数: image'}), 400
        
        result = captcha_service.classify(
            data['image'],
            data.get('preprocess', False)
        )
        
        if result is None:
            return jsonify({'error': '识别失败，请检查图片格式'}), 500
        
        return jsonify({'success': True, 'result': result})
    except ValueError as e:
        return jsonify({'error': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        current_app.logger.error(f"OCR识别错误: {e}", exc_info=True)
        return jsonify({'error': '服务器内部错误'}), 500

@api_bp.route('/batch/classification', methods=['POST'])
@limiter.limit("10 per minute")
@track_stats('batch_classification')
@require_api_key
def batch_classification():
    """
    批量OCR文字识别
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            images:
              type: array
              items:
                type: string
              description: 图片数组（base64/URL）
            preprocess:
              type: boolean
              default: false
    responses:
      200:
        description: 批量识别结果
    """
    try:
        data = request.get_json()
        
        if not data or 'images' not in data:
            return jsonify({'error': '缺少必需参数: images'}), 400
        
        images = data['images']
        
        if not isinstance(images, list):
            return jsonify({'error': 'images 必须是数组'}), 400
        
        if len(images) == 0:
            return jsonify({'error': '图片数组不能为空'}), 400
        
        if len(images) > current_app.config['MAX_BATCH_SIZE']:
            return jsonify({
                'error': f'单次最多处理 {current_app.config["MAX_BATCH_SIZE"]} 张图片，当前: {len(images)}'
            }), 400
        
        result = captcha_service.batch_classify(
            images,
            data.get('preprocess', False)
        )
        
        if result is None:
            return jsonify({'error': '批量处理失败'}), 500
        
        return jsonify({'success': True, 'results': result, 'total': len(images)})
    except ValueError as e:
        return jsonify({'error': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        current_app.logger.error(f"批量识别错误: {e}", exc_info=True)
        return jsonify({'error': '服务器内部错误'}), 500

@api_bp.route('/detection', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('detection')
@require_api_key
def detection():
    """目标检测"""
    try:
        data = request.get_json()
        result = captcha_service.detect(data['image'])
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/calculate', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('calculate')
@require_api_key
def calculate():
    """计算类验证码识别"""
    try:
        data = request.get_json()
        result = captcha_service.calculate(data['image'])
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/crop', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('crop')
@require_api_key
def crop():
    """
    图片分割
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            image:
              type: string
              description: 图片数据（base64/URL）
            y_coordinate:
              type: integer
              description: Y轴分割坐标
    responses:
      200:
        description: 分割后的图片
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data or 'y_coordinate' not in data:
            return jsonify({'error': '缺少必需参数: image 和 y_coordinate'}), 400
        
        y_coord = data['y_coordinate']
        if not isinstance(y_coord, (int, float)) or y_coord <= 0:
            return jsonify({'error': 'y_coordinate 必须是正数'}), 400
        
        result = captcha_service.crop_image(data['image'], int(y_coord))
        
        if result is None:
            return jsonify({'error': '图片分割失败'}), 500
        
        return jsonify({'success': True, **result})
    except ValueError as e:
        return jsonify({'error': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        current_app.logger.error(f"图片分割错误: {e}", exc_info=True)
        return jsonify({'error': '服务器内部错误'}), 500

@api_bp.route('/select', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('select')
@require_api_key
def select():
    """点选验证码识别"""
    try:
        data = request.get_json()
        result = captcha_service.click_select(data['image'])
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
