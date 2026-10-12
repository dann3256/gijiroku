import streamlit as st

st.title("議事録自動入力アプリ")


#メモを入力する欄
memo = st.text_area("会議のメモを貼り付けてください", height=200)

if st.button("議事録を作る"):
    st.write("入力されたメモ:")
    st.write(memo)