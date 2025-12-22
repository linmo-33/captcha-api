"""API 认证中间件"""
from functools import wraps
from flask import request, jsonify, current_app

def require_api_key(f):
    """API Key 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从 Flask config 获取 API Keys
        api_keys_str = current_app.config.get('API_KEYS', '')
        api_keys = [key.strip() for key in api_keys_str.split(',') if key.strip()]
        
        # 如果没有配置 API_KEYS，则不启用认证
        if not api_keys:
            return f(*args, **kwargs)
        
        # 从请求头获取 API Key
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'Missing API Key',
                'message': 'Please provide API Key in X-API-Key header or api_key parameter'
            }), 401
        
        if api_key not in api_keys:
            return jsonify({
                'error': 'Invalid API Key',
                'message': 'The provided API Key is not valid'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
