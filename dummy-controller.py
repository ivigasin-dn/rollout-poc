#!/usr/bin/env python3
"""
Dummy Controller for Config Rollout
Receives webhook calls and simulates sending configurations to devices
"""

import json
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigController(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "service": "config-controller"}
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Simulate metrics collection
            metrics = {
                "cpu_usage": random.uniform(10, 80),
                "memory_usage": random.uniform(20, 90),
                "response_time": random.uniform(100, 500),
                "error_rate": random.uniform(0, 5),
                "throughput": random.uniform(1000, 5000),
                "active_rollouts": random.randint(1, 10),
                "devices_configured": random.randint(50, 200)
            }
            self.wfile.write(json.dumps(metrics).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/validate':
            self.handle_validation()
        elif self.path == '/send-config':
            self.handle_send_config()
        elif self.path == '/rollout-status':
            self.handle_rollout_status()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_validation(self):
        """Validate configuration before rollout"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            logger.info(f"Validating config: {data.get('configVersion', 'unknown')}")
            
            # Simulate validation logic
            success = self.validate_config(data)
            
            if success:
                self.send_response(200)
                response = {
                    "status": "success", 
                    "message": "Configuration validation passed",
                    "configVersion": data.get('configVersion', 'unknown')
                }
            else:
                self.send_response(400)
                response = {
                    "status": "failure", 
                    "message": "Configuration validation failed",
                    "configVersion": data.get('configVersion', 'unknown')
                }
            
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def handle_send_config(self):
        """Send configuration to target devices"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            device_id = data.get('deviceId', 'unknown')
            config_data = data.get('config', {})
            
            logger.info(f"Sending config to device {device_id}: {config_data.get('name', 'unknown')}")
            
            # Simulate sending config to device
            success = self.send_config_to_device(device_id, config_data)
            
            if success:
                self.send_response(200)
                response = {
                    "status": "success",
                    "message": f"Configuration sent to device {device_id}",
                    "deviceId": device_id,
                    "configName": config_data.get('name', 'unknown')
                }
            else:
                self.send_response(500)
                response = {
                    "status": "failure",
                    "message": f"Failed to send config to device {device_id}",
                    "deviceId": device_id
                }
            
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Send config error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def handle_rollout_status(self):
        """Get rollout status"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            rollout_id = data.get('rolloutId', 'unknown')
            
            # Simulate rollout status
            status = self.get_rollout_status(rollout_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
            
        except Exception as e:
            logger.error(f"Status error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def validate_config(self, data):
        """Simulate configuration validation"""
        time.sleep(1)  # Simulate processing time
        
        # Simple validation logic
        config_version = data.get('configVersion', '')
        if not config_version or len(config_version) < 3:
            return False
            
        # Randomly pass/fail for demo purposes (90% success rate)
        return random.random() < 0.9
    
    def send_config_to_device(self, device_id, config_data):
        """Simulate sending configuration to a device"""
        time.sleep(2)  # Simulate network delay
        
        # Simulate device response (95% success rate)
        success = random.random() < 0.95
        
        if success:
            logger.info(f"✅ Config successfully applied to device {device_id}")
        else:
            logger.error(f"❌ Failed to apply config to device {device_id}")
            
        return success
    
    def get_rollout_status(self, rollout_id):
        """Simulate getting rollout status"""
        return {
            "rolloutId": rollout_id,
            "phase": random.choice(["Progressing", "Completed", "Paused"]),
            "currentStep": random.randint(1, 3),
            "totalSteps": 3,
            "completedDevices": random.randint(1, 10),
            "totalDevices": 10,
            "message": f"Rollout {rollout_id} is progressing"
        }
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server():
    """Start the webhook server"""
    server = HTTPServer(('0.0.0.0', 8080), ConfigController)
    logger.info("🚀 Config Controller running on port 8080")
    logger.info("📡 Available endpoints:")
    logger.info("   GET  /health - Health check")
    logger.info("   GET  /metrics - System metrics")
    logger.info("   POST /validate - Validate configuration")
    logger.info("   POST /send-config - Send config to device")
    logger.info("   POST /rollout-status - Get rollout status")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
