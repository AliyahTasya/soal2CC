from flask import Flask, request, render_template_string
import pyodbc  # type: ignore

app = Flask(__name__)

# 🔹 Konfigurasi Koneksi ke Database
DB_CONFIG = {
    'DRIVER': '{ODBC Driver 18 for SQL Server}',
    'SERVER': 'tcp:praktik2db.database.windows.net,1433',
    'DATABASE': 'praktik2db',
    'USERNAME': 'Aliyah',
    'PASSWORD': 'AzureSQL_1234',  
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
        print("✅ Database connection successful!")
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
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
            <a href="/form" class="btn btn-lg btn-success me-2">Isi Form Sekarang</a>
            <a href="/data" class="btn btn-lg btn-primary">Lihat Data</a>
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

        print(f"📩 Received input - Name: {name}, Email: {email}")

        # 🔹 Simpan Data ke Database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
                print("✅ Database commit successful!")

                # 🔹 Validasi apakah data benar-benar masuk
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                row = cursor.fetchone()
                if row:
                    print("✅ Data successfully inserted:", row)
                else:
                    print("❌ Data not found after insert!")

            except Exception as e:
                print(f"❌ Error saat menyimpan ke database: {e}")
            finally:
                cursor.close()
                conn.close()

        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Result</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="bg-light d-flex justify-content-center align-items-center" style="height: 100vh;">
                <div class="text-center">
                    <h2 class="mb-3">Halo {{ name }}!</h2>
                    <p>Email Anda <strong>{{ email }}</strong> telah diterima 🎉</p>
                    <a href="/" class="btn btn-secondary mt-3">Kembali ke Home</a>
                </div>
            </body>
            </html>
        ''', name=name, email=email)

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

# 🔹 Halaman untuk Melihat Data dari Database
@app.route("/data")
def view_data():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, email FROM users")
            rows = cursor.fetchall()
        except Exception as e:
            return f"<h3>❌ Gagal mengambil data: {e}</h3>"
        finally:
            cursor.close()
            conn.close()
        
        # Render data dengan HTML tabel
        table_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Data Pengguna</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light p-4">
            <div class="container">
                <h2 class="mb-4">📄 Data Pengguna</h2>
                <table class="table table-bordered table-striped">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Nama</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
        '''

        for row in rows:
            table_html += f"<tr><td>{row.id}</td><td>{row.name}</td><td>{row.email}</td></tr>"

        table_html += '''
                    </tbody>
                </table>
                <a href="/" class="btn btn-secondary mt-3">Kembali ke Home</a>
            </div>
        </body>
        </html>
        '''

        return table_html

    return "<h3>❌ Tidak dapat terhubung ke database!</h3>"

# 🔹 Jalankan Aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
