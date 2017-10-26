# -*- coding:utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename
from addW import addW

ALLOWED_PIC_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_DOC_EXTENSIONS = set(['docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Word契约生成</h1>
    <p>一、先在这上传你的印迹</p>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    <p>二、再在这上传你的Word</p>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file1>
         <input type=submit value=上传>
    </form>
    '''

def allowed_pic_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_PIC_EXTENSIONS

def allowed_doc_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_DOC_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file1 = request.files['file1']
            if file1 and allowed_doc_file(file1.filename):
                filename = secure_filename(file1.filename)
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_url = url_for('uploaded_file', filename=filename)
                file_url2 = url_for('uploaded_file', filename=filename.split('.')[0]+'.png')
                if file_url and file_url2:
                    addW(filename, filename.split('.')[0]+'.png')
                    file_url2 = url_for('uploaded_file', filename='new'+filename.split('.')[0]+'.docx')
                    return html+'<a href='+file_url2+'>获取契约之书</a>'
                 
        except:
            file = request.files['file']
            if file and allowed_pic_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_url = url_for('uploaded_file', filename=filename)
                return html + '<br><img src=' + file_url + '>'
        
    return html + '<br><img src=' + '/uploads/wsyzkadqb.png' + '>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
