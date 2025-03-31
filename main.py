from flask import Flask, request, render_template_string # type: ignore

app = Flask(__name__)

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
        </div>
    </body>
    </html>
    '''

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
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

if __name__ == "__main__":
    app.run(debug=True)
