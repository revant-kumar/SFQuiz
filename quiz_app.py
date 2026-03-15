import streamlit as st
import sqlite3

conn = sqlite3.connect("questions.db", check_same_thread=False)
cursor = conn.cursor()

st.title("SnowPro Core Practice")

mode = st.sidebar.selectbox(
    "Mode",
    ["Practice Mode", "Exam Mode"]
)

# -------------------------
# Fetch Questions
# -------------------------

if mode == "Practice Mode":

    page = st.sidebar.number_input("Page", 1, 20, 1)

    limit = 100
    offset = (page - 1) * limit

    questions = cursor.execute(
        "SELECT * FROM questions LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall()

else:

    questions = cursor.execute(
        "SELECT * FROM questions ORDER BY RANDOM() LIMIT 50"
    ).fetchall()

# -------------------------
# Display Questions
# -------------------------

for i, q in enumerate(questions):

    qid = q[0]
    qtext = q[1]
    num_correct = q[2]

    st.subheader(f"{qtext}")

    options = cursor.execute(
        """
        SELECT option_letter, option_text, is_correct
        FROM options
        WHERE question_id=?
        """,
        (qid,)
    ).fetchall()

    labels = [f"{o[0]}. {o[1]}" for o in options]

    correct_letters = [o[0] for o in options if o[2] == 1]

    # Each question gets its own form
    with st.form(key=f"form_{qid}"):

        if num_correct == 1:

            user_answer = st.radio(
                "Select answer",
                labels
            )

            selected = [user_answer[0]]

        else:

            user_answer = st.multiselect(
                f"Select {num_correct} answers",
                labels
            )

            selected = [a[0] for a in user_answer]

        submit = st.form_submit_button("Submit Answer")

    # -------------------------
    # Evaluate Answer
    # -------------------------

    if submit:

        if sorted(selected) == sorted(correct_letters):

            st.success("Correct!")

        else:

            st.error("Incorrect")

        st.write("Correct answer(s):")

        for o in options:
            if o[2] == 1:
                st.write(f"{o[0]}. {o[1]}")

    st.markdown("---")