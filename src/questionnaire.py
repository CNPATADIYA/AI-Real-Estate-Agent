import streamlit as st

# Set page title
st.title("Kindly answer following questions")

st.subheader("Let AI find best property for you !")

# Define MCQs (Question, Options, Correct Answer)
questions = [
    {
        "type": "radio",
        "question": "Which City are you finding the house?",
        "options": ["Ahmedabad", "Mumbai", "Bangalore", "Delhi"],
        "answer": "Ahmedabad"
    },
    {
        "type": "radio",
        "question": "How confident are you in your understanding of real estate buying?",
        "options": ["Very Confident - I have done my research", "Somewhat Confident - I know the basics", "Not Confident - I need expert guidance"],
        "answer": "Very Confident - I have done my research"
    },
    {
        "type": "radio",
        "question": "Your Occupation?",
        "options": ["Salaried", "Self-employed/Business Owner", "Retired", "Student", "Other"],
        "answer": "Salaried"
    },
    {
        "type": "radio",
        "question": "What is your Monthly Income Range?",
        "options": ["< ₹50,000", "₹50,000 - ₹1,00,000", "₹1,00,000 - ₹3,00,000", "₹3,00,000+"],
        "answer": "₹50,000 - ₹1,00,000"
    },
    {
        "type": "radio",
        "question": "What is the main reason for purchasing a property?",
        "options": ["First home", "Upgrade to a better home", "Investment", "Vacation home", "Retirement home", "Other"],
        "answer": "First home"
    },
    {
        "type": "radio",
        "question": "How soon are you looking to buy?",
        "options": ["Urgent (0-3 months)", "In 6 months", "In 1 year", "Less than 3 year", "Okay after 3 years"],
        "answer": "In 1 year"
    },
    {
        "type": "radio",
        "question": "Are you open to resale properties, or do you prefer new construction? ",
        "options": ["Only New Construction", "Only Resale", "Open to Both New and Resale properties"],
        "answer": "Only New Constructio"
    },
    {
        "type": "Multi-Select",
        "question": "What type of property are you looking for?",
        "options": ["Apartment", "Villa", "Independent House", "Plot"],
        "answer": ""
    },
    {
        "type": "Multi-Select",
        "question": "Preferred Configuration (For residential)",
        "options": ["1 BHK", "2 BHK", "3 BHK", "4 BHK"],
        "answer": "1 BHK"
    },
    {
        "type": "pills",
        "question": "Preferred Location(s)",
        "options": ["Shela", "Shilaj", "Bopal", "South Bopal", "Vaishno Devi", "Lambha", "SG Highway", "Hanspura", "Hathijan", "Chandkheda", "Ognaj", "Zundal", "Gota", "Thaltej"],
        "answer": ""
    },
    {
        "type": "radio",
        "question": "Distance from Workplace/School Important?",
        "options": ["Yes, workplace/school should be within nearby area", "No specific preference"],
        "answer": "No specific preference"
    },
    {
        "type": "radio",
        "question": "What is your total budget for this purchase?",
        "options": ["< ₹50 Lakhs", "₹50L - ₹1Cr", "₹1Cr - ₹2Cr", "₹2Cr+"],
        "answer": "₹50L - ₹1Cr"
    },
    {
        "type": "radio",
        "question": "Are you planning to take a home loan?",
        "options": ["Yes, Need Loan Assistance", "Yes, Have Pre-Approved Loan", "No, Self-Funded"],
        "answer": "Yes, Need Loan Assistance"
    },
    {
        "type": "radio",
        "question": "What EMI range are you comfortable with (If Loan Required)?",
        "options": ["< ₹25,000", "₹25,000 - ₹50,000", "₹50,000 - ₹1,00,000", "₹1,00,000+"],
        "answer": "₹50,000 - ₹1,00,000"
    },
    {
        "type": "Multi-Select",
        "question": "What concerns you the most about buying a property?",
        "options": ["Price fluctuations", "Legal issues/title verification", "Builder credibility", "Loan approval process", "Other"],
        "answer": "What concerns you the most about buying a property?"
    },
    {
        "type": "radio",
        "question": "Are you looking for future appreciation or rental income?",
        "options": ["Yes, Investment is a key factor", "No, I am buying for self-use only"],
        "answer": ""
    },
    {
        "type": "radio",
        "question": "What kind of neighbourhood do you prefer?",
        "options": ["Quiet & Residential", "Lively & Close to Markets", "Close to Business/IT Parks", "Close to Schools & Hospitals", "Other"],
        "answer": ""
    },
    {
        "type": "radio",
        "question": "What is the primary emotion driving this purchase?",
        "options": ["Security (I want a stable, safe home)", "Prestige (I want a better lifestyle/luxury property)", "Investment (I want wealth creation & passive income)", "Stability (I want to stop renting and own a home)", "Retirement (I want a home to settle down in my later years)"],
        "answer": ""
    },
    {
        "type": "Multi-Select",
        "question": "Are you planning any major life changes in the next 5 years?",
        "options": ["Marriage", "Having Kids", "Job Change / Transfer", "Moving Abroad", "Retirement", "Nothing"],
        "answer": ""
    },
    {
        "type": "Multi-Select",
        "question": "What are your deal-breakers? (Things you absolutely can’t compromise on)",
        "options": ["High Maintenance Costs", "Lack of Natural Light", "Small Room Sizes", "Parking Issues", "No Public Transport Nearby", "Builder Reputation"],
        "answer": ""
    }
]

# Initialize session state for answers if not already set
if "answers" not in st.session_state:
    st.session_state.answers = {}
    st.session_state.answers_ready = False

# Variable to track if all fields are answered
all_answered = True

# Display questions with numbering
for idx, q in enumerate(questions, start=1):  # start=1 ensures numbering starts from 1
    #st.subheader(f"Q{idx}: {q['question']}")  # Numbered question
    #question_markdown = st.markdown(f"## **Q{idx}: {q['question']}**")
    if q["type"] == "radio":
        user_answer = st.radio(f"**Q{idx}: {q['question']}**", q["options"], index=0, key=f"q{idx}")
    elif q["type"] == "Multi-Select":
        user_answer = st.multiselect(f"**Q{idx}: {q['question']}**", q["options"]) 
    elif q["type"] == "pills":
        user_answer = st.pills(f"**Q{idx}: {q['question']}**", q["options"], selection_mode="multi")
    if user_answer and (user_answer == "Other" or "Other" in  user_answer):
        other_text = st.text_input("**Please specify here:**", key=f"other_q{idx}")
        if not other_text:  # Ensure text input is filled
            all_answered = False
        st.session_state.answers[f"q{idx}"] = {"Question": q['question'], "Answer": other_text}  # Store text input
    else:
        st.session_state.answers[f"q{idx}"] = {"Question": q['question'], "Answer": user_answer}  # Store selected option
    
    # Check if the question is unanswered
    if not st.session_state.answers[f"q{idx}"]:
        all_answered = False
    st.write("---")  # Separator between questions

if st.button("Submit Answer"):
    if all_answered:
        st.session_state.answers_ready = True
        st.success(f"✅ Your response stored successfully please ask you questions to chatbot")
        st.switch_page("advisor.py")


    else:
        st.error("❌ Please answer all questions before submitting!")

    