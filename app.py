import streamlit as st 
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi


from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


input_prompt=""" You are a professional youtube video summarizer, you will get transcript text and you will be generating a summary of the entire video in a proper point wise structure with proper headings, covering important points in not more than 250 words. The Transcript Text will be appended here :  """

def get_response(input_prompt, transcript):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt + transcript)
    return response.text

def gen_transcript(link):
    try:
        video_id = link.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']
        return transcript
    
    except Exception as e:
        raise e

st.set_page_config("Youtube Transcriber")

st.header("Youtube Transcriber")

link = st.text_input("Give me the link of video")

if link:
    video_id = link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

submit = st.button("Get Summary")


if submit:
    transcript = gen_transcript(link)
    response = get_response(input_prompt, transcript)
    st.subheader("Summary is:")
    st.write(response)