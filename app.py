import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import cv2
import numpy as np
import requests
import json

st.title("履歴書OCRアプリ")

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

# Notion APIのエンドポイント、データベースID、シークレットトークンを設定
notion_api_url = "https://api.notion.com/v1/pages"
database_id = "1c252a10951580368a9ecfcb5e648d61"      # 自身のデータベースIDに置き換えてください
notion_secret = "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"    # 自身の統合シークレットに置き換えてください

def preprocess_image(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

if uploaded_file:
    if st.button("読込"):
        with st.spinner("OCR処理中..."):
            images = convert_from_bytes(uploaded_file.read(), dpi=300)
            # OCRの設定
            custom_config = r'--oem 3 --psm 6'

            full_text = ""
            # for img in images:
            #     # 前処理（グレースケールと2値化）
            #     processed_img = preprocess_image(img)
            #     # OCR処理
            #     text = pytesseract.image_to_string(processed_img, lang="jpn", config=custom_config)
            #     full_text += text
            
            test_dict = {
                "name": "テスト太郎",
                "age": 30,
                "address": "テスト県テスト待ち",
                "academy": "テスト大学",
                "company": "テスト株式会社"
            }
            
            # Notion APIに渡すペイロードを作成（データベースに定義されているプロパティ名に合わせる必要があります）
            payload = {
                "parent": { "database_id": database_id },
                "properties": {
                    "Name": {  # タイトルプロパティ
                        "title": [
                            {
                                "text": {
                                    "content": test_dict["name"]
                                }
                            }
                        ]
                    },
                    "Age": {  # 数値プロパティ
                        "number": test_dict["age"]
                    },
                    "Address": {  # リッチテキストプロパティ
                        "rich_text": [
                            {
                                "text": {
                                    "content": test_dict["address"]
                                }
                            }
                        ]
                    },
                    "Academy": {  # リッチテキストプロパティ
                        "rich_text": [
                            {
                                "text": {
                                    "content": test_dict["academy"]
                                }
                            }
                        ]
                    },
                    "Company": {  # リッチテキストプロパティ
                        "rich_text": [
                            {
                                "text": {
                                    "content": test_dict["company"]
                                }
                            }
                        ]
                    }
                }
            }

            # HTTPヘッダーの設定
            headers = {
                "Authorization": f"Bearer {notion_secret}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"  # Notion APIのバージョン。必要に応じて最新のものに変更してください
            }

            # POSTリクエストを送信し、Notionデータベースにデータを追加
            response = requests.post(notion_api_url, headers=headers, json=payload)

            # レスポンスの確認
            print("ステータスコード:", response.status_code)
            print("レスポンス内容:", response.text)


        st.success("OCRが完了しました！")
        st.subheader("抽出したテキスト")
        st.text_area("OCR結果", full_text, height=400)
    else:
        st.info("「読込」ボタンを押してOCRを開始してください。")