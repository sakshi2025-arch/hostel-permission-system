from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# 🟢 SESSION SECRET KEY
app.secret_key = "hostel123"


# 🟢 LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # 🔵 ADMIN LOGIN
        if username == "admin" and password == "admin123":
            session['user'] = "admin"
            return redirect(url_for('admin'))

        # 🔵 CHIEF LOGIN
        elif username == "chief" and password == "chief123":
            session['user'] = "chief"
            return redirect(url_for('chief'))

        else:
            return "Invalid Login ❌"

    return render_template('login.html')


# 🟢 HOME PAGE + SUBMIT REQUEST
@app.route('/', methods=['GET', 'POST'])
def home():

    message = ""

    if request.method == 'POST':

        conn = sqlite3.connect('hostel.db')
        cur = conn.cursor()

        # 🔴 DUPLICATE CHECK
        cur.execute(
            "SELECT * FROM requests WHERE student_no = ?",
            (request.form['student_no'],)
        )

        existing = cur.fetchone()

        if existing:
            conn.close()
            return "❌ You have already submitted request"

        # 🟢 INSERT DATA
        cur.execute("""
            INSERT INTO requests (
                student_name,
                branch,
                year,
                hostel_no,
                room_no,
                student_no,
                parent_no,
                outgoing_date,
                incoming_date,
                reason,
                emergency_level,
                emergency
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            request.form['student_name'],
            request.form['branch'],
            request.form.get('year'),
            request.form.get('hostel_no'),
            request.form.get('room_no'),
            request.form.get('student_no'),
            request.form.get('parent_no'),
            request.form.get('outgoing_date'),
            request.form.get('incoming_date'),
            request.form.get('reason'),
            request.form.get('emergency_level'),
            request.form.get('emergency')

        ))

        conn.commit()
        conn.close()

        message = "Request Submitted Successfully ✔"

    return render_template('index.html', message=message)


# 🟢 ADMIN PANEL
@app.route('/admin')
def admin():

    if session.get('user') != "admin":
        return redirect(url_for('login'))

    conn = sqlite3.connect('hostel.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    # 🟢 ALL DATA
    cur.execute("SELECT * FROM requests")
    data = cur.fetchall()

    # 🟢 COUNTERS
    cur.execute("SELECT COUNT(*) FROM requests")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Pending'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Approved'")
    approved = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Rejected'")
    rejected = cur.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        data=data,
        total=total,
        pending=pending,
        approved=approved,
        rejected=rejected
    )


# 🟢 CHIEF PANEL
@app.route('/chief')
def chief():

    if session.get('user') != "chief":
        return redirect(url_for('login'))

    status_filter = request.args.get('status')
    search = request.args.get('search')

    conn = sqlite3.connect('hostel.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    # 🟢 SEARCH + FILTER LOGIC
    if search and status_filter:

        cur.execute(
            "SELECT * FROM requests WHERE student_name LIKE ? AND status = ?",
            ('%' + search + '%', status_filter)
        )

    elif search:

        cur.execute(
            "SELECT * FROM requests WHERE student_name LIKE ?",
            ('%' + search + '%',)
        )

    elif status_filter:

        cur.execute(
            "SELECT * FROM requests WHERE status = ?",
            (status_filter,)
        )

    else:

        cur.execute("SELECT * FROM requests")

    data = cur.fetchall()

    # 🟢 COUNTERS
    cur.execute("SELECT COUNT(*) FROM requests")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Pending'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Approved'")
    approved = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Rejected'")
    rejected = cur.fetchone()[0]

    conn.close()

    return render_template(
        'chief.html',
        data=data,
        total=total,
        pending=pending,
        approved=approved,
        rejected=rejected
    )


# 🟢 APPROVE REQUEST
@app.route('/approve/<int:id>')
def approve(id):

    conn = sqlite3.connect('hostel.db')
    cur = conn.cursor()

    cur.execute(
        "UPDATE requests SET status='Approved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('chief'))


# 🟢 REJECT REQUEST
@app.route('/reject/<int:id>')
def reject(id):

    conn = sqlite3.connect('hostel.db')
    cur = conn.cursor()

    cur.execute(
        "UPDATE requests SET status='Rejected' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('chief'))


# 🟢 LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


# 🟢 RUN APP
if __name__ == '__main__':
    app.run(debug=True)