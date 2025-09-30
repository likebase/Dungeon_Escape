⚠ 現在、公共データポータルのAPIサーバーがダウンしているため、プログラムは正常に動作しません。⚠  
⚠ PlayVideoフォルダ内のプレイ動画で確認することができます。⚠  
⚠ Anacondaを使用する場合は「Dungeon_Escape.ipynb」を、Visual Studio Codeを使用する場合は「Dungeon_Escape.py」を使用してください。⚠  

---------- コンテンツの主な特徴 ----------
 - MediaPipeと音声認識を利用したナチュラルユーザーインターフェース（NUI）による操作
 - リアルタイムの天気データを反映し、コンテンツ環境に影響を与える  

---------- キャラクター操作 ----------  
【探索】  
 - MediaPipeのハンドトラッキングでキャラクターを操作
 - カメラで検出されたエリアに基づいてキャラクターが移動
【バトル】  
 - マイクを接続し、右側に表示されるガイドコマンドに従ってバトルアクションを実行

---------- 外部パッケージ（インストール必要） ----------  
 - pygame
 - opencv-python
 - numpy
 - SpeechRecognition
 - mediapipe
 - requests
 - xmltodict

---------- 内部パッケージ（インストール不要） ----------  
 - math
 - sys
 - random
 - time
 - threading
 - weather（プロジェクトソースに含まれるカスタムモジュール）

---------- セットアップガイド ----------  
【Anacondaユーザー向け】  
1. 仮想環境の作成（Anaconda Promptで入力）  
  ① conda create -n venv python=3.10 -y  
  ② conda activate venv  
2. pipと基本ツールのアップグレード  
  ① python -m pip install --upgrade pip setuptools wheel  
3. 必要なパッケージのインストール  
  ① pip install pygame opencv-python mediapipe SpeechRecognition requests xmltodict numpy  

【Visual Studio Codeユーザー向け】  
1. Python 3.10以上をインストール  
  ① 公式Pythonサイトからダウンロード  
2. 仮想環境の作成（Visual Studio Codeのターミナルで入力）  
  ① cd C:\python 　　# 例：プロジェクトフォルダに移動  
  ② python -m venv venv  
  ③ venv\Scripts\activate  
3. pipのアップグレード  
  ① python -m pip install --upgrade pip setuptools wheel  
4. 必要なパッケージのインストール  
  ① pip install pygame opencv-python mediapipe SpeechRecognition requests xmltodict numpy  
5. プロジェクトの実行（プロジェクトフォルダ内で実行してください）  
  ① python Dungeon_Escape.py  
