import streamlit as st
import pandas as pd
import io

# Load Excel from the same directory or remote path
@st.cache_data
def load_questions():
    xls = pd.ExcelFile("Dynamic leadership Inventory.xlsm")
    all_parts = []
    for i in range(1, 7):
        part_df = pd.read_excel(xls, sheet_name=f"PART {i}")
        part_df = part_df.dropna(subset=[part_df.columns[0], part_df.columns[1]])
        part_df = part_df[[part_df.columns[0], part_df.columns[1]]]
        part_df.columns = ['Q_No', 'Question']
        part_df['Part'] = f'PART {i}'
        all_parts.append(part_df)
    questions_df = pd.concat(all_parts, ignore_index=True)
    return questions_df

def get_leadership_styles():
    return {
        "Visionary/Authoritative": "You lead by painting a clear and inspiring vision...",
        "Coaching": "You focus on developing people and helping them grow...",
        "Affiliative": "You prioritize emotional bonds, team harmony...",
        "Democratic": "You lead by building consensus through participation...",
        "Pace-setting": "You set high standards and expect excellence...",
        "Commanding/Coercive": "You lead with clear authority and expect immediate compliance..."
    }

# --- STREAMLIT APP ---
st.set_page_config(page_title="Leadership Inventory", layout="centered")
st.title("🧭 Dynamic Leadership Inventory")

# --- USER INFO ---
name = st.text_input("Your Name")
email = st.text_input("Your Email")
password = st.text_input("Enter Access Password", type="password")

if password != "leader2024":
    st.warning("Please enter a valid password to begin.")
    st.stop()

questions_df = load_questions()
styles = get_leadership_styles()

st.markdown("---")
st.header("📋 Rate the Following Statements (1 = Strongly Disagree, 5 = Strongly Agree)")

responses = []

for index, row in questions_df.iterrows():
    score = st.slider(f"{int(row['Q_No'])}. {row['Question']}", 1, 5, 3)
    responses.append((row['Part'], score))

if st.button("Submit Exam"):
    # Score aggregation
    part_scores = {}
    for part, score in responses:
        part_scores[part] = part_scores.get(part, 0) + score

    # Dummy mapping of parts to styles (can customize)
    style_map = {
        "PART 1": "Visionary/Authoritative",
        "PART 2": "Coaching",
        "PART 3": "Affiliative",
        "PART 4": "Democratic",
        "PART 5": "Pace-setting",
        "PART 6": "Commanding/Coercive"
    }

    style_totals = {}
    for part, total in part_scores.items():
        style = style_map[part]
        style_totals[style] = style_totals.get(style, 0) + total

    # Determine top style
    final_style = max(style_totals, key=style_totals.get)
    description = styles[final_style]

    st.success(f"Your Leadership Style: {final_style}")
    st.write(description)

    # Result string
    result_text = f"Leadership Inventory Result\nName: {name}\nEmail: {email}\n\nYour Leadership Style: {final_style}\n\n{description}"

    # Download button
    st.download_button("📥 Download Your Result", result_text, file_name="leadership_result.txt")
