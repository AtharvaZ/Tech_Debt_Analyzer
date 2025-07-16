import streamlit as st
from analyzer.ruff_analyzer import analyze_ruff
from analyzer.radon_analyzer import analyze_radon
from analyzer.bandit_analyzer import analyze_bandit

import os
import shutil

if "page" not in st.session_state:
    st.session_state.page = "home"

col1, col2, col3 = st.columns(3)    
with col1:
    if st.button("Home"):
        st.session_state.page = "home"
with col2:
    if st.button("Raw Analysis"):
        st.session_state.page = "raw_analysis"
with col3:
    if st.button("Raw report"):
        st.session_state.page = "debt_report"

#----------------------------------------------------------------------------------------------------------#
if st.session_state.page == "home":
#set page title
    st.title("Technical Debt Analyzer")

    #file uploader to upload files
    uploaded_files = st.file_uploader(
        "Upload Python files from your folder",
        type=["py"],
        accept_multiple_files=True
    )
    if st.button("Upload Files"):
        if uploaded_files:
            st.session_state.files_to_analyze = uploaded_files
            st.success("File(s) successfully uploaded!")

    st.warning("Only upload python/.py files")

    if "files_to_analyze" in st.session_state and st.session_state.files_to_analyze:
            temp_dir = "temp_uploads"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir, exist_ok=True)

            saved_paths = []
            for file in st.session_state.files_to_analyze:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())
                saved_paths.append(file_path)
            
            #get the results using the linter funcitons 
            ruff_result = analyze_ruff(saved_paths if saved_paths else st.error("File Not Found"))
            radon_result = analyze_radon(saved_paths if saved_paths else st.error("File Not Found"), "mi")
            bandit_result = analyze_bandit(saved_paths if saved_paths else st.error("File Not Found"))

            #make sessinons states to save the results received from the linter functions
            st.session_state["ruff_result"] = ruff_result
            st.session_state["radon_result"] = radon_result
            st.session_state["bandit_result"] = bandit_result

            st.success("Analysis complete. Go to Debt Analysis Page to see raw analysis.")

#----------------------------------------------------------------------------------------------------------#
if st.session_state.page == "raw_analysis":
    st.title("🧮 Debt Analysis")

    if not all(key in st.session_state for key in ["ruff_result", "bandit_result", "radon_result"]):
        st.warning("No analysis found. Please run the analysis from the Home or Analyze page.")
    else:
        # RUFF Report
        with st.expander("🐍 Ruff - Linting & Style Warnings", expanded=True):
            st.markdown("Ruff highlights PEP8 and other static analysis violations.")
            st.code(st.session_state.ruff_result, language="text")

        # BANDIT Report
        with st.expander("🛡️ Bandit - Security Analysis", expanded=True):
            st.markdown("Bandit checks for common security issues like use of `eval`, hardcoded credentials, etc.")

            try:
                import json
                bandit_data = json.loads(st.session_state.bandit_result)
                results = bandit_data.get("results", [])

                if not results:
                    st.success("✅ No security issues found by Bandit.")
                else:
                    for issue in results:
                        severity = issue["issue_severity"]
                        confidence = issue["issue_confidence"]
                        msg = issue["issue_text"]
                        line = issue["line_number"]
                        file = issue["filename"]

                        color = {"LOW": "green", "MEDIUM": "orange", "HIGH": "red"}.get(severity, "black")
                        st.markdown(
                            f"<div style='color:{color};'><strong>{severity}</strong> ({confidence}) — Line {line} in `{file}`: {msg}</div>",
                            unsafe_allow_html=True
                        )
            except Exception:
                st.error("⚠️ Failed to parse Bandit report.")
                st.code(st.session_state.bandit_result, language="json")
        # RADON Report
        with st.expander("📊 Radon - Maintainability & Complexity", expanded=True):
            st.markdown("""
            Radon shows the maintainability index (MI) and complexity of your code:
            - **MI > 85**: Excellent
            - **70 < MI < 85**: Good
            - **< 70**: Poor
            """)
            st.code(st.session_state.radon_result, language="text")

#----------------------------------------------------------------------------------------------------------#
if st.session_state.page == "debt_report":
    st.write("Helloooo")




def get_ruff_error_count(output: str) -> int:
    for line in reversed(output.strip().splitlines()):
        if line.startswith("Found ") and "error" in line:
            try:
                return int(line.split()[1])
            except (IndexError, ValueError):
                return 0
    return 0









        
