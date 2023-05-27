
from flask import render_template, request, Flask, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey



app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"
# responses = ['Yes', 'No', 'Less than $10,000', 'Yes']


@app.route("/Survey")
def do_survey():
    """Generate and show the survey."""
    survey1 = survey
    return render_template("select_survey.html", survey=survey1)


# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these

@app.route("/start", methods=["GET"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []
    
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def answer_question():
    """response is saved and redirected to the next question."""

    # request the response choice
    choice = request.form['answer']

    # adding the response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # Thanking them, when all questions are answered.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def display_question(qid):
    """showing current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
       #if question page is accessed too soon
        return redirect("/Survey")

    if (len(responses) == len(survey.questions)):
        # Thanking them, if all questions are answered.
        return redirect("/complete")

    if (len(responses) != qid):
        # not accessing the questions orderly.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "ans_quest.html", question_num=qid, question=question)



@app.route("/complete")
def complete():
    """Survey is completed."""

    return render_template("complete.html")