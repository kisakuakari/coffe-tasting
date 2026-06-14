#!/usr/bin/env python3
import streamlit as st
from database import get_judge_by_email, save_score, get_coffee_info
from matching import get_assignments_for_judge
from scoring import calculate_total_score

def main() -> None:
    appearance = [1, 2, 3]
    aroma = [1, 2, 3, 4, 5, 6, 7]
    flavor = [1, 2、3, 4, 5, 6, 7, 8, 9, 10]
    email = st.text_input('メールアドレスを入力してください')
    if get_judge_by_email(email):
        judge = get_judge_by_email(email)
        assignments = get_assignments_for_judge(judge)
        for coffee in assignments:
            submit_btn = st.button("ログイン")
            st.write('外観')
            st.radio("1~3", appearance, horizontal=True)
            st.write('香り')
            st.radio("1~7", aroma, horizontal=True)
            st.write('味わい')
            st.radio("1~10", flavor, horizontal=True)


if __name__ == "__main__":
    main()