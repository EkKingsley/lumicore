# app.py
import streamlit as st
import base64
import os
from pathlib import Path


def image_to_base64(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None


def replace_images_with_base64(html_content):
    """Replace image src attributes with base64 data URLs"""
    import re

    # Find all image tags in the HTML
    image_pattern = r'src="(images/[^"]+)"'
    matches = re.findall(image_pattern, html_content)

    for image_path in matches:
        base64_data = image_to_base64(image_path)
        if base64_data:
            # Get file extension
            ext = image_path.split('.')[-1].lower()
            mime_type = f"image/{ext}" if ext in ['jpg', 'jpeg', 'png', 'gif',
                                                  'bmp'] else f"image/{'jpeg' if ext == 'jpg' else ext}"

            # Replace the src with base64 data URL
            data_url = f"data:{mime_type};base64,{base64_data}"
            html_content = html_content.replace(f'src="{image_path}"', f'src="{data_url}"')

    return html_content


def render_html_file():
    # Read HTML file
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Replace image paths with base64 data URLs
    html_content = replace_images_with_base64(html_content)

    # Display with proper height and scrolling
    st.components.v1.html(
        html_content,
        height=4000,
        scrolling=True
    )


def main():
    st.set_page_config(
        page_title="LumiCore | Shopper Marketing & Retail Analytics",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Hide Streamlit default elements
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Render your HTML website
    render_html_file()


if __name__ == "__main__":
    main()