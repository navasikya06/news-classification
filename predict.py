# Du bao
import numpy as np
from time import time
import pyodbc
from pyvi import ViTokenizer
import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer ,CountVectorizer
from sklearn.svm import LinearSVC

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=F:\\TTX_Tintulieu\\Ly\\temp.mdb;'
    )
cnxn = pyodbc.connect(conn_str)
cursor1 = cnxn.cursor()
cursor2 = cnxn.cursor()
cursor3 = cnxn.cursor()
p1 = re.compile(r'''\[kw\].*\[/kw\]|\[su\].*\[/su\]|\[id\].*\[/id\]|\[au\].*\[/au\]''')
p2 = re.compile(r'''\[ti\]|\[/ti\]|\[ca\]|\[/ca\]''')
punct = string.punctuation
punct = re.sub('_', '', punct)
cac_cd = ['Bổ túc VH-Xóa mù chữ', 'Đại học', 'Đại học-cao học-cao đẳng', 'Điển hình', 'Du học, lưu học sinh', 'Giáo dục phổ thông', 'Giáo viên', 'Kỳ thì chuyển cấp', 'Sở giáo dục', 'Thi-Tuyển sinh', 'Trung học chuyên nghiệp-d/nghề', 'Vấn đề chung Giáo dục', 'Công nghệ ( nói chung )', 'Đánh giá tổng quát', 'Điển hình', 'Khoa học ( nói chung )', 'Khoa học kỹ thuật-Công nghệ', 'Khoa học xã hội', 'Kinh tế chung', 'Môi trường']

# %% Clean noi_dung
def chuan_hoa(noi_dung):
    temp = noi_dung
    temp = re.sub(p1, ' ', temp)
    temp = re.sub(p2, ' ', temp)
    temp = ViTokenizer.tokenize(temp)
    for c in punct:
        c = '\\'+c
        temp = re.sub(c, ' ', temp)
        temp = temp.lower()
    return temp    

# %% Xay dung  model clf=LinearSVC(penalty="l2", dual=False,tol=1e-3)
def model():
    # % Doc data huan luyen: noi_ dung va chu_de => label
    print('Doc data huan luyen')
    noi_dung = []
    label = []
    cursor1.execute('select noi_dung, chu_de from temp')
    row1s = cursor1.fetchall()
    for row1 in row1s:
        cd = row1.chu_de
        cs = cac_cd.index(cd)
        label.append(cs)
        temp = chuan_hoa(row1.noi_dung)
        noi_dung.append(temp)
    print('vectorizer va clf')
    # % Vecto hoa noi_dung va xay dung model clf = LinearSVC(penalty="l2", dual=False,tol=1e-3)
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    X = vectorizer.fit_transform(noi_dung)
    y = label
    clf = LinearSVC(penalty="l2", dual=False,tol=1e-3)
    clf.fit(X, y)
    return vectorizer, clf

# %% Du bao
print('Bat dau xd model')
vectorizer, clf = model()
print('Ket thuc xay dung model')
cursor2.execute('select idx, noi_dung from temp where dau=1')
row2s = cursor2.fetchall()
for row2 in row2s:
    idx = row2.idx
    temp = chuan_hoa(row2.noi_dung)
    X_predict = vectorizer.transform([temp])
    pred = clf.predict(X_predict)
    cursor3.execute('update temp set du_bao=? where idx=?',  cac_cd[int(pred)], idx)
    print(pred, '=',  cac_cd[int(pred)])
cnxn.commit()
    
                                     
    
    
    


