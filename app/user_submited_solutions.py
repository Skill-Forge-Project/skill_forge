from flask import Blueprint, render_template
from flask_login import login_required
# Import models
from app.models import SubmitedSolution

bp_uss = Blueprint('uss', __name__)

# Route to handle the view solution page.
@login_required
@bp_uss.route('/view_solution/<solution_id>', methods=['GET'])
def open_view_solution(solution_id):
    
    # Get the user's desired solution based on the solution_id
    user_solved_quest = SubmitedSolution.query.filter_by(submission_id=solution_id).first()


    return render_template('view_solution.html', user_solved_quest=user_solved_quest)