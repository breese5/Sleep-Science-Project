"""
Monitoring and logging dashboard endpoints.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.database.connection import db_manager

router = APIRouter()
logger = get_logger(__name__)


class SystemMetrics(BaseModel):
    """System metrics model."""
    uptime_seconds: float
    total_requests: int
    active_users: int
    database_connections: int
    memory_usage_mb: float
    cpu_usage_percent: float
    last_updated: datetime


class LogEntry(BaseModel):
    """Log entry model."""
    timestamp: datetime
    level: str
    message: str
    module: str
    function: str
    line_number: int


@router.get("/monitoring/dashboard", response_class=HTMLResponse)
async def monitoring_dashboard():
    """Simple HTML dashboard for monitoring."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sleep Science Bot - Monitoring Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
            .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .metric-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .metric-value { font-size: 2em; font-weight: bold; color: #667eea; }
            .metric-label { color: #666; margin-top: 5px; }
            .section { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .log-entry { padding: 10px; border-bottom: 1px solid #eee; }
            .log-error { background-color: #ffebee; }
            .log-warning { background-color: #fff3e0; }
            .log-info { background-color: #e3f2fd; }
            .refresh-btn { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-bottom: 20px; }
            .refresh-btn:hover { background: #5a6fd8; }
        </style>
        <script>
            function refreshData() {
                location.reload();
            }
            
            function autoRefresh() {
                setTimeout(refreshData, 30000); // Refresh every 30 seconds
            }
            
            // Auto-refresh on page load
            window.onload = function() {
                autoRefresh();
            };
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌙 Sleep Science Bot - Monitoring Dashboard</h1>
                <p>Real-time system monitoring and analytics</p>
            </div>
            
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value" id="uptime">--</div>
                    <div class="metric-label">System Uptime</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="requests">--</div>
                    <div class="metric-label">Total Requests</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="users">--</div>
                    <div class="metric-label">Active Users</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="interactions">--</div>
                    <div class="metric-label">Total Interactions</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Recent Analytics</h2>
                <div id="analytics-data">Loading...</div>
            </div>
            
            <div class="section">
                <h2>📝 Recent Logs</h2>
                <div id="logs-data">Loading...</div>
            </div>
        </div>
        
        <script>
            // Fetch and display metrics
            fetch('/api/v1/monitoring/metrics')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('uptime').textContent = Math.floor(data.uptime_seconds / 3600) + 'h ' + Math.floor((data.uptime_seconds % 3600) / 60) + 'm';
                    document.getElementById('requests').textContent = data.total_requests.toLocaleString();
                    document.getElementById('users').textContent = data.active_users;
                    document.getElementById('interactions').textContent = data.total_interactions || '--';
                })
                .catch(error => {
                    console.error('Error fetching metrics:', error);
                });
            
            // Fetch and display analytics
            fetch('/api/v1/analytics/overview?days=1')
                .then(response => response.json())
                .then(data => {
                    const analyticsHtml = `
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                            <div><strong>Total Interactions:</strong> ${data.total_interactions}</div>
                            <div><strong>Unique Users:</strong> ${data.unique_users}</div>
                            <div><strong>Avg Message Length:</strong> ${data.avg_message_length || 'N/A'}</div>
                            <div><strong>Popular Topics:</strong> ${data.popular_topics ? data.popular_topics.slice(0, 3).join(', ') : 'N/A'}</div>
                        </div>
                    `;
                    document.getElementById('analytics-data').innerHTML = analyticsHtml;
                })
                .catch(error => {
                    document.getElementById('analytics-data').innerHTML = '<p style="color: #666;">Analytics data unavailable</p>';
                });
            
            // Fetch and display logs
            fetch('/api/v1/monitoring/logs?limit=10')
                .then(response => response.json())
                .then(data => {
                    const logsHtml = data.logs.map(log => `
                        <div class="log-entry log-${log.level.toLowerCase()}">
                            <strong>${new Date(log.timestamp).toLocaleString()}</strong> [${log.level}] 
                            ${log.message} <em>(${log.module}:${log.line_number})</em>
                        </div>
                    `).join('');
                    document.getElementById('logs-data').innerHTML = logsHtml || '<p>No recent logs</p>';
                })
                .catch(error => {
                    document.getElementById('logs-data').innerHTML = '<p style="color: #666;">Logs unavailable</p>';
                });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/monitoring/metrics", response_model=SystemMetrics)
async def get_system_metrics():
    """Get current system metrics."""
    try:
        # Get database session to check connectivity
        db_session = db_manager.get_session()
        
        # Get basic metrics
        total_requests = 0  # Would need to implement request counting
        active_users = 0
        total_interactions = 0
        
        try:
            # Count users
            user_count = db_session.execute("SELECT COUNT(*) FROM users").scalar()
            active_users = user_count or 0
            
            # Count interactions
            interaction_count = db_session.execute("SELECT COUNT(*) FROM interactions").scalar()
            total_interactions = interaction_count or 0
            
        except Exception as e:
            logger.warning(f"Could not fetch database metrics: {e}")
        
        # Simulate uptime (in production, this would be tracked from app start)
        uptime_seconds = 3600  # 1 hour for demo
        
        # Simulate system metrics
        memory_usage_mb = 128.5
        cpu_usage_percent = 15.2
        database_connections = 5
        
        return SystemMetrics(
            uptime_seconds=uptime_seconds,
            total_requests=total_requests,
            active_users=active_users,
            database_connections=database_connections,
            memory_usage_mb=memory_usage_mb,
            cpu_usage_percent=cpu_usage_percent,
            last_updated=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system metrics")


@router.get("/monitoring/logs")
async def get_recent_logs(limit: int = Query(10, ge=1, le=100)):
    """Get recent application logs."""
    try:
        # In a real implementation, this would read from log files
        # For demo purposes, we'll return some sample logs
        sample_logs = [
            {
                "timestamp": datetime.now(timezone.utc) - timedelta(minutes=5),
                "level": "INFO",
                "message": "Application started successfully",
                "module": "app",
                "function": "create_app",
                "line_number": 45
            },
            {
                "timestamp": datetime.now(timezone.utc) - timedelta(minutes=3),
                "level": "INFO",
                "message": "Database connection established",
                "module": "database.connection",
                "function": "create_tables",
                "line_number": 23
            },
            {
                "timestamp": datetime.now(timezone.utc) - timedelta(minutes=1),
                "level": "INFO",
                "message": "Health check endpoint accessed",
                "module": "api.routes.health",
                "function": "health_check",
                "line_number": 35
            }
        ]
        
        return {"logs": sample_logs[:limit]}
        
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to get logs") 