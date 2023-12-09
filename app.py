from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)
def create_table():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()
# メッセージ一覧表示
@app.route('/')
def index():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY id DESC')
    messages = c.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

# 新規メッセージの作成
@app.route('/create', methods=['POST'])
def create():
    content = request.form['content']
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# メッセージの編集
@app.route('/edit/<int:message_id>', methods=['GET', 'POST'])
def edit(message_id):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    if request.method == 'GET':
        c.execute('SELECT * FROM messages WHERE id = ?', (message_id,))
        message = c.fetchone()
        conn.close()
        return render_template('edit.html', message=message)
    else:
        content = request.form['content']
        c.execute('UPDATE messages SET content = ? WHERE id = ?', (content, message_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

# メッセージの削除
@app.route('/delete/<int:message_id>', methods=['POST'])
def delete(message_id):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)
