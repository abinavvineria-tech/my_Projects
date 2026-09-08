from flask import Blueprint
bp = Blueprint('api', __name__)
@bp.route('/health')
def health(): return {'status':'ok'}
