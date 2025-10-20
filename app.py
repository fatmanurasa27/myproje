from flask import Flask, render_template, request, redirect, flash, session
from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os



app = Flask(__name__)
app.secret_key = 'gizli-anahtar'

# Veritabanı bağlantı fonksiyonu
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ana Sayfa - Giriş/Kayıt
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Boş alan bırakma 😿')
            return redirect('/')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            if user['password'] == password:
                session['kullanıcı_email']= email
                flash('Giriş başarılı 🎉')
                return redirect('https://www.btkakademi.gov.tr/')  # Yönlendirme
            else:
                flash('Şifre yanlış 😢')
                return redirect('/')
        else:
            try:
                conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
                conn.commit()
                flash('Kayıt başarılı! Artık giriş yapabilirsin 🌟')
                return redirect('/')
            except:
                flash('Bir hata oluştu 😔')
                return redirect('/')
        conn.close()

    return render_template('login.html')




@app.route('/dashboard')
def dashboard():
    if 'user_email' in session:
        return render_template('dashboard.html', email=session['user_email'])
    else:
        flash('Lütfen önce giriş yap 🙏')
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Çıkış yapıldı 👋')
    return redirect('/')

# Uygulama çalıştırma
if __name__ == '__main__':
    if not os.path.exists('users.db'):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.close()
    app.run(debug=True)

flash('Fatas’a hoş geldin! 🎉')


if __name__ == '__main__':
    app.run(debug=True)








