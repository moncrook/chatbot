import streamlit as st
import google.generativeai as genai
import json
import os

# Configure the API key
genai.configure(api_key="AIzaSyCtYTMC6RXStb2GMdvaHujENoEUkOSIWAI")

# Set up the model with default configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# CSS tùy chỉnh
st.markdown(
    """
    <style>
    # body {
    #     background-color: #87a0b0 !important ; /* Dùng !important để ghi đè CSS mặc định */
    # }
    .stChatMessage {
        background-color: #093552;
        # color: pink; 
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
    }/* Màu chữ cho tin nhắn người dùng (màu trắng) */
    .stChatMessage:not([data-role="assistant"]) .stMarkdown {
        color: white !important;
    }

    /* Màu chữ cho tin nhắn của bot (màu hồng) */
    .stChatMessage[data-role="assistant"] .stMarkdown {
        color: pink !important;
    }
    /* Thêm kiểu cho văn bản trong bong bóng chat */
    .stChatMessage .stMarkdown {
        font-family: sans-serif;
    }
    /* Tùy chỉnh màu của input và placeholder */
    .stChatInputContainer input {
        background-color: #BBDEFB; /* Màu xanh nhạt */
        color: #212121; /* Màu chữ xám đậm */
    }

    .stChatInputContainer input::placeholder {
        color: #757575; /* Màu chữ xám nhạt */

    }

    /*Tùy chỉnh màu send button */
    button.edg094p1 {
        background-color: green !important;
        border: 1px solid green;
        color: white;

    }.my-title {
        color: green;
    }



    </style>
    """,
    unsafe_allow_html=True,
)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

with st.sidebar:
    st.header("các chức năng")
    if st.button("bắt đầu cuộc trò truyện mới"):
        st.session_state.chat = model.start_chat(history=[]) # Khởi tạo lại chat ở đây
        st.rerun()  # Thêm lựa chọn ngôn ngữ
    
    

# Set up the chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Streamlit app title
st.markdown("<h1 class='my-title'>Storytelling Chatbot</h1>", unsafe_allow_html=True)

# Add a dropdown to choose the style of the story
story_style = st.selectbox(
    "Chọn phong cách kể chuyện:",
    ["Ngẫu nhiên","Hài hước", "Kinh dị", "Bí ẩn","thiếu nhi"]
)

# Display the current style
st.write(f"Storytelling style: {story_style}")

# Define prompt templates for different story styles
story_prompts = {
    "ngẫu nhiên":"kể cho tôi nghe một câu chuyện với phong cách ngẫu nhiên",
    "Hài hước": "Kể cho tôi nghe một câu chuyện vui khiến mọi người bật cười.",
    "Kinh dị": "Kể cho tôi nghe một câu chuyện rùng rợn và đáng sợ khiến mọi người rùng mình.",
    "Bí ẩn": "Kể cho tôi nghe một câu chuyện bí ẩn với tình tiết bất ngờ ở cuối.",
    "thiếu nhi":"kể cho tôi nghe một câu chuyện cho những đứa trẻ con"
    }


# Generate the correct prompt based on the user's choice
selected_prompt = story_prompts.get(story_style, "Hãy kể cho tôi một câu chuyện ")

# Show history of the conversation
if not st.session_state.chat.history:
    st.write("<p style='font-size: 25px;'>Hãy bắt đầu cuộc trò chuyện bằng cách nhập tin nhắn của bạn!</p>", unsafe_allow_html=True)

else: # Chỉ hiển thị lịch sử chat nếu có tin nhắn
    for message in st.session_state.chat.history:
        with st.chat_message(message.role):
            st.markdown(message.parts[0].text)

# User input for additional messages
user_input = st.chat_input("Hãy nhập chủ đề của bạn tại đây...")

if user_input:
    # Add user message to chat history
    st.chat_message("user").markdown(user_input)
    # Send the message to the model along with the style-specific prompt
    prompt_with_user_input = f"{selected_prompt} {user_input}"

    # Generate the response based on the user's message and the selected storytelling style
    response = st.session_state.chat.send_message(prompt_with_user_input)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response.text)
