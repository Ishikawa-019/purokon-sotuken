import sys,os.path
import subprocess
import wave
from pydub import AudioSegment
import librosa
import soundfile as sf
import struct
from scipy import fromstring, int16
import numpy as np
import math
import time
import requests
import json
import glob
import PySimpleGUI as sg

# メインのコントロールエリア
control_layout = [
    [sg.Text('録画を開始する際はSTARTボタンを、終了する際はSTOPボタンを押してください。')],
    [sg.Text('STOPボタンを押すと分析が始まります。結果が出るまでお待ちください。')],
    [sg.Text('ENDボタンでウィンドウが閉じます。')],
    [sg.Button('START', size=(10, 1)), sg.Button('STOP', size=(10, 1)), sg.Button('END', size=(10, 1))],
]

# ログの表示・操作エリア
log_layout = [
    [sg.Output(size=(100, 5),key="-OUTPUT-")]
]

layout = [
    [sg.Frame("説明", control_layout)],
    [sg.Frame("Log", log_layout)]
]

# ウィンドウを作成
window = sg.Window("TSUWA", layout)
cmd = ""
file_na = ""
p = None
rec_flag = False
url = 'https://api.webempath.net/v2/analyzeWav'
apikey = 'I9D0hwNxDJpBbDRv2fDtouE3bWpzAuCihpJVzc7bSic'
payload = {'apikey': apikey}
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'END':
        break
    if event == 'START':
        for wav in glob.glob('C:/Users/dishi/pro_con/voice02/voice*.wav'):
            os.remove(wav)
        if rec_flag == False:
            cmd = "sox -t waveaudio -d out01.wav"
            p = subprocess.Popen(cmd.split())
            p.terminate()
            rec_flag = True
            print('録音開始')
        
    if event =='STOP':
        if  rec_flag == True:
            p.terminate()
            print('録音を終了')
            try:
                p.wait(timeout=1)
                rec_flag = False
            except subprocess.TimeoutExpired:
                p.kill()
                rec_flag = False
        time.sleep(1)
        #wavファイルの変換
        y, sr = librosa.core.load('out01.wav', sr=11025, mono=True) # 22050Hz、モノラルで読み込み
        sf.write("new_out01.wav", y, sr, subtype="PCM_16") #1
        sound = AudioSegment.from_wav("new_out01.wav")
        sound = sound.set_channels(1)
        sound.export("new_out01.wav", format="wav")
        # wavファイルをどの間隔で区切りたいか？（単位[sec]）
        cut_time = 5
        # 分割したいwavファイルの格納先
        audio_change_wav = 'new_out001.wav'
        # wav分割ファイルの格納先
        wav_cut_dir = 'C:/Users/dishi/pro_con/voice02/voice'
        # wav読み込み
        wr = wave.open(audio_change_wav, "r")
    
        # wav情報を取得
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        integer = math.floor(total_time)
        t = int(cut_time)
        frames = int(ch * fr * t)
        # 小数点切り上げ（1分に満たない最後のシーンを出力するため）
        num_cut = int(math.ceil(integer / t))
        data = wr.readframes(wr.getnframes())
        wr.close()
    
        X = np.frombuffer(data, dtype=int16)
    
        for i in range(num_cut):
            outf = wav_cut_dir + str(i) + '.wav'
            start_cut = int(i * frames)
            end_cut = int(i * frames + frames)
            Y = X[start_cut:end_cut]
            outd = struct.pack("h" * len(Y), *Y)
    
            # 書き出し
            ww = wave.open(outf, "w")
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
            ww.close()

        cal_sum=0   #平常
        ang_sum=0   #怒り
        joy_sum=0   #喜び
        sor_sum=0   #悲しみ
        ene_sum=0   #元気
        count=0     #ファイル数

        for wav in glob.glob(r'C:\Users\dishi\pro_con\voice02\voice*.wav'):
            data = open(wav, 'rb')
            file = {'wav': data}

            res = requests.post(url, params=payload, files=file)
            kekka = json.loads(res.text)
            if kekka['error'] == 1001:
                print('API keyが空です')
                break
            elif kekka['error'] == 1002:
                print('wavファイル送信されていません')
                break
            elif kekka['error'] == 1003:
                print('contet-typeがmulripart/form-dataで始まりません')
                break
            elif kekka['error'] == 1011:
                print('wavファイルがPCM_FLOAT,PCM_SIGNED,PCM_UNSIGNEDのいずれにも該当しません')
                break
            elif kekka['error'] == 1012:
                print('wavファイルのサンプリング周波数が11025Hz以外です')
                break
            elif kekka['error'] == 1013:
                print('wavファイルがモノラルではありません')
                break
            elif kekka['error'] == 1014:
                print('wavファイルの録音秒数が5秒以上です')
                break
            elif kekka['error'] == 1015:
                print('wavファイルのサイズが1.9MB以上です')
                break
            elif kekka['error'] == 1016:
                print('wavファイルが妥当な音声として読み取れません')
                break
            elif kekka['error'] == 1017:
                print('不正なAPIバージョンが指定されました')
                break
            elif kekka['error'] == 2001:
                print('送信されたAPI keyはAPIコール回数上限を超過しました')
                apikey = 'Rla2mV6XkggQ-2FpJUkCKjO1JdGJF6gD61egg0ELJE4'
                continue
            elif kekka['error'] == 2002:
                print('アカウントまたはその状態が不正です')
                break
            elif kekka['error'] == 2003:
                print('送信されたAPI key利用可能な状態ではありません')
                apikey = 'Rla2mV6XkggQ-2FpJUkCKjO1JdGJF6gD61egg0ELJE4'
                continue
            elif kekka['error'] == 1017:
                print('送信されたAPI keyは利用できないか、存在しません')
                break
            elif kekka['error'] == 1017:
                print('不正なAPIバージョンが指定されました')
                break
            elif kekka['error'] == 3001:
                print('許可されていない国からのアクセスである')
                break
            elif kekka['error'] == 9999:
                print('内部エラー')
                break
            error = kekka['error']    
            cal = kekka['calm']
            ang = kekka['anger']
            joy = kekka['joy']
            sor = kekka['sorrow']
            ene = kekka['energy']
            cal_sum += cal   #平常
            ang_sum += ang   #怒り
            joy_sum += joy   #喜び
            sor_sum += sor   #悲しみ
            ene_sum +=ene   #元気            
            count += 1
            time.sleep(1)
        
        kekka = json.loads(res.text)
        cal_ave = cal_sum/count
        ang_ave = ang_sum/count
        joy_ave = joy_sum/count
        sor_ave = sor_sum/count
        ene_ave = ene_sum/count
        print('calm:',cal_ave,'anger:',ang_ave,'joy:',joy_ave,'sorrow:',sor_ave,'energy:',ene_ave)
        if ene_ave>=25: 
            if joy_ave>=25:
                print('元気もあり、楽しそうですね')
            print('元気がいいですね')
        if joy_ave>=25:
            print('楽しそうに話せています')
        if cal_ave>=25:
            print('落ち着いて会話できています')
        if ang_ave>=25:
            print('怒りっぽく聞こえています')
        elif sor_ave>=25:
            print('悲しく聞こえています')
        
window.close()