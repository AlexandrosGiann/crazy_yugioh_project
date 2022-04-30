import streamlit as st

code = st.text_input('')

if code:
    f = open('game_data.txt', 'w')
    f.write(code)
    f.close()

