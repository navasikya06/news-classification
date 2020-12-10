# Cac model
import numpy as np
from time import time
import pyodbc
from pyvi import ViTokenizer
import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer ,CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=F:\\TTX_Tintulieu\\Ly\\temp.mdb;'
    )
cnxn = pyodbc.connect(conn_str)
cursor1 = cnxn.cursor()
cursor2 = cnxn.cursor()

# % Read idx, document, subject from datasae
def read_db():
    # Khai bao 
    p1 = re.compile(r'''\[kw\].*\[/kw\]|\[su\].*\[/su\]|\[id\].*\[/id\]|\[au\].*\[/au\]''')
    p2 = re.compile(r'''\[ti\]|\[/ti\]|\[ca\]|\[/ca\]''')
    punct = string.punctuation
    punct = re.sub('_', '', punct)
    cac_cd = ['Bổ túc VH-Xóa mù chữ', 'Đại học', 'Đại học-cao học-cao đẳng', 'Điển hình', 'Du học, lưu học sinh', 'Giáo dục phổ thông', 'Giáo viên', 'Kỳ thì chuyển cấp', 'Sở giáo dục', 'Thi-Tuyển sinh', 'Trung học chuyên nghiệp-d/nghề', 'Vấn đề chung Giáo dục', 'Công nghệ ( nói chung )', 'Đánh giá tổng quát', 'Điển hình', 'Khoa học ( nói chung )', 'Khoa học kỹ thuật-Công nghệ', 'Khoa học xã hội', 'Kinh tế chung', 'Môi trường']
    
    # Read db
    noi_dung = []
    label = []
    cursor1.execute('select noi_dung, chu_de from temp')
    row1s = cursor1.fetchall()
    for row1 in row1s:
        cd = row1.chu_de
        cs = cac_cd.index(cd)
        label.append(cs)
        temp = row1.noi_dung
        temp = re.sub(p1, ' ', temp)
        temp = re.sub(p2, ' ', temp)
        temp = ViTokenizer.tokenize(temp)
        for c in punct:
            c = '\\'+c
            temp = re.sub(c, ' ', temp)
        noi_dung.append(temp.lower())
    return noi_dung, label

# % accuracy of classifiers
def acc_clf(clf,ts):
    clf_descr = str(clf).split('(')[0]+ts
    print(clf_descr)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)
    t0 = time()
    pred = clf.predict(X_test)      
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)
    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)
    return

# % Main
print('=' * 80)
print('Read database')
noi_dung, label = read_db()
print('Done')
print('=' * 80)
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
X = vectorizer.fit_transform(noi_dung)
X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.1, random_state=0)
print('LinearSVC => SGDClassifier')
for penalty in ["l2", "l1"]:
    print('-' * 80)
    print("%s penalty" % penalty.upper())
    # Train Liblinear model
    ts='_'+penalty
    acc_clf(LinearSVC(penalty=penalty, dual=False, tol=1e-3),ts)
    # Train SGD model
    acc_clf(SGDClassifier(alpha=.0001, penalty=penalty),ts)
     






    
    
