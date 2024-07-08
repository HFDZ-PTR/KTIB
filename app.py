from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def get_semester_data(semester=None):
    if semester:
        semester_path = os.path.join(app.config['UPLOAD_FOLDER'], semester)
        mata_kuliah_list = os.listdir(semester_path) if os.path.exists(semester_path) else []
        semester_data = {semester: {}}
        for mata_kuliah in mata_kuliah_list:
            materi_files = os.listdir(os.path.join(semester_path, mata_kuliah))
            semester_data[semester][mata_kuliah] = materi_files
    else:
        semesters = os.listdir(app.config['UPLOAD_FOLDER'])
        semester_data = {}
        for semester in semesters:
            mata_kuliah_list = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], semester))
            semester_data[semester] = {}
            for mata_kuliah in mata_kuliah_list:
                materi_files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], semester, mata_kuliah))
                semester_data[semester][mata_kuliah] = materi_files
    return semester_data

@app.context_processor
def inject_semester_data():
    semester_data = get_semester_data()
    return dict(semester_data=semester_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/semester/<semester>')
def view_semester(semester):
    semester_data = get_semester_data(semester)
    return render_template('index.html', selected_semester=semester)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        semester = request.form['semester']
        mata_kuliah = request.form['mata_kuliah']
        
        if not semester or not mata_kuliah:
            return redirect(url_for('home'))
    
        if 'file' not in request.files:
            return redirect(url_for('home'))
        
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('home'))
        
        directory = os.path.join(app.config['UPLOAD_FOLDER'], semester, mata_kuliah)
        os.makedirs(directory, exist_ok=True)
        filename = file.filename
        file.save(os.path.join(directory, filename))
        
        return redirect(url_for('view_semester', semester=semester))
    
    return render_template('upload.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/semester/<semester>/course/<course>')
def view_course(semester, course):
    semester_data = get_semester_data(semester)
    course_files = semester_data.get(semester, {}).get(course, [])
    return render_template('course.html', semester=semester, course=course, course_files=course_files)

@app.route('/get_course_files/<semester>/<course>')
def get_course_files(semester, course):
    course_files_path = os.path.join(app.config['UPLOAD_FOLDER'], semester, course)
    course_files = os.listdir(course_files_path) if os.path.exists(course_files_path) else []
    return jsonify({"course_files": course_files})

if __name__ == '__main__':
    app.run(debug=True)
