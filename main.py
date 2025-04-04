from flask import Flask, request, render_template_string
import pyodbc # type: ignore

app = Flask(__name__)

# 🔹 Konfigurasi Koneksi ke Database (Sudah diperbarui)
DB_CONFIG = {
    'DRIVER': '{ODBC Driver 18 for SQL Server}',
    'SERVER': 'tcp:praktik2db.database.windows.net,1433',
    'DATABASE': 'praktik2db',
    'USERNAME': 'Aliyah',
    'PASSWORD': 'your_password_here',  # Ganti dengan password asli
    'ENCRYPT': 'yes',
    'TRUST_SERVER_CERTIFICATE': 'no',
    'TIMEOUT': 30
}

# 🔹 Fungsi untuk Membuka Koneksi Database
def get_db_connection():
    try:
        conn_str = (
            f"DRIVER={DB_CONFIG['DRIVER']};"
            f"SERVER={DB_CONFIG['SERVER']};"
            f"DATABASE={DB_CONFIG['DATABASE']};"
            f"UID={DB_CONFIG['USERNAME']};"
            f"PWD={DB_CONFIG['PASSWORD']};"
            f"Encrypt={DB_CONFIG['ENCRYPT']};"
            f"TrustServerCertificate={DB_CONFIG['TRUST_SERVER_CERTIFICATE']};"
            f"Connection Timeout={DB_CONFIG['TIMEOUT']};"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# 🔹 Halaman Home
@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Hello Page</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="text-center">
            <h1 class="display-4 mb-4">Hello, World! 🌍</h1>
            <a href="/form" class="btn btn-lg btn-success">Isi Form Sekarang</a>
            <a href="/users" class="btn btn-lg btn-primary">Lihat Data</a>
        </div>
    </body>
    </html>
    '''

# 🔹 Halaman Form Input
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # 🔹 Simpan Data ke Database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
            except Exception as e:
                print(f"Error saat menyimpan ke database: {e}")
            finally:
                cursor.close()
                conn.close()

        return f"<h2>Halo {name}!</h2><p>Email Anda <strong>{email}</strong> telah diterima 🎉</p><a href='/'>Kembali</a>"
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Form Input</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="card p-4 shadow" style="width: 24rem;">
            <h4 class="mb-4 text-center">Input Form</h4>
            <form method="post">
                <div class="mb-3">
                    <label class="form-label">Nama:</label>
                    <input type="text" name="name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Email:</label>
                    <input type="email" name="email" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

# 🔹 Halaman untuk Menampilkan Data Users
@app.route("/users")
def show_users():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        user_list = "<h2>Daftar Users</h2><ul>"
        for user in users:
            user_list += f"<li>ID: {user[0]}, Nama: {user[1]}, Email: {user[2]}</li>"
        user_list += "</ul><a href='/'>Kembali</a>"
        return user_list
    return "Gagal mengambil data dari database"

# 🔹 Jalankan Aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
