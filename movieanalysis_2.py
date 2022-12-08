#ライブラリインポート
import cv2
#動画ファイルの読み込み
movie = cv2.VideoCapture('output.mp4')
#フレーム数の取得

nframe = int(movie.get(cv2.CAP_PROP_FRAME_COUNT)) // int(30)
#画像化処理
for i in range(nframe):
    ret, frame = movie.read()
    cv2.imwrite(r'C:\Users\dishi\pro_con\moviedata\moviedata'+str(i).zfill(3)+'.jpg', frame)