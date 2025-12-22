from datetime import datetime
from flask import jsonify
from app.routes import api_bp
from app.utils.stats import get_stats_data
import logging

# 获取 logger，用于过滤健康检查日志
log = logging.getLogger('werkzeug')

@api_bp.route('/', methods=['GET'])
def api_info():
    """
    API首页
    ---
    responses:
      200:
        description: 欢迎信息
    """
    return jsonify({
        'message': 'CAPTCHA识别API运行成功！',
        'version': '2.0',
        'docs': '/docs',
        'endpoints': {
            'health': '/health',
            'stats': '/stats',
            'classification': '/classification',
            'batch_classification': '/batch/classification',
            'capcode': '/capcode',
            'slideComparison': '/slideComparison',
            'detection': '/detection',
            'calculate': '/calculate',
            'crop': '/crop',
            'select': '/select'
        }
    })

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    健康检查端点
    ---
    responses:
      200:
        description: 服务健康状态
    """
    # 不记录健康检查日志，避免刷屏
    log.setLevel(logging.ERROR)
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'CAPTCHA Recognition API'
    })

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    获取API统计信息
    ---
    responses:
      200:
        description: API使用统计
    """
    return jsonify(get_stats_data())
