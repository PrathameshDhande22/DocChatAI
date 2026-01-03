from pathlib import Path
import streamlit as st


@st.dialog("About")
def show_info():
    with st.container(horizontal=True, horizontal_alignment="center"):
        st.image(
            image=Path.cwd().joinpath("Images").joinpath("imageicon.png"),
            caption="DocChat AI",
            width=100,
        )
        st.markdown(
            "The **DocChat AI** is a web-based application built using **_Streamlit_** and _**LangChain**_ that allows users to upload one or more PDF documents and interact with them using natural language queries.",
            text_alignment="justify",
        )

    st.markdown(
        "**Created By:** Prathamesh Dhande </br> **Contact:** prathameshdhande534@gmail.com",
        unsafe_allow_html=True,
    )
