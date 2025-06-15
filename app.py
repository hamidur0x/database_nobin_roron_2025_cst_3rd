from flask import Flask, render_template, request, redirect, session, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import csv
import os
import io

app = Flask(__name__)
app.secret_key = b'_5#y2L"shohan10_F4Q8z\n\xec]/'  # Hardcoded secret key
FILENAME = 'students.csv'

# Security configuration
ADMIN_PASSWORD_HASH = 'shohan10'  # Insecure! Only for demonstration purposes

def load_data():
    try:
        with open(FILENAME, 'r') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def save_data(data):
    with open(FILENAME, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['Serial', 'Name', 'Roll', 'Amount'])
        writer.writeheader()
        writer.writerows(data)

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect('/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD_HASH:
            session['is_admin'] = True
            return redirect('/')
        return "Invalid password", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect('/')

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html',
                         students=data,
                         is_admin=session.get('is_admin'))

@app.route('/add', methods=['POST'])
@admin_required
def add():
    name = request.form['name']
    roll = request.form['roll']
    amount = request.form['amount']

    data = load_data()
    if any(item['Roll'] == roll for item in data):
        return "Roll number exists!", 400

    data.append({
        'Serial': str(len(data)+1),
        'Name': name,
        'Roll': roll,
        'Amount': amount
    })
    save_data(data)
    return redirect('/')

@app.route('/delete/<roll>')
@admin_required
def delete(roll):
    data = load_data()
    new_data = [item for item in data if item['Roll'] != roll]
    save_data(new_data)
    return redirect('/')

@app.route('/pdf')
def generate_pdf():
    data = load_data()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("CST 3rd Finance Database", styles['Title']))

    pdf_data = [['ID', 'Name', 'Roll', 'Amount']]
    for item in data:
        pdf_data.append([item['Serial'], item['Name'], item['Roll'], item['Amount']])

    table = Table(pdf_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F5F5')),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, download_name="students.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)




















