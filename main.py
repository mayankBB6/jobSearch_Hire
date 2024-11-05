from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database with default jobs
def init_db():
    conn = get_db_connection()
    # Updated schema to include salary and location
    conn.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        salary TEXT,
                        location TEXT
                    )''')
    conn.commit()

    # Default jobs suitable for high school students
    default_jobs = [
        {
            'title': 'Retail Associate',
            'description': 'Assist customers, stock shelves, and organize displays in a retail setting.',
            'salary': '$15/hour',
            'location': 'Autozone'
        },
        {
            'title': 'Fast Food Crew Member',
            'description': 'Take customer orders, prepare food, and maintain cleanliness in a fast-food restaurant.',
            'salary': '$14/hour',
            'location': 'In-Person'
        },
        {
            'title': 'Lifeguard',
            'description': 'Ensure the safety of swimmers, enforce pool rules, and provide emergency response if needed.',
            'salary': '$13/hour',
            'location': 'In-Person'
        },
        {
            'title': 'Grocery Store Bagger',
            'description': 'Bag groceries, assist customers with loading, and return shopping carts.',
            'salary': '$12/hour',
            'location': 'In-Person'
        },
        {
            'title': 'Tutor',
            'description': 'Tutoring kids from grade 1-5 on basic mathematics and English.',
            'salary': '$15/hour',
            'location': 'Kumon'
        },
        {
            'title': 'Library Assistant',
            'description': 'Help organize books, assist patrons, and manage book check-outs at a local library.',
            'salary': '$11/hour',
            'location': 'Urbana Library'
        }
    ]

    # Add default jobs if the table is empty
    existing_jobs = conn.execute('SELECT * FROM jobs').fetchall()
    if not existing_jobs:  # Only insert defaults if the table is empty
        for job in default_jobs:
            conn.execute('INSERT INTO jobs (title, description, salary, location) VALUES (?, ?, ?, ?)',
                         (job['title'], job['description'], job['salary'], job['location']))
        conn.commit()

    conn.close()

# Route to display all jobs on the main page
@app.route('/')
def index():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()  # Fetch all jobs
    conn.close()
    return render_template('index.html', jobs=jobs)

# Route to add a job
@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        salary = request.form.get('salary', '')
        location = request.form.get('location', '')

        conn = get_db_connection()
        conn.execute('INSERT INTO jobs (title, description, salary, location) VALUES (?, ?, ?, ?)', 
                     (title, description, salary, location))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # Redirect to home page after adding a job

    # Display all jobs, including newly added and default ones
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return render_template('addJob.html', jobs=jobs)

# Route to search jobs
@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    search_term = request.form['search_term'].lower()
    filtered_jobs = [job for job in jobs if search_term in job['title'].lower()] # type: ignore
    return render_template('searchJob.html', jobs=filtered_jobs)

def apply(job_id):
    # Handle application logic here
    return f"Applying for job ID {job_id}"

if __name__ == '__main__':
    init_db()  # Initialize the database and add default jobs if necessary
    app.run(debug=True)
