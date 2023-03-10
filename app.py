from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

# root route
# renders title, instructions, button start survey
#   Button action will eventually take user to /questions/0 (rn form action
#   takes user to /begin)
@app.get("/")
def root_route():
    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions)

# POST reroute survey_start form from /begin to /questions/0
#   /questions/<q_number>
#   either hardcode on length of responses, or future cookies?
@app.post("/begin")
def begin_survey_route():
    q_number = len(responses)
    return redirect(f"/questions/{q_number}")

# GET request for updated /questions/0 page
#   render the question.html jinja template
@app.get("/questions/<int:q_number>")
def survey_question(q_number):

    return render_template(
        "question.html",
        question=survey.questions[q_number],
        q_number=q_number
    )

# POST route for /answer
#   record answer in responses
#   take user to next question by input of question
#   return parameter of q_number of next question
#   return redirect("/questions/<q_number>")
@app.post("/answer")
def answer_route():

    global responses
    responses.append(request.form["answer"])

    q_number = int(request.form["index"])
    q_number += 1

    if q_number < len(survey.questions):
        # route to next quesiton
        return redirect(f"/questions/{q_number}")
    else:
        # redirect to thank you page
        return redirect("/completion")

@app.get("/completion")
def thank_you():

    recap = zip(survey.questions, responses)

    return render_template(
        "completion.html",
        recap=recap
    )



# request.form["comment"]

# debugger pin: 114-386-609