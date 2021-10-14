import streamlit as st
from moviepy.editor import *
import requests
import struct
import json
from numpy import load
from numpy import expand_dims
from matplotlib import pyplot
from PIL import Image, ImageDraw, ImageFont, ImageFile
import numpy as np
import os
import random as _random
import string

st.set_page_config(layout="wide", page_title="微信公众号:Streamlit")
st.markdown("<h2 style='text-align: center; color: blue;'>微信公众号：Streamlit</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>长按下方二维码进行关注</h4>", unsafe_allow_html=True)
c1, c2, c3, c4, c5=st.columns([2,1,0.5,1,2])
with c1:
	st.empty()
with c2:
	st.image("公众号Streamlit作者二维码.png")
with c3:
	st.empty()
with c4:
	st.image("公众号Streamlit二维码.jpg")
with c5:
	st.empty()


choose = st.sidebar.radio("请选择一个要打开的应用",("中英文互翻","MP4视频转GIF","ASCII字符画","密码生成器"))
if choose == "中英文互翻":
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

elif choose == "MP4视频转GIF":
	#获取视频时长信息
	def get_video_duration(video_file):
	    with open(video_file,'rb') as fp:
	        data = fp.read()
	    index = data.find(b'mvhd') + 4
	    time_scale = struct.unpack('>I', data[index+13:index+13+4])
	    durations  = struct.unpack('>I', data[index+13+4:index+13+4+4])
	    duration = durations[0] / time_scale[0]
	    return duration

	#下载按钮效果设置
	css = """<style>
	.stDownloadButton>button {
	    background-color: #0099ff;
	    color:#ffffff;
	}

	.stDownloadButton>button:hover {
	    background-color: #00ff00;
	    color:#ffffff;
	    }
	</style>
	"""
	st.markdown(css, unsafe_allow_html=True)

	#隐藏按钮及底部链接
	sysmenu = '''
	<style>
	#MainMenu {visibility:hidden;}
	footer {visibility:hidden;}
	'''
	st.markdown(sysmenu,unsafe_allow_html=True)

	#设置要选择的16:9黄金分辨率和每秒要抽取的帧数
	fenbianlv = st.sidebar.selectbox("请选择要设置的GIF图片分辨率",("1280×720","960×540","854×480","320×180","720×405","640×360","480×270"))
	zhenshu = st.sidebar.slider('每秒抽取帧数', min_value=5, max_value=15, value=10, step=1)

	if fenbianlv == "1280×720":
		set_fenbianlv=(1280,720)
	elif fenbianlv == "960×540":
		set_fenbianlv=(960,540)
	elif fenbianlv == "854×480":
		set_fenbianlv=(854,480)
	elif fenbianlv == "720×405":
		set_fenbianlv=(720,405)
	elif fenbianlv == "640×360":
		set_fenbianlv=(640,360)
	elif fenbianlv == "320×180":
		set_fenbianlv=(320,180)	


	file = st.file_uploader("请上传你要处理的mp4视频文件", type=["mp4"])


	if file is not None:
		try:
			time = get_video_duration(file.name)
			#设置裁剪视频的起止时间段
			middle_time = st.sidebar.slider('请选择要裁剪的视频起始时间段',0.0, round(time,1), (round(time,1)/3, round(time,1)/2))

			st.sidebar.subheader("上传的视频")
			st.sidebar.video(file)

			clip =VideoFileClip(file.name).subclip(middle_time[0],middle_time[1]).resize((set_fenbianlv))
			clip.write_gif("movie.gif",fps=zhenshu)
			
			st.image("movie.gif")

			with open("movie.gif", "rb") as giffile:
			    btn = st.download_button(
			        label="点我下载生成的动图",
			        data=giffile,
			        file_name="生成的动图.gif",
			        mime="image/gif"
	        )

		except RuntimeError:
			st.warning("GIF文件大小超过限制，分辨率或帧数过高，请调整！")

elif choose == "ASCII字符画":
	st.header("上传一张图片生成ASCII字符画")

	ImageFile.LOAD_TRUNCATED_IMAGES = True
	Image.MAX_IMAGE_PIXELS = None

	color_fornt = st.sidebar.color_picker('选择前景色', '#00b8e6')

	color_background = st.sidebar.color_picker('选择背景色', '#ffffff')

	sc_control = st.sidebar.slider('选择密度参数1', 0.1, 0.9, 0.5, 0.1)
	gcf_control = st.sidebar.slider('选择密度参数2', 0.5, 4.5, 2.1, 0.1)

	uploaded_file = st.file_uploader("选择一张图片", type=["png","jpg","bmp","jpeg"])

	@st.cache()
	def asciiart(in_f, SC, GCF,  out_f, bgcolor=color_background):

	    chars = np.asarray(list(' .,:irs?@9B&#*$%!~'))

	    font = ImageFont.load_default()
	    letter_width = font.getsize("x")[0]
	    letter_height = font.getsize("x")[1]
	    WCF = letter_height/letter_width
	    img = Image.open(in_f)
	    widthByLetter=round(img.size[0]*SC*WCF)
	    heightByLetter = round(img.size[1]*SC)
	    S = (widthByLetter, heightByLetter)
	    img = img.resize(S)
	    img = np.sum(np.asarray(img), axis=2)
	    img -= img.min()
	    img = (1.0 - img/img.max())**GCF*(chars.size-1)
	    lines = ("\n".join( ("".join(r) for r in chars[img.astype(int)]) )).split("\n")
	    nbins = len(lines)
	    newImg_width= letter_width *widthByLetter
	    newImg_height = letter_height * heightByLetter
	    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
	    draw = ImageDraw.Draw(newImg)
	    leftpadding=0
	    y = 0
	    lineIdx=0
	    
	    for line in lines:
	        color = color_fornt
	        lineIdx +=1
	        draw.text((leftpadding, y), line, color, font=font)
	        y += letter_height

	    newImg.save(out_f)

	@st.cache()
	def load_image(filename, size=(512,512)):
		pixels = load_img(filename, target_size=size)
		pixels = img_to_array(pixels)
		pixels = (pixels - 127.5) / 127.5
		pixels = expand_dims(pixels, 0)
		return pixels

	@st.cache()
	def imgGen2(img1):
	  inputf = img1
	  SC = sc_control
	  GCF= gcf_control
	  asciiart(inputf, SC, GCF, "results.png",color_background)
	  img = Image.open(img1)
	  img2 = Image.open('results.png').resize(img.size)
	  return img2	

	#下载按钮效果设置
	css = """<style>
	.stDownloadButton>button {
	    background-color: #0099ff;
	    color:#ffffff;
	}

	.stDownloadButton>button:hover {
	    background-color: green;
	    color:white;
	    }
	</style>
	"""
	st.markdown(css, unsafe_allow_html=True)


	if uploaded_file is not None:
	    st.sidebar.image(uploaded_file, caption='原始图片', use_column_width=True)
	    im = imgGen2(uploaded_file)	
	    st.image(im, width=700)
	    with open("results.png", "rb") as file:
	        #st.image("图片.jpg")
	        btn = st.download_button(
	            label="点我下载生成的ASCII字符画",
	            data=file,
	            file_name="ASCII字符画.png",
	            mime="image/png"
	            ) 	


elif choose == "密码生成器":
	st.markdown("<h1 style='text-align: center; color: blue;'>密码生成器</h1>", unsafe_allow_html=True)
	length = st.number_input('请选择你要设置的密码长度', min_value=10, max_value=100)
	title = st.write('请勾选生成的密码包含的类型')
	cb1 = st.checkbox('数字')
	cb2 = st.checkbox('字母')
	cb3 = st.checkbox('特殊字符($%?!)')
	empty = st.empty()

	if cb1 == True:
	        numbers = "0123456789"
	else:
	        numbers = ""
	if cb2 == True:
	        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz"
	else:
	        letters = ""
	if cb3 == True:
	        symbols = string.punctuation
	else:
	        symbols = ""
	if cb1 and cb1 and cb3 == None: 
	        st.warning("请至少勾选1种类型")

	all = letters + str(numbers) + symbols
	#生成密码列表
	try:
	        temp = _random.sample(all, length)
	except ValueError:
	        pass	                
	try:
	        temp2 = _random.sample(all, length)
	except ValueError:
	        pass
	try:
	        temp3 = _random.sample(all, length)
	except ValueError:
	        pass
	try:
	        temp4 = _random.sample(all, length)
	except ValueError:
	        pass

	#从列表中取出元素组成密码
	try:
	        password = "".join(temp)
	except ValueError and NameError:
	        pass
	try:
	        password2 = "".join(temp2)
	except ValueError and NameError:
	        pass
	try:
	        password3 = "".join(temp3)
	except ValueError and NameError:
	        pass
	try:
	        password4 = "".join(temp4)
	except ValueError and NameError:
	        pass

	#打印密码
	try:
	        st.code(password)
	        st.code(password2)
	        st.code(password3)
	        st.code(password4)

	except ValueError and NameError:
	        st.warning("请至少勾选1种类型")       

