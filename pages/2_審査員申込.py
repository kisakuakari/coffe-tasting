#!/usr/bin/env python3
import streamlit as st
from database import add_judge, check_judge_exists

prefectures = [
    "未選択", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", 
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", 
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", 
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", 
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

def main() -> None:
    with st.form("my_form"):
        st.title('審査員申込')
        st.write('')
        st.write('1. 基本情報')
        st.write('以下の項目に記入をお願い致します')
        name = st.text_input("氏名")
        name_kana = st.text_input("よみがな")
        prefecture = st.selectbox("都道府県", prefectures)
        address = st.text_input("住所（都道府県以下）")
        phone = st.text_input("電話番号")
        email = st.text_input("メールアドレス")
        workplace = st.text_input("勤務先")

        st.write('')
        st.write('2. 審査員画像（任意)')
        uploaded_file = st.file_uploader('画像をアップロードしてください(JPEG / PNG のみ、最大5MB)', type=['jpeg', 'jpg', 'png'])
        submit_btn = st.form_submit_button()

    if submit_btn:
        is_valid = True
        if not name:
            st.error("氏名は必須です")
            is_valid = False
        if prefecture == "未選択":
            st.error("都道府県は必須です")
            is_valid = False
        if not address:
            st.error("住所は必須です")
            is_valid = False
        if not phone:
            st.error("電話番号は必須です")
            is_valid = False
        if not email:
            st.error("メールアドレスは必須です")
            is_valid = False
        if not workplace:
            st.error("勤務地は必須です")
            is_valid = False
        if check_judge_exists(email):
            st.error("既に登録済みです")
            is_valid = False
        if uploaded_file != None:
            if uploaded_file.size > 5*1024*1024:
                st.error('サイズが大きいです')
                is_valid = False
        judge_data = {
                "name": name,
                "name_kana": name_kana,
                "prefecture": prefecture,
                "address": address,
                "phone": phone,
                "email": email,
                "workplace": workplace,
            }
        if is_valid == True:
            add_judge(judge_data)

if __name__ == "__main__":
    main()

