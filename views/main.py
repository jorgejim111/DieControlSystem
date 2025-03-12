from flask import Blueprint, render_template, jsonify
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('layouts/base.html')

@main_bp.route('/module/<module_name>')
@login_required
def load_module(module_name):
    try:
        return render_template(f'components/{module_name}.html')
    except:
        return 'Error al cargar el módulo', 404 