from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from datetime import datetime, timedelta
import pandas as pd
from LoanPredictor import LoanPredictor

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'loan_system'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

mysql = MySQL(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_role(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT role FROM users WHERE id = %s', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result['role'] if result else None



@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill out all fields!', 'danger')
            return render_template('login.html')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        cursor.close()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Incorrect username/password!', 'danger')
    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_applications,
            SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved_loans,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_approvals,
            SUM(CASE WHEN status = 'declined' THEN 1 ELSE 0 END) as declined_loans
        FROM loan_applications
    ''')
    stats = cursor.fetchone()
    
    cursor.execute('SELECT * FROM loan_applications ORDER BY created_at DESC LIMIT 5')
    recent_applications = cursor.fetchall()
    
    cursor.close()
    
    return render_template('dashboard.html', stats=stats, recent_applications=recent_applications)



@app.route('/loan_form', methods=['GET'])
def loanForm():
    return render_template('loan_form.html')




@app.route('/save_loan_form', methods=['POST'])
def saveloanform():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    else:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            form_data = {
                'loan_id': request.form.get('loanId'),
                'name': request.form.get('name'),
                'nic': request.form.get('applicantId'),
                'contact': request.form.get('contactInfo'),
                'no_of_dependents': int(request.form.get('dependents', 0)),
                'education': request.form.get('education'),
                'self_employed': request.form.get('selfEmployed'),
                'income_annum': float(request.form.get('annualIncome', 0)),
                'loan_amount': float(request.form.get('loanAmount', 0)),
                'loan_term': int(request.form.get('loanTerm', 0)),
                'purposes': request.form.get('purpose'),
                'cibil_score': int(request.form.get('cibilScore', 0)),
                'residential_assets_value': float(request.form.get('resAssets', 0)),
                'commercial_assets_value': float(request.form.get('comAssets', 0)),
                'luxury_assets_value': float(request.form.get('luxAssets', 0)),
                'bank_asset_value': float(request.form.get('bankAssets', 0)),
                'status': 'pending',
                'created_at': datetime.now()
}

            query = """
                INSERT INTO loan_applications 
                (loan_id, name, nic, contact, no_of_dependents, education, self_employed, income_annum, 
                loan_amount, loan_term, purposes, cibil_score, residential_assets_value, 
                commercial_assets_value, luxury_assets_value, bank_asset_value, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    
            values = (
                form_data['loan_id'], form_data['name'], form_data['nic'], form_data['contact'], 
                form_data['no_of_dependents'], form_data['education'], form_data['self_employed'], 
                form_data['income_annum'], form_data['loan_amount'], form_data['loan_term'], 
                form_data['purposes'], form_data['cibil_score'], 
                form_data['residential_assets_value'], form_data['commercial_assets_value'], 
                form_data['luxury_assets_value'], form_data['bank_asset_value'], 
                form_data['status'], form_data['created_at']
            )
    
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()

            flash('Loan application submitted successfully!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(f'Error submitting application: {str(e)}', 'danger')
        return render_template('loan_form.html')

    return render_template('loan_form.html')




@app.route('/applications')
def applications():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if session['role'] == 'admin':
        cursor.execute('SELECT * FROM loan_applications ORDER BY created_at DESC')
    else:
        cursor.execute('SELECT * FROM loan_applications WHERE user_id = %s ORDER BY created_at DESC', 
                      (session['id'],))
    
    applications = cursor.fetchall()
    cursor.close()
    
    return render_template('applications.html', applications=applications)




@app.route('/review/<int:application_id>', methods=['GET', 'POST'])
def review_application(application_id):
    if 'loggedin' not in session or session['role'] != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        status = request.form.get('status')
        remarks = request.form.get('remarks')
        
        cursor.execute('''
            UPDATE loan_applications 
            SET status = %s, remarks = %s, reviewed_by = %s, reviewed_at = NOW() 
            WHERE id = %s
        ''', (status, remarks, session['id'], application_id))
        
        mysql.connection.commit()
        flash('Application review completed!', 'success')
        return redirect(url_for('applications'))
    
    cursor.execute('SELECT * FROM loan_applications WHERE id = %s', (application_id,))
    application = cursor.fetchone()
    cursor.close()
    
    if not application:
        flash('Application not found!', 'danger')
        return redirect(url_for('applications'))
    
    return render_template('review.html', application=application)




@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if 'loggedin' not in session or session['role'] != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_user':
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')
            
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                         (username, password, role))
            mysql.connection.commit()
            flash('User added successfully!', 'success')
            
        elif action == 'update_user':
            user_id = request.form.get('user_id')
            role = request.form.get('role')
            
            cursor.execute('UPDATE users SET role = %s WHERE id = %s', (role, user_id))
            mysql.connection.commit()
            flash('User role updated!', 'success')
            
        elif action == 'delete_user':
            user_id = request.form.get('user_id')
            
            cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
            mysql.connection.commit()
            flash('User deleted!', 'success')
    
    cursor.execute('SELECT * FROM users ORDER BY username')
    users = cursor.fetchall()
    cursor.close()
    
    return render_template('admin_settings.html', users=users)




@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))



loan_predictor = LoanPredictor()
loan_predictor.train('loan_approval_dataset.csv')

@app.route('/review')
def review():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('''
            SELECT 
                l.*, 
                CASE 
                    WHEN l.status = 'approved' THEN 'success'
                    WHEN l.status = 'rejected' THEN 'danger'
                    ELSE 'warning'
                END as status_color
            FROM loan_applications l
            ORDER BY l.created_at DESC
        ''')
        
        loans = cursor.fetchall()
    except Exception as e:
        flash(f"Error fetching loan data: {str(e)}", 'danger')
        loans = []
    finally:
        cursor.close() 

    return render_template('review.html', loans=loans)


@app.route('/get_prediction/<int:loan_id>')
def get_prediction(loan_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM loan_applications WHERE loan_id = %s', (loan_id,))
        loan = cursor.fetchone()

        if not loan:
            return jsonify({"error": "Loan application not found"}), 404

        loan_data = {
            'loan_amount': loan['loan_amount'],
            'cibil_score': loan['cibil_score'],
            'loan_term': loan['loan_term'],
            'income_annum': loan['income_annum'],
            'no_of_dependents': loan['no_of_dependents'],
            'education': loan['education'],
            'self_employed': loan['self_employed'],
            'residential_assets_value': loan['residential_assets_value'],
            'commercial_assets_value': loan['commercial_assets_value'],
            'luxury_assets_value': loan['luxury_assets_value'],
            'bank_asset_value': loan['bank_asset_value']
        }

        prediction_result = loan_predictor.predict(loan_data)

        return jsonify({
            "prediction": prediction_result['prediction'], 
            "confidence": prediction_result['confidence'], 
            "features_importance": prediction_result['features_importance']
        })
    except ValueError as ve:

        return jsonify({"error": f"Error during prediction: {str(ve)}"}), 400
    except Exception as e:

        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        cursor.close()
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



# Careers page
@app.route('/careers', methods=['GET'])
def careers():
    return render_template('careers.html')

# Careers quick application handler
@app.route('/careers/apply', methods=['POST'])
def careers_apply():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    position = request.form.get('position')
    resume_file = request.files.get('resume')

    if not full_name or not email or not phone or not position or not resume_file:
        flash('Please complete all required fields.', 'danger')
        return redirect(url_for('careers'))

    if resume_file and allowed_file(resume_file.filename):
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{resume_file.filename}")
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(save_path)
        flash('Application submitted successfully! We\'ll be in touch soon.', 'success')
        return redirect(url_for('careers'))

    flash('Invalid resume format. Allowed: PDF, DOC, DOCX, JPG, JPEG, PNG.', 'danger')
    return redirect(url_for('careers'))

if __name__ == '__main__':
    app.run(debug=True)