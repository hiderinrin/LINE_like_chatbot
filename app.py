import streamlit as st
import openai
import base64
import textwrap

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

# 入力欄を中央に配置するために3つの列を作成
# cols = st.columns(3)

# 中央の列にメッセージ入力欄を配置
# user_input = cols[1].text_area("メッセージを入力してください。", key="user_input", on_change=communicate)

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

# メッセージ入力欄をページ全体の幅に広げる
# user_input = st.text_area("メッセージを入力してください。", key="user_input")
# メッセージ入力欄をページ全体の幅に広げる（1行の入力欄に変更）
# user_input = st.text_input("メッセージを入力してください。", key="user_input")

# # 送信ボタンを追加
# if st.button("送信"):
#     if user_input:  # 入力が空でないことを確認
#         communicate()
#         st.session_state["user_input"] = ""  # 入力欄を消去
#         user_input = ""  # これも追加してみてください


if st.session_state["messages"]:
    messages = st.session_state["messages"]

# LINE風デザインを適用するためのカスタムCSS
# 縦スクロールバーの追加と、文字の表示を左端から始めるようにする
custom_css = '''
<style>
    .container {
        background-color: #7a7a7a;
        border-radius: 10px;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        align-items: center;
    }
    .message {
        background-color: #4caf50;
        color: black;
        border-radius: 15px;
        padding: 5px 10px;
        white-space: pre-wrap;
        text-align: left;
    }
    .assistant {
        text-align: right;
    }
    .assistant .message {
        background-color: #1a1a1a;
        color: white;
        text-align: left;
    }
    .fixed-height {
        height: auto;
        overflow-y: scroll;
        width: 100%;
        display: flex;
        flex-direction: column;
    }
    .stTextInput textarea {
        width: 100% !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
</style>
'''


st.markdown(custom_css, unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="fixed-height">', unsafe_allow_html=True)

    reversed_messages = list(reversed(messages[1:]))
    
    # reversed_messagesをイテレーション
    for i in range(0, len(reversed_messages), 2):
        user_message = reversed_messages[i]
        bot_message = reversed_messages[i + 1] if i + 1 < len(reversed_messages) else None
        
        if bot_message:
            content = f'<div class="container"><div class="message">おやじ💪: {bot_message["content"]}</div></div>'
            st.markdown(content, unsafe_allow_html=True)

        content = f'<div class="container assistant"><div class="message">ChatGPT🤖: {user_message["content"]}</div></div>'
        st.markdown(content, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# message_input_container = st.empty()
# st.write(" ")  # スペースを挿入して、下部の余白を作成

# # 入力欄を中央に配置するために3つの列を作成
# cols = st.columns(3)

# # 中央の列にメッセージ入力欄を配置
# user_input = cols[1].text_area("メッセージを入力してください。", key="user_input", on_change=communicate)


