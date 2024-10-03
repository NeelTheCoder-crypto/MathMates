import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Original prompts dictionary integrated with specific sections
prompts = {
    "Math Concepts": {
        "Stack Multiplication": "Explain 3 digit by 2 digit multiplication with an example in simple 4th grader language",
        "Long Division": "Explain Long Division with an example in simple 4th grader language",
        "Fractions": "Explain Fractions with an example in simple 4th grader language",
        "Order of Operations": "Explain Order of Operations with an example in simple 4th grader language"
    },
    "Learn with Stories": {
        "Stack Multiplication": "Generate a story for a 4th grader to understand 3 digit by 2 digit multiplication.",
        "Long Division": "Generate a story for a 4th grader to understand Long Division",
        "Fractions": "Generate a story for a 4th grader to understand Fractions",
        "Order of Operations": "Generate a story for a 4th grader to understand Order of Operations"
    },
    "Real-Life Application": {
        "Stack Multiplication": "Explain a real-life application of 3 digit by 2 digit multiplication for a 4th grader",
        "Long Division": "Explain a real-life application of Long Division for a 4th grader",
        "Fractions": "Explain a real-life application of Fractions for a 4th grader",
        "Order of Operations": "Explain a real-life application of Order of Operations for a 4th grader"
    },
    "Practice Problems": { 

         "Stack Multiplication": "Generate a 3 digit by 2 digit multiplication problem for a 4th grader. Include:\n1. The problem statement\n2. The correct answer\n3. A step-by-step solution\n\nFormat your response as follows:\nProblem:\n[Your Problem Here]\n\nAnswer:\n[Correct Answer Here]\n\nSolution:\n[Step-by-step Solution Here]",
         "Long Divison": "Generate a Long Division problem for a 4th grader. Include:\n1. The problem statement\n2. The correct answer\n3. A step-by-step solution\n\nFormat your response as follows:\nProblem:\n[Your Problem Here]\n\nAnswer:\n[Correct Answer Here]\n\nSolution:\n[Step-by-step Solution Here]",
         "Fractions": "Generate a Fractions problem for a 4th grader. Include:\n1. The problem statement\n2. The correct answer\n3. A step-by-step solution\n\nFormat your response as follows:\nProblem:\n[Your Problem Here]\n\nAnswer:\n[Correct Answer Here]\n\nSolution:\n[Step-by-step Solution Here]",
        "Order of Operations": "Generate a Order of Operations problem for a 4th grader. Include:\n1. The problem statement\n2. The correct answer\n3. A step-by-step solution\n\nFormat your response as follows:\nProblem:\n[Your Problem Here]\n\nAnswer:\n[Correct Answer Here]\n\nSolution:\n[Step-by-step Solution Here]" 
        
        
    },
    "Tips & Tricks": {
        "Stack Multiplication": "Give some tips and tricks for 3 digit by 2 digit multiplication in simple 4th grader language",
        "Long Division": "Give some tips and tricks for Long Division in simple 4th grader language",
        "Fractions": "Give some tips and tricks for Fractions in simple 4th grader language",
        "Order of Operations": "Give some tips and tricks for Order of Operations in simple 4th grader language"
    }
}

# Initialize Langchain Model
model = ChatOpenAI(openai_api_key="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")

# Ensure session state for problem solutions is initialized
if 'problem_solutions' not in st.session_state:
    st.session_state.problem_solutions = {}

# Function to get problem, answer, and step-by-step solution
def get_problem_with_solution(problem_type):
    prompt_template = ChatPromptTemplate.from_template(prompts["Practice Problems"][problem_type])
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({})
    
    # Structured parsing based on the defined format
    problem_start = response.find("Problem:")
    answer_start = response.find("Answer:", problem_start)
    solution_start = response.find("Solution:", answer_start)
    
    problem = response[problem_start + len("Problem:"):answer_start].strip()
    answer = response[answer_start + len("Answer:"):solution_start].strip()
    solution = response[solution_start + len("Solution:"):].strip()
    
    return problem, answer, solution

def check_answer(user_answer, correct_answer):
    # Attempt to handle as numeric values to compare numbers accurately
    try:
        user_answer_numeric = float(user_answer.strip())
        correct_answer_numeric = float(correct_answer.strip())
        return "Correct!:)" if user_answer_numeric == correct_answer_numeric else "Incorrect"
    except ValueError:
        # Fallback to string comparison if not numeric
        # Case insensitive comparison for textual answers
        return "Correct!:)" if user_answer.strip().lower() == correct_answer.strip().lower() else "Incorrect"

def get_response(section, query, problem_type=None):
    if section in ["Math Concepts", "Tips & Tricks"]:
        prompt_template = ChatPromptTemplate.from_template(prompts[section][query])
    elif query == "solution":
        if problem_type == "Step-by-step Solution":
            # Retrieve the stored problem to generate a step-by-step solution
            generated_problem = st.session_state.problem_solutions.get("Generated Problem")
            if generated_problem:
                prompt_template = ChatPromptTemplate.from_template(prompts["Practice Problems"]["Step-by-step Solution"])
                prompt_template = prompt_template.format(generated_problem=generated_problem)
            else:
                return "Please generate a problem first."
        else:
            prompt_template = ChatPromptTemplate.from_template(prompts[section][problem_type])
    else:
        prompt_template = ChatPromptTemplate.from_template(prompts[section][query])
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({"foo": query})
    
    if query == "solution":
        # Extract the step-by-step solution from the response
        solution = response
        return solution
    else:
        return response
    
    
# Streamlit UI
st.title('MathMate for Fourth Graders')

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select a Page", ['Math Concepts', 'Learn with Stories', 'Real-Life Application', 'Practice Problems', 'Tips & Tricks'])

if page == 'Math Concepts': 
    concept_topic = st.selectbox("Choose a concept:", options=list(prompts["Math Concepts"].keys()))
    if st.button(f'Explain {concept_topic}'):
        explanation = get_response("Math Concepts", concept_topic)
        st.write(explanation)

elif page == 'Learn with Stories':
    story_topic = st.selectbox("Choose a story topic:", options=list(prompts["Learn with Stories"].keys()))
    if st.button(f'Tell Story about {story_topic}'):
        story = get_response("Learn with Stories", story_topic)
        st.write(story)

elif page == 'Real-Life Application':
    real_life_topic = st.selectbox("Choose a real-life application topic:", options=list(prompts["Real-Life Application"].keys()))
    if st.button(f'Explain real-life application of {real_life_topic}'):
        real_life_explanation = get_response("Real-Life Application", real_life_topic)
        st.write(real_life_explanation)

        
if page == 'Tips & Tricks': 
    tip_topic = st.selectbox("Choose a Tips & Tricks topic:", options=list(prompts["Tips & Tricks"].keys()))
    if st.button(f'Tips & Tricks for {tip_topic}'):
        explanation = get_response("Tips & Tricks", tip_topic)
        st.write(explanation)

# Handle Practice Problems section
if page == 'Practice Problems':
    st.header("Practice Problems")
    problem_type = st.selectbox("Choose a problem type:", options=list(prompts["Practice Problems"].keys()))
    
    if st.button('Generate New Problem'):
        problem, answer, solution = get_problem_with_solution(problem_type)
        
        # Store the generated problem, its answer, and solution
        st.session_state.problem_solutions[problem_type] = {'problem': problem, 'answer': answer, 'solution': solution}
        
        st.write("Problem:", problem)

    user_solution = st.text_input("Your Solution")

    if st.button('Check Answer') and problem_type in st.session_state.problem_solutions:
        correct_answer = st.session_state.problem_solutions[problem_type]['answer']
        result = check_answer(user_solution, correct_answer)
        st.write(f"Your Answer is: {result}")
        
        # Display the step-by-step solution regardless of the answer's correctness
        st.write("Step-by-step Solution:", st.session_state.problem_solutions[problem_type]['solution'])


        


