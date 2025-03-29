import streamlit as st
import pdfplumber
import pytesseract
import cv2
import numpy as np
import requests
from PIL import Image

st.title("履歴書OCRアプリ")

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

notion_api_url = "https://api.notion.com/v1/pages"
database_id = "1c252a10951580368a9ecfcb5e648d61"
notion_secret = "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"

# def preprocess_image(img):
#     gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return thresh

if uploaded_file:
    if st.button("読込"):
        with st.spinner("OCR処理中..."):
            full_text = "テスト"

            # with pdfplumber.open(uploaded_file) as pdf:
            #     for page in pdf.pages:
            #         img = page.to_image(resolution=300).original
            #         processed_img = preprocess_image(img)
            #         text = pytesseract.image_to_string(processed_img, lang="jpn", config="--oem 3 --psm 6")
            #         full_text += text

            test_dict = {
                "name": "テスト太郎",
                "age": 30,
                "address": "テスト県テスト町",
                "academy": "テスト大学",
                "company": "テスト株式会社"
            }

            payload = {
                "parent": {"database_id": database_id},
                "properties": {
                    "Name": {"title": [{"text": {"content": test_dict["name"]}}]},
                    "Age": {"number": test_dict["age"]},
                    "Address": {"rich_text": [{"text": {"content": test_dict["address"]}}]},
                    "Academy": {"rich_text": [{"text": {"content": test_dict["academy"]}}]},
                    "Company": {"rich_text": [{"text": {"content": test_dict["company"]}}]}
                }
            }

            headers = {
                "Authorization": f"Bearer {notion_secret}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }

            response = requests.post(notion_api_url, headers=headers, json=payload)

            print("ステータスコード:", response.status_code)
            print("レスポンス内容:", response.text)

        st.success("OCRが完了しました！")
        st.subheader("抽出したテキスト")
        st.text_area("OCR結果", full_text, height=400)
    else:
        st.info("「読込」ボタンを押してOCRを開始してください。")
