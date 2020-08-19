from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey, personality_quiz, surveys, curr_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    """Display the home page, survey title,"""
    return render_template('home.html', survey_title=curr_survey.title, survey_instructions=curr_survey.instructions)

@app.route('/questions/<number>')
def question_page(number):
    """Display a question page"""
    q_number = int(number)

    # """If the survey is complete, redirect to a thank you page"""
    if len(responses) == len(curr_survey.questions):
        return redirect("/thanks")
    # """The correct page # will load the correct question"""
    elif q_number == len(responses):
        question = curr_survey.questions[q_number]
        return render_template('question.html', question=question.question, num=q_number + 1, answers=question.choices, allowstext = question.allow_text)
    else:
        flash("You're trying to access an invalid question")
        return redirect(f"/questions/{len(responses)}")

@app.route('/answer', methods=['POST'])
def question_answer():
    """Handles accepting answers"""
    
    choice = request.form['choice']

    try:
        responses.append([choice, request.form['why']])
    except KeyError:
        responses.append(choice)

    count = len(responses)
    if count < len(curr_survey.questions):
        return redirect(f"/questions/{count}")
    else:
        return redirect('/thanks')

@app.route('/thanks')
def thank_you():
    """Thank you page"""
    return render_template('thanks.html')