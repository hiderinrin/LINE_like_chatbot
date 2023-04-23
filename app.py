%%writefile app.py

import streamlit as st
import openai

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
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    # LINE風表示のためのカスタムスタイル
    st.markdown("""
    <style>
        .bubble {
            display: inline-block;
            padding: 10px;
            border-radius: 20px;
            margin-bottom: 5px;
        }
        .user {
            background-color: #E6E6FA;
            float: left;
            clear: both;
        }
        .assistant {
            background-color: #00BFFF;
            float: right;
            clear: both;
        }
        .speaker {
            font-weight: bold;
            margin-bottom: 2px;
        }
    </style>
    """, unsafe_allow_html=True)

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        if message["role"] == "user":
            speaker = "おやじ💪"
            bubble_class = "user"
        else:
            speaker = "ChatGPT🤖"
            bubble_class = "assistant"

        # カスタムスタイルを適用したメッセージ表示
        st.markdown(f"""
        <div class="bubble {bubble_class}">
            <p class="speaker">{speaker}</p>
            <p>{message["content"]}</p>
        </div>
        """, unsafe_allow_html=True)
