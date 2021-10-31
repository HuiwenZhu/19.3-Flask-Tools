from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session:
# put here as contants so we are guarenteed to be consistent in our spelling of these

app = Flask(__name__)

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def survey_start():
    """Start a survey"""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", method=["POST"])
def start_survey():
    """Clear the session of response"""
    session[RESPONSE_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", method=["POST"])
def handle_question():
    choice = request.form['answer']
    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(response)) == len(survey.question)):
        return redirect("/complete")
    else:
        return redirect(f"/question/{len(responses)}")

@ app.route("/questions/<int:qid>")
def show_question(qid):
    response=session.get(RESPONSE_KEY)

    if(response is None):
        return redirect("/")

   if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question=survey.questions[qid]
    return render_template(
        "question.html", question_num = qid, question = question)


@ app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")
