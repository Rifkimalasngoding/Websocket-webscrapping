"""
MODUL WEB SCRAPER
=================
Berisi fungsi-fungsi untuk scraping data dari website
"""

import requests
from bs4 import BeautifulSoup
import random

def scrape_quotes():
    """
    Scraping quotes dari http://quotes.toscrape.com/
    Website ini khusus dibuat untuk latihan scraping
    """
    url = "http://quotes.toscrape.com/"
    
    try:
        # 1. Kirim HTTP request ke website
        response = requests.get(url, timeout=10)
        
        # 2. Cek apakah request berhasil
        if response.status_code != 200:
            print(f"[Scraper] Gagal akses website. Status: {response.status_code}")
            return None
        
        # 3. Parse HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Cari semua elemen quote
        quote_elements = soup.find_all('div', class_='quote')
        
        # 5. Ekstrak data dari setiap quote
        quotes = []
        for quote in quote_elements[:5]:  # Ambil 5 quote pertama
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
        
        print(f"[Scraper] Berhasil scrape {len(quotes)} quotes")
        return quotes
        
    except requests.exceptions.Timeout:
        print("[Scraper] Timeout - Website terlalu lama merespon")
        return None
    except requests.exceptions.ConnectionError:
        print("[Scraper] Connection Error - Tidak bisa konek ke website")
        return None
    except Exception as e:
        print(f"[Scraper] Error: {e}")
        return None

def scrape_news():
    """
    Contoh scraping berita dari website (untuk variasi)
    Bisa dikembangkan sesuai kebutuhan
    """
    # Ini contoh dummy data jika website tidak bisa diakses
    dummy_news = [
        {
            'title': 'Belajar Web Scraping dengan Python',
            'source': 'Tech Blog',
            'url': '#'
        },
        {
            'title': 'Membuat Aplikasi Real-time dengan WebSocket',
            'source': 'Dev Community',
            'url': '#'
        },
        {
            'title': 'Flask vs Django: Mana yang Harus Dipilih?',
            'source': 'Python Weekly',
            'url': '#'
        }
    ]
    
    # Pilih random 1-3 berita
    return random.sample(dummy_news, random.randint(1, 3))