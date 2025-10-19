import os
import math # 페이지 계산을 위해 math 라이브러리를 가져옵니다.
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
# flash 메시지 기능을 사용하기 위해 secret_key가 필요합니다.
app.secret_key = 'supersecretkey' # 아무 문자열이나 입력해도 됩니다.

# --- 사진 업로드 폴더 경로 설정 및 자동 생성 ---
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- 한 페이지에 보여줄 사진 개수 설정 ---
PHOTOS_PER_PAGE = 9

# 허용할 파일 확장자 설정
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 이름 입력 페이지
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['name']
        if user_name == '최연우' or user_name == '연우':
            return redirect(url_for('letter'))
        else:
            error_message = "앗, 이름이 틀렸어요! 다시 시도해 보세요. 😉"
            return render_template('index.html', error=error_message)
    return render_template('index.html')

# 편지 페이지
@app.route('/letter')
def letter():
    return render_template('letter.html')

# 앨범 페이지 (페이지 번호를 받을 수 있도록 수정)
@app.route('/album')
@app.route('/album/page/<int:page>')
def album(page=1):
    image_files = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True) # 최신순으로 정렬
    total_photos = len(image_files)
    total_pages = math.ceil(total_photos / PHOTOS_PER_PAGE)

    # 페이지에 맞는 사진만 잘라내기
    start_index = (page - 1) * PHOTOS_PER_PAGE
    end_index = start_index + PHOTOS_PER_PAGE
    photos_for_page = image_files[start_index:end_index]

    return render_template(
        'album.html',
        photos=photos_for_page,
        page=page,
        total_pages=total_pages
    )

# 사진 업로드 처리
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('album'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('album'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('album'))

# ✨ 사진 삭제 기능 ✨
@app.route('/delete/<filename>', methods=['POST'])
def delete_photo(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('album'))

if __name__ == '__main__':
    app.run(debug=True)