import streamlit as st
import openai
import base64

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

message_input_container = st.empty()

user_input = message_input_container.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    # LINE風デザインを適用するためのカスタムCSS
    custom_css = """
    <style>
        .container {
            background-color: #1a1a1a;
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
            white-space: nowrap;
        }
        .assistant {
            text-align: right;
        }
        .assistant .message {
            background-color: #1a1a1a;
            color: white;
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        if message["role"] == "assistant":
            content = f'<div class="container assistant"><div class="message">ChatGPT🤖: {message["content"]}</div></div>'
        else:
            content = f'<div class="container"><div class="message">おやじ💪: {message["content"]}</div></div>'
        st.markdown(content, unsafe_allow_html=True)
