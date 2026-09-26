import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

# 设置页面配置
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)


# 保存会话信息
def save_session():
    # 构建新的会话对象
    new_session = {
        "session_time": st.session_state.session_time,
        "name": st.session_state.name,
        "character": st.session_state.character,
        "messages": st.session_state.messages
    }
    if not os.path.exists("sessions"):
        os.makdir("sessions")
    with open(f'sessions/{st.session_state.session_time}.json', 'w', encoding='utf-8') as f:
        json.dump(new_session, f, ensure_ascii=False, indent=2)


# 会话时间
def generate_session_time():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")
#加载所有会话列表
def load_sessions():
    session_list=[]
    if os.path.exists('sessions'):
        file_list=os.listdir('sessions')
        for file_name in file_list:
            if file_name.endswith('.json'):
                session_list.append(file_name[:-5])
    session_list.sort(reverse=True)
    return session_list
#加载指定对话信息
def load_session(session_name):
    try:
        if os.path.exists(f'sessions/{session_name}.json'):
            with open(f'sessions/{session_name}.json', 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                st.session_state.session_time = session_name
                st.session_state.name = session_data['name']
                st.session_state.character = session_data['character']
                st.session_state.messages = session_data['messages']
    except Exception:
        st.error("加载会话失败！")
#删除会话信息
def delete_session(session_name):
    try:
        if os.path.exists(f'sessions/{session_name}.json'):
            os.remove(f'sessions/{session_name}.json')
            # 如果删除的是当前会话,则需要更新会话列表
            if session == st.session_state.session_time:
                st.session_state.messages = []
                st.session_state.session_time = generate_session_time()
    except Exception:
        st.error("会话删除失败！")

# 大标题
st.title("AI智能伴侣")
# 系统提示词
ts = '你是一个%s的助手，你的名字是%s'
# 初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []
# 昵称
if 'name' not in st.session_state:
    st.session_state.name = '助手'
# 性格
if 'character' not in st.session_state:
    st.session_state.character = '温柔'
# 会话标识
if 'session_time' not in st.session_state:
    st.session_state.session_time = generate_session_time()
# 会话名称
st.text(f"会话名称:{st.session_state.session_time}")
# 创建一个聊天界面
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
# 侧边栏
with st.sidebar:
    st.subheader('AI控制面板')
    if st.button('新建对话', width='stretch', icon='✏️'):
        # 保存当前对话
        save_session()
        # 创建新的对话
        if st.session_state.messages:
            st.session_state.messages=[]
            st.session_state.session_time = generate_session_time()
            save_session()
    # 会话历史
    st.text('会话历史')
    load_sessions()
    for session in load_sessions():
        col1,col2=st.columns([4,1])
        with col1:
            #加载会话信息
            if st.button(session, width='stretch', icon='📄',type='primary'if session == st.session_state.session_time else 'secondary'):
                load_session(session)
                st.rerun()
        with col2:
            #删除会话信息
            if st.button('', width='stretch', icon='❌',key=f'delete_{session}'):
                delete_session(session)
                st.rerun()
    #分割线
    st.divider()
    # 伴侣信息
    st.subheader('伴侣信息')
    name = st.text_input('昵称', placeholder='请输入昵称', value=st.session_state.name)
    if name:
        st.session_state.name = name
    character = st.text_area('性格', placeholder='请输入性格', value=st.session_state.character)
    if character:
        st.session_state.character = character
# ai模型的调用
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
# 创建一个输入框，用于用户输入问题
prompt = st.chat_input("请输入您要问的问题")
if prompt:
    st.chat_message("user").write(prompt)
    # 将用户问题添加到会话状态变量中
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 调用AI模型
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": ts % (st.session_state.character, st.session_state.name)},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    # 流式输出
    response_message = st.empty()
    full_respond = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_respond += content
            response_message.chat_message("assistant").write(full_respond)
    # 非流式输出
    # print(response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # 将AI模型的响应添加到会话状态变量中
    st.session_state.messages.append({"role": "assistant", "content": full_respond})
    save_session()



