from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey, personality_quiz, surveys, curr_survey

RESPONSES = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Display the home page, survey title,"""

    return render_template('home.html', survey_title=curr_survey.title, survey_instructions=curr_survey.instructions)


@app.route('/setup', methods=["POST"])
def set_up_responses():
    """Sets session to an empty list"""

    session[RESPONSES] = []

    return redirect("/questions/0")


@app.route('/answer', methods=['POST'])
def question_answer():
    """Handles accepting answers"""
    
    #get the choice
    choice = request.form['choice']

    try:
        responses = session[RESPONSES]
        responses.append([choice, request.form['why']])
        session[RESPONSES] = responses
    except KeyError:
        responses = session[RESPONSES]
        responses.append(choice)
        session[RESPONSES] = responses

    if len(responses) == len(curr_survey.questions):
        #all questions have been answered
        return redirect('/thanks')
        
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:number>')
def question_page(number):
    """Display a question page"""
    responses = session.get(RESPONSES)

    if (responses is None):
        #if trying to access questions before the start
        return redirect("/")

    if (len(responses) == len(curr_survey.questions)):
        #all questions have been answered
        return redirect("/thanks")
        
    if (len(responses) != number):
        #trying to get to questions out of order
        flash(f"You're trying to access an invalid question")
        return redirect(f"/questions/{len(responses)}")
        
    question = curr_survey.questions[number]
    return render_template('question.html', question=question.question, num=number + 1, answers=question.choices, allowstext = question.allow_text)


@app.route('/thanks')
def thank_you():
    """Thank you page"""
    return render_template('thanks.html')