from . import models
from . import wizards

def _pre_init_update_rule(cr):
    cr.execute("""update ir_model_data set noupdate=False where model = 'hr.salary.rule'""")