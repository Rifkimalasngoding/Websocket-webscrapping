"""
APLIKASI WEB SCRAPING + WEBSOCKET DENGAN FLASK
==============================================
Aplikasi ini menggabungkan:
1. Web Scraping - Mengambil data dari website
2. WebSocket (Socket.IO) - Komunikasi real-time
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
from scraper import scrape_quotes, scrape_news

# Inisialisasi Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia-12345'

# Inisialisasi SocketIO dengan Flask
# async_mode='threading' untuk mendukung background task
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

# ============================================================
# VARIABEL GLOBAL
# ============================================================
scraping_active = False
scraping_thread = None

# ============================================================
# ROUTE HALAMAN UTAMA
# ============================================================
@app.route('/')
def index():
    """Halaman utama aplikasi"""
    return render_template('index.html')

# ============================================================
# FUNGSI SCRAPING BACKGROUND
# ============================================================
def background_scraping():
    """
    Fungsi yang berjalan di background thread
    Melakukan scraping setiap 5 detik dan kirim hasil via WebSocket
    """
    global scraped_data, scraping_active
    
    print("[Background] Memulai background scraping...")
    
    while scraping_active:
        try:
            # 1. Lakukan scraping dari website
            print("[Background] Melakukan scraping...")
            quotes = scrape_quotes()
            
            # 2. Jika ada data, kirim ke semua client via WebSocket
            if quotes:
                socketio.emit('scraping_update', {
                    'status': 'success',
                    'data': quotes,
                    'count': len(quotes),
                    'timestamp': time.strftime('%H:%M:%S')
                })
                print(f"[Background] Data terkirim: {len(quotes)} items")
            else:
                socketio.emit('scraping_update', {
                    'status': 'error',
                    'message': 'Gagal mengambil data'
                })
            
            # 3. Tunggu 5 detik sebelum scraping lagi
            time.sleep(5)
            
        except Exception as e:
            print(f"[Background] Error: {e}")
            socketio.emit('scraping_update', {
                'status': 'error',
                'message': str(e)
            })
            time.sleep(5)
    
    print("[Background] Background scraping dihentikan")

# ============================================================
# WEBSOCKET EVENT HANDLERS
# ============================================================

@socketio.on('connect')
def handle_connect():
    """Event ketika client terhubung"""
    print(f"[Socket] Client terhubung")
    emit('connected', {'message': 'Terhubung ke server!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Event ketika client terputus"""
    print(f"[Socket] Client terputus")

@socketio.on('start_scraping')
def handle_start_scraping():
    """Event untuk memulai background scraping"""
    global scraping_active, scraping_thread
    
    print("[Socket] Menerima perintah START scraping")
    
    if not scraping_active:
        scraping_active = True
        scraping_thread = threading.Thread(target=background_scraping)
        scraping_thread.daemon = True
        scraping_thread.start()
        emit('scraping_status', {'active': True, 'message': 'Scraping dimulai'})
    else:
        emit('scraping_status', {'active': True, 'message': 'Scraping sudah berjalan'})

@socketio.on('stop_scraping')
def handle_stop_scraping():
    """Event untuk menghentikan background scraping"""
    global scraping_active
    
    print("[Socket] Menerima perintah STOP scraping")
    scraping_active = False
    emit('scraping_status', {'active': False, 'message': 'Scraping dihentikan'})

@socketio.on('scrape_once')
def handle_scrape_once():
    """Event untuk scraping satu kali (manual)"""
    print("[Socket] Menerima perintah scrape sekali")
    
    try:
        quotes = scrape_quotes()
        if quotes:
            emit('scraping_result', {
                'status': 'success',
                'data': quotes,
                'count': len(quotes)
            })
        else:
            emit('scraping_result', {
                'status': 'error',
                'message': 'Gagal mengambil data'
            })
    except Exception as e:
        emit('scraping_result', {
            'status': 'error',
            'message': str(e)
        })

# ============================================================
# MENJALANKAN APLIKASI
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 APLIKASI WEB SCRAPING + WEBSOCKET")
    print("=" * 60)
    print("📍 Akses di browser: http://localhost:5000")
    print("📡 WebSocket siap menerima koneksi")
    print("🔄 Scraping dapat berjalan otomatis setiap 5 detik")
    print("=" * 60)
    
    # Jalankan dengan SocketIO
    socketio.run(app, debug=True, host='localhost', port=5000)