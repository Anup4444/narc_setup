from wtforms import SelectField, StringField, SubmitField
from flask_wtf import FlaskForm
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from setup.dbsetup import db
from models.db_update import *

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


class EditOptionsForm(FlaskForm):
    select_option = SelectField('Select an option')
    new_option = StringField('Add a new option')
    submit = SubmitField('Submit')


admin_blueprint = Blueprint('admin', __name__)

models_map = {
    'host': Host,
    'diagnostictest': DiagnosticTest,
    'suspectedproblem': SuspectedProblem,
    'samplematerialssubmitted': SampleMaterialsSubmitted,
    # add other models here
}


@admin_blueprint.route('/<model_name>/form')
@admin_blueprint.route('/')
def form(model_name=None):  # Set default value for model_name
    host_list = []
    DiagnosticTest_list = []
    suspectProblem_list = []
    SampleMaterialsSubmittedData_list = []

    if model_name:
        model = models_map.get(model_name)
        if not model:
            flash('Invalid model name provided.')
            # Redirect to a suitable error page or index
            return redirect(url_for('index'))

        if model_name == "host":
            host_list = model.search({"status": 1})
        elif model_name == "diagnostictest":
            DiagnosticTest_list = model.search({"status": 1})
        elif model_name == "suspectedproblem":
            suspectProblem_list = model.search({"status": 1})
        elif model_name == "samplematerialssubmitted":
            SampleMaterialsSubmittedData_list = model.search({"status": 1})
    else:
        # Get both lists if no specific model is provided
        host_list = models_map["host"].search({"status": 1})
        DiagnosticTest_list = models_map["diagnostictest"].search({
                                                                  "status": 1})
        suspectProblem_list = models_map["suspectedproblem"].search({
            "status": 1})
        SampleMaterialsSubmittedData_list = models_map["samplematerialssubmitted"].search({
            "status": 1})

    return render_template('admin.html', host_list=host_list, DiagnosticTest_list=DiagnosticTest_list, suspectProblem_list=suspectProblem_list, SampleMaterialsSubmittedData_list=SampleMaterialsSubmittedData_list)


@admin_blueprint.route('/<model_name>', methods=['POST'])
def crud(model_name):
    datas = request.json
    model = models_map.get(model_name)

    if not model:
        return jsonify({"status_code": 0, "status": f"Invalid model: {model_name}"}), 400

    # Map action to corresponding function
    actions = {
        'edit': update_value,
        'del': delete_record,
        'add': add_new_record
    }

    action_function = actions.get(datas["type"])

    if action_function:
        return action_function(datas, model)
    else:
        return jsonify({"status_code": 0, "status": f"Invalid action: {datas['type']}"}), 400


def update_value(datas, model):
    try:
        filter = {"id": int(datas["id"])}
        para = {"value": datas["value"]}
        model.update(filter, para)
        return jsonify({"status_code": 1, "status": "Update successful"})
    except Exception as e:
        return jsonify({"status_code": 0, "status": f"Update failed: {str(e)}"}), 400


def delete_record(datas, model):
    try:
        filter = {"id": int(datas["id"])}
        para = {"status": 0}
        model.update(filter, para)
        return jsonify({"status_code": 1, "status": "Delete successful"})
    except Exception as e:
        return jsonify({"status_code": 0, "status": f"Delete failed: {str(e)}"}), 400


def add_new_record(datas, model):
    try:
        data = {"value": datas["value"], "status": 1}
        new_record = model.addData(data)
        data['id'] = new_record.id
        return jsonify({"status_code": 1, "status": "Add successful", "data": data})
    except Exception as e:
        return jsonify({"status_code": 0, "status": f"Add failed: {str(e)}"}), 400
