from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def root_route():
    """ Render the start page for the survey, passing in
        title and instructions from global survey object.
    """

    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions)

@app.post("/begin")
def begin_survey_route():
    """ POST route for starting survey.

        Clears any existing responses and starts survey at question 0.
    """
    session["responses"] = []
    return redirect("/questions/0")


@app.get("/questions/<int:q_number>")
def survey_question(q_number):
    """ Render a single survey question on a page.
    """
    responses_length = len(session["responses"])
    if responses_length == len(survey.questions):
        return redirect(f"/completion")
    elif responses_length != q_number:
        return redirect(f"/questions/{responses_length}")
    else:
        return render_template(
            "question.html",
            question=survey.questions[q_number]
    )

@app.post("/answer")
def answer_route():
    """ POST route that:
        - Records the answer given to an individual question
        - Checks if question number < num of survey questions
            - If yes, redirect to next survey question
            - If no, redirect to thank you page
    """
    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses
    q_number = len(responses)

    if q_number < len(survey.questions):
        return redirect(f"/questions/{q_number}")

    else:
        return redirect("/completion")

@app.get("/completion")
def thank_you():
    """ Render thank you confirmation page to confirm survey has been
        successfully received.

        Show a list of survey questions and user's responses.
    """

    recap = zip(survey.questions, session["responses"])

    return render_template(
        "completion.html",
        recap=recap
    )



# request.form["comment"]

# debugger pin: 114-386-609