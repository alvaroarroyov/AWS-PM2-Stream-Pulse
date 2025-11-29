from flask import Flask, render_template_string, jsonify
import sqlite3
import os

app = Flask(__name__)

# --- FRONTEND (HTML + JS) ---
# In a larger project, this would be in a /templates folder.
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Stream Pulse Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #121212; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; }
        .container { width: 90%; max-width: 800px; margin: 0 auto; padding-top: 20px; }
        h1 { color: #00ff88; text-transform: uppercase; letter-spacing: 2px; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        
        /* List Styles */
        ul { list-style-type: none; padding: 0; text-align: left; }
        li { padding: 8px; border-bottom: 1px solid #333; animation: fadeIn 0.5s; }
        .user { font-weight: bold; color: #bb86fc; }
        .msg { color: #aaa; font-style: italic; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Stream Pulse Live Analytics</h1>
        
        <div class="card">
            <canvas id="pulseChart"></canvas>
        </div>

        <div class="card">
            <h3>📝 Live Incoming Feed</h3>
            <ul id="recentList">
                <li>Waiting for data...</li>
            </ul>
        </div>
    </div>

    <script>
        // CHART CONFIGURATION
        const ctx = document.getElementById('pulseChart').getContext('2d');
        const pulseChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // Will be filled with time stamps
                datasets: [{
                    label: 'Messages per Minute (Hype Level)',
                    data: [], // Will be filled with counts
                    borderColor: '#00ff88',
                    backgroundColor: 'rgba(0, 255, 136, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4 // Smooth curve
                }]
            },
            options: {
                scales: { 
                    y: { beginAtZero: true, grid: { color: '#333' } }, 
                    x: { grid: { display: false } } 
                }
            }
        });

        // FETCH DATA FROM FLASK API
        function updateData() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    // Update Chart
                    pulseChart.data.labels = data.times;
                    pulseChart.data.datasets[0].data = data.counts;
                    pulseChart.update();

                    // Update Recent List
                    const list = document.getElementById('recentList');
                    list.innerHTML = "";
                    data.recent.forEach(item => {
                        list.innerHTML += `<li><span class="user">${item.user}:</span> <span class="msg">${item.message}</span></li>`;
                    });
                });
        }

        // Auto-refresh every 3 seconds
        setInterval(updateData, 3000);
        updateData();
    </script>
</body>
</html>
"""

# --- BACKEND ROUTES ---

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/api/stats')
def api_stats():
    conn = sqlite3.connect('pulse.db')
    c = conn.cursor()
    
    # 1. Fetch last 5 messages for the list
    c.execute("SELECT username, message FROM chat_logs ORDER BY id DESC LIMIT 5")
    recent_rows = c.fetchall()
    recent_data = [{"user": r[0], "message": r[1]} for r in recent_rows]

    # 2. COMPLEX QUERY: Aggregate messages by minute (Last 15 mins)
    c.execute("""
        SELECT strftime('%H:%M', timestamp) as minute, COUNT(*) 
        FROM chat_logs 
        WHERE timestamp >= datetime('now', '-15 minutes')
        GROUP BY minute 
        ORDER BY minute ASC
    """)
    chart_rows = c.fetchall()
    conn.close()

    # Format for Chart.js
    times = [r[0] for r in chart_rows]
    counts = [r[1] for r in chart_rows]

    return jsonify({
        "recent": recent_data,
        "times": times,
        "counts": counts
    })

if __name__ == '__main__':
    # Host 0.0.0.0 allows external access (AWS Security Group must allow port 5000)
    app.run(host='0.0.0.0', port=5000)