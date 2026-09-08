from flask import Flask, jsonify
import sqlite3, os
app = Flask(__name__, static_folder='dist', static_url_path='')
DB = 'data/crhq.db'
@app.before_request
def init_db():
    if not os.path.exists('data'): os.makedirs('data')
    conn = sqlite3.connect(DB); conn.execute('CREATE TABLE IF NOT EXISTS games (id TEXT PRIMARY KEY, name TEXT, short TEXT)'); conn.execute('CREATE TABLE IF NOT EXISTS updates (id INTEGER PRIMARY KEY, game TEXT, title TEXT, status TEXT, date TEXT)'); conn.commit(); conn.close()
@app.route('/api/health')
def health(): return jsonify({'success':True,'status':'ok','offline':True})
@app.route('/api/games')
def games(): return jsonify({'success':True,'data':[]})
@app.route('/api/updates')
def updates(): return jsonify({'success':True,'data':[]})
if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=False)
