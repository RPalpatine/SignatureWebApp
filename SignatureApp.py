import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from streamlit_cropper import st_cropper


st.title("Make your own digital signature")
st.write("Upload image of your signature")
img_file = st.file_uploader("Image file has to be either 'jpg', 'jpeg', or 'png'", type=['jpg', 'jpeg', 'png'])
camera_file = None
select_camera = st.checkbox("Select to take a photo from your camera", value = False)
if select_camera:
    camera_file = st.camera_input("Photo of your signature")

realtime_update = st.checkbox(label="Update in Real Time", value=True)

def signature(img, selected, block_size = 25, choose_c = 10.0, thr = 127):
    sig_cr = img[:, :, ::1]
    sig_gs = cv2.cvtColor(sig_cr, 6)
    if selected == "Binary":
        revlt, sig_MASK = cv2.threshold(sig_gs, thr, 255, cv2.THRESH_BINARY_INV)
        bc, gc, rc = cv2.split(sig_cr)
        new_sig = [gc, bc, rc, sig_MASK]
        new_sig_merged = cv2.merge(new_sig, 4)
    else:
        sig_adaptive = cv2.adaptiveThreshold(sig_gs, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, choose_c)
        bc, gc, rc = cv2.split(sig_cr)
        new_sig = [gc, bc, rc, sig_adaptive]
        new_sig_merged = cv2.merge(new_sig, 4)
    return new_sig_merged[:, :, ::1]

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


if img_file:
    img = Image.open(img_file)
    if not realtime_update:
        st.write("Double click to save crop")
        # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=realtime_update)
    st.write("Input")
    _ = cropped_img.thumbnail((500, 500))
    st.image(cropped_img)
    cvt_img = np.array(cropped_img)
    save_it = st.checkbox(label="Press when finished with cropping", value=False)
    if save_it:
        select_thr = st.selectbox("Choose thresholding method", ["Binary", "Adaptive"])
        if select_thr == "Binary":
            thr = st.slider("Choose threshold value", 0, 255, step=1, value=127)
            cvt_img_res = signature(cvt_img, select_thr, thr = thr)
        else:
            block_size = st.slider("Choose block size value", 1, 51, step=2, value=25)
            choose_c = st.slider("Choose C value", -15.0, 50.0, step = 0.1, value = 16.0)
            cvt_img_res = signature(cvt_img, select_thr, block_size, choose_c)
        st.write("Output")
        st.image(cvt_img_res, width=500)
        out_image = Image.fromarray(cvt_img_res[:, :, ::1])
        st.markdown(get_image_download_link(out_image, "your_signature.png", 'Download Output Image'),
                    unsafe_allow_html=True)
elif camera_file:
    img = Image.open(camera_file)
    st.write(type(img))
    if not realtime_update:
        st.write("Double click to save crop")
        # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=realtime_update)
    st.write("Input")
    _ = cropped_img.thumbnail((500, 500))
    st.image(cropped_img)
    st.write(type(cropped_img))
    cvt_img = np.array(cropped_img)
    st.write(type(cvt_img))
    save_it = st.checkbox(label="Press when finished with cropping", value=False)
    if save_it:
        select_thr = st.selectbox("Choose thresholding method", ["Binary", "Adaptive"])
        if select_thr == "Binary":
            thr = st.slider("Choose threshold value", 0, 255, step=1, value=127)
            cvt_img_res = signature(cvt_img, select_thr, thr = thr)
        else:
            block_size = st.slider("Choose block size value", 1, 51, step=2, value=25)
            choose_c = st.slider("Choose C value", -15.0, 50.0, step = 0.1, value = 16.0)
            cvt_img_res = signature(cvt_img, select_thr, block_size, choose_c)
        st.write("Output")
        st.image(cvt_img_res, width=500)
        out_image = Image.fromarray(cvt_img_res[:, :, ::1])
        st.markdown(get_image_download_link(out_image, "your_signature.png", 'Download Output Image'),
                    unsafe_allow_html=True)
