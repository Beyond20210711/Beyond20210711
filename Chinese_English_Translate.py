import streamlit as st
import requests
import json

st.set_page_config(layout="wide", page_title="中英单词互翻神器")

st.header("中英单词互翻神器")
st.info("要翻译中文单词，请输入中文，会返回对应英文；\n\n\n\n要翻译英文单词，请输入英文，会返回对应中文;")

danci = st.text_input("请输入要查找的中文单词或英文单词")
fanhui = requests.get("http://dict.iciba.com/dictionary/word/suggestion?word="+danci)
data1 = fanhui.text
data2 = json.loads(data1)
for i in range(len(data2["message"])):
	st.write(data2["message"][i]["key"],data2["message"][i]["paraphrase"])

#隐藏按钮及底部链接
sysmenu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sysmenu,unsafe_allow_html=True)
