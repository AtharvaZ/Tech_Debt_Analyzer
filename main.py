import streamlit as st
from analyzer.ruff_analyzer import analyze_ruff
from analyzer.radon_analyzer import analyze_radon
from analyzer.bandit_analyzer import analyze_bandit

import os
import shutil

#set page title
st.title("Technical Debt Analyzer")

#file uploader to upload files
uploaded_files = st.file_uploader(
    "Upload Python files from your folder",
    type=["py"],
    accept_multiple_files=True
)
files_to_analyze = uploaded_files
st.warning("Only upload python/.py files")

#create button to upload the file(s) selected
if files_to_analyze and st.button("Upload"):

    #make a temporary folder to make a copy all the selected files
    #this is done so that we can pass a OS.Path to the libraries used
    temp_dir = "temp_uploads"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    #saving paths to all the files in the form of a list
    #pass the list of paths as an argument to the linter functions
    saved_paths = []
    for file in files_to_analyze:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        saved_paths.append(file_path)

    st.success(f"{len(saved_paths)} file(s) uploaded successfully.")

    #get the results using the linter funcitons 
    ruff_result = analyze_ruff(saved_paths if saved_paths else st.error("File Not Found"))
    radon_result = analyze_radon(saved_paths if saved_paths else st.error("File Not Found"))
    bandit_result = analyze_bandit(saved_paths if saved_paths else st.error("File Not Found"))

    #make sessinons states to save the results received from the linter functions
    st.session_state["ruff_result"] = ruff_result
    st.session_state["radon_result"] = radon_result
    st.session_state["bandit_result"] = bandit_result

    #only show the report button after getting the results
    st.session_state["show_report_button"] = True
    st.session_state["full_ruff_report"] = False
    st.session_state["full_radon_report"] = False
    st.session_state["full_bandit_report"] = False

#make 2 buttons to show results from 2 linter functions
#and the set the corresponding session state report to True to display it on clicking
if st.session_state.get("show_report_button"):
    col1, col2, col3 = st.columns(3)

    #col1 containing button for ruff results
    with col1:
        if st.button("Ruff Report"):
            st.session_state["full_ruff_report"] = True
            st.session_state["full_radon_report"] = False
            st.session_state["full_bandit_report"] = False

    #col2 containing button for radon results
    with col2:
        if st.button("Radon Report"):
            st.session_state["full_radon_report"] = True
            st.session_state["full_ruff_report"] = False
            st.session_state["full_bandit_report"] = False
    
    #col3 containing button for bandit results
    with col3:
        if st.button("Bandit Report"):
            st.session_state["full_bandit_report"] = True
            st.session_state["full_radon_report"] = False
            st.session_state["full_ruff_report"] = False

#get ruff report from session state when Ruff report button is clicked
if st.session_state.get("full_ruff_report"):
    st.subheader("Ruff Analyzer Report")
    st.code(st.session_state.get("ruff_result", ""), language="text")

#get radon report from session state when Radon report button is clicked
if st.session_state.get("full_radon_report"):
    st.subheader("Radon Analyzer Report")
    st.code(st.session_state.get("radon_result", ""), language="text")

#get bandit report from session state when Bandit report button is clicked
if st.session_state.get("full_bandit_report"):
    st.subheader("Bandit Analyzer Report")
    st.code(st.session_state.get("bandit_result", ""), language="text")


def get_ruff_error_count(output: str) -> int:
    for line in reversed(output.strip().splitlines()):
        if line.startswith("Found ") and "error" in line:
            try:
                return int(line.split()[1])
            except (IndexError, ValueError):
                return 0
    return 0









        
