from flask import *
from resume_comparison import DocComparision as dc
import os

app = Flask(__name__)


PATH = os.path.normpath(os.getcwd()+os.sep+os.pardir)
print(os.getcwd())

@app.route("/", methods=["POST", "GET"])
def resume_match():
    if request.method == 'POST':
        file = request.form["resume"]
        try:
            resume_file = PATH+"/Resumes/"+file
        except:
            resume_file = PATH+"/Resumes/"+file
        description = PATH+"/Job_Description/"+request.form["description"]
        res = dc(resume_file, description).result
        return render_template("resume_comparison_result.html", data=res)
    else:
        return render_template("resume_comparison.html")


if __name__ == "__main__":

    app.run(host="localhost", debug=True, port=5000)