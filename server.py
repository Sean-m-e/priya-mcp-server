#!/usr/bin/env python3
"""
PRIYA MCP Server - Production Version for Railway
Serves MCP JSON modules via HTTP API for PRIYA voice agent
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configuration - Railway provides PORT via environment variable
MODULES_DIR = os.path.join(os.path.dirname(__file__), 'modules')
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
PORT = int(os.environ.get('PORT', 8080))  # Railway sets this
HOST = '0.0.0.0'  # Listen on all interfaces for Railway

# Setup logging
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'mcp_server.log')),
        logging.StreamHandler()
    ]
)

# Module cache for performance
module_cache = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'modules_available': len(os.listdir(MODULES_DIR)) if os.path.exists(MODULES_DIR) else 0,
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'unknown'),
        'version': '1.0.0'
    })

@app.route('/modules', methods=['GET'])
def list_modules():
    """List all available modules"""
    try:
        if not os.path.exists(MODULES_DIR):
            return jsonify({'error': 'Modules directory not found'}), 404
        
        modules = [f for f in os.listdir(MODULES_DIR) if f.endswith('.json')]
        modules.sort()  # Sort alphabetically
        
        return jsonify({
            'modules': modules,
            'count': len(modules),
            'expected': 14
        })
    except Exception as e:
        logging.error(f"Error listing modules: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/module/<module_name>', methods=['GET'])
def get_module(module_name):
    """Get a specific module by name"""
    try:
        # Add .json extension if not present
        if not module_name.endswith('.json'):
            module_name = f"{module_name}.json"
        
        module_path = os.path.join(MODULES_DIR, module_name)
        
        # Security: Prevent directory traversal
        if not os.path.abspath(module_path).startswith(os.path.abspath(MODULES_DIR)):
            logging.warning(f"Directory traversal attempt: {module_name}")
            return jsonify({'error': 'Invalid module name'}), 400
        
        if not os.path.exists(module_path):
            logging.warning(f"Module not found: {module_name}")
            return jsonify({'error': f'Module not found: {module_name}'}), 404
        
        # Check cache first
        if module_name in module_cache:
            logging.info(f"Serving module from cache: {module_name}")
            return jsonify(module_cache[module_name])
        
        # Load module
        with open(module_path, 'r', encoding='utf-8') as f:
            module_data = json.load(f)
        
        # Cache it
        module_cache[module_name] = module_data
        
        logging.info(f"Serving module: {module_name} (size: {len(str(module_data))} bytes)")
        return jsonify(module_data)
        
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in module {module_name}: {e}")
        return jsonify({'error': 'Invalid JSON in module'}), 500
    except Exception as e:
        logging.error(f"Error serving module {module_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/module/<module_name>/content', methods=['GET'])
def get_module_content(module_name):
    """Get just the 'content' field from a module (for R-modules)"""
    try:
        if not module_name.endswith('.json'):
            module_name = f"{module_name}.json"
        
        module_path = os.path.join(MODULES_DIR, module_name)
        
        if not os.path.exists(module_path):
            return jsonify({'error': f'Module not found: {module_name}'}), 404
        
        with open(module_path, 'r', encoding='utf-8') as f:
            module_data = json.load(f)
        
        if 'content' in module_data:
            return jsonify({'content': module_data['content']})
        else:
            return jsonify({'error': 'Module does not have a content field'}), 400
            
    except Exception as e:
        logging.error(f"Error serving module content {module_name}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/reload', methods=['POST'])
def reload_cache():
    """Clear module cache (forces reload from disk)"""
    try:
        module_cache.clear()
        logging.info("Module cache cleared")
        return jsonify({
            'status': 'success', 
            'message': 'Cache cleared',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'name': 'PRIYA MCP Server',
        'version': '1.0.0',
        'description': 'MCP server for PRIYA voice agent - serves JSON modules',
        'endpoints': {
            'GET /': 'API documentation (this page)',
            'GET /health': 'Health check',
            'GET /modules': 'List all modules',
            'GET /module/<name>': 'Get specific module',
            'GET /module/<name>/content': 'Get module content field only',
            'POST /reload': 'Clear cache and reload modules'
        },
        'modules_directory': MODULES_DIR,
        'modules_loaded': len(module_cache),
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'unknown')
    })

@app.errorhandler(404)
def not_found(e):
    """Custom 404 handler"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': ['/', '/health', '/modules', '/module/<name>']
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Custom 500 handler"""
    logging.error(f"Internal server error: {e}")
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500

if __name__ == '__main__':
    # Ensure modules directory exists
    os.makedirs(MODULES_DIR, exist_ok=True)
    
    logging.info("=" * 80)
    logging.info("PRIYA MCP SERVER - STARTING (PRODUCTION MODE)")
    logging.info("=" * 80)
    logging.info(f"Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'local')}")
    logging.info(f"Host: {HOST}")
    logging.info(f"Port: {PORT}")
    logging.info(f"Modules directory: {MODULES_DIR}")
    
    # Check for modules
    if os.path.exists(MODULES_DIR):
        module_count = len([f for f in os.listdir(MODULES_DIR) if f.endswith('.json')])
        logging.info(f"Found {module_count} modules")
        
        if module_count == 0:
            logging.warning("⚠️  WARNING: No modules found!")
        elif module_count < 14:
            logging.warning(f"⚠️  WARNING: Expected 14 modules, found {module_count}")
        else:
            logging.info("✅ All 14 modules loaded successfully")
    else:
        logging.warning("⚠️  Modules directory not found! Creating it...")
        os.makedirs(MODULES_DIR, exist_ok=True)
    
    logging.info("=" * 80)
    logging.info(f"Server ready at http://{HOST}:{PORT}")
    logging.info("=" * 80)
    
    # Run the app
    app.run(host=HOST, port=PORT, debug=False)
