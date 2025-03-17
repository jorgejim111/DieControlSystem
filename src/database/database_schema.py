"""
Este módulo contiene las definiciones del esquema de la base de datos Masternet.
Incluye nombres de tablas, columnas y relaciones para facilitar el desarrollo.
"""

# Nombres de las tablas
class Tables:
    POSITIONS = 'Positions'
    WORKERS = 'Workers'
    USER = 'user'
    ROLES = 'Rols'
    ROLES_USER = 'Roles_User'
    INCHES = 'Inches'
    DESCRIPTION = 'Description'
    PARTS = 'Parts'
    DIE_DESCRIPTION = 'Die_Description'
    STATUS_SERIAL = 'Status_Seril'
    SERIALS = 'Serials'
    LINE = 'Line'
    PRODUCTS = 'Products'
    DR_DESCRIPTION = 'DR_Description'
    EXPLANATION = 'Explanetion'
    DR_STATUS = 'DR_Status'
    DAMAGE_REPORT = 'Damage_Report'

# Columnas principales por tabla
class Columns:
    class Positions:
        ID = 'id_positions'
        POSITION = 'Position'

    class Workers:
        ID = 'idWorkers'
        NAME = 'Name'
        POSITION_ID = 'id_position'
        CREATE_TIME = 'create_time'

    class Users:
        ID = 'id_user'
        USERNAME = 'username'
        EMAIL = 'email'
        PASSWORD = 'password'
        WORKER_ID = 'id_worker'
        CREATE_TIME = 'create_time'

    class Roles:
        ID = 'id_rol'
        ROLE = 'Rol'

    class RolesUser:
        ID = 'id_roles_user'
        ROLE_ID = 'id_rol'
        USER_ID = 'id_user'

    class DieDescription:
        ID = 'id_die_description'
        INCH_ID = 'id_inch'
        PART_ID = 'id_part'
        DESCRIPTION_ID = 'id_description'
        DIE_DESCRIPTION = 'Die_Description'
        OBSOLETE = 'Obsolet'
        CIRCULATION = 'Circulation'
        NEW = 'New'
        CREATE_TIME = 'create_time'
        UPDATE_TIME = 'updat_time'

    class DRDescription:
        ID = 'id_dr_description'
        DESCRIPTION = 'description'

    class Explanation:
        ID = 'id_explanetion'
        EXPLANATION = 'explanetion'

    class DRStatus:
        ID = 'id_dr_status'
        STATUS = 'Status'

    class Serials:
        ID = 'id_serial'
        SERIAL = 'Serial'
        DIE_DESCRIPTION_ID = 'id_die_description'
        INNER = 'inner'
        OUTER = 'outer'
        STATUS_ID = 'id_status'
        CREATE_TIME = 'create_time'
        UPDATE_TIME = 'updat_time'

    class DamageReport:
        ID = 'id_dagame_report'
        CREATE_TIME = 'create_time'
        SERIAL_ID = 'id_serial'
        SUPERVISOR_ID = 'id_supervisor'
        OPERATOR_ID = 'id_operator'
        LINE_ID = 'id_line'
        PRODUCT_ID = 'id_product'
        DR_DESCRIPTION_ID = 'id_dr_description'
        EXPLANATION_ID = 'id_explanetion'
        SAMPLE = 'Sample'
        NOTE = 'Note'
        DR_STATUS_ID = 'id_dr_status'
        UPDATE_TIME = 'updat_time'

    class Lines:
        ID = 'id_line'
        LINE = 'Line'

# Relaciones entre tablas
class Relations:
    WORKER_POSITION = {
        'table': Tables.WORKERS,
        'foreign_key': Columns.Workers.POSITION_ID,
        'references': Tables.POSITIONS,
        'references_key': Columns.Positions.ID
    }

    USER_WORKER = {
        'table': Tables.USER,
        'foreign_key': Columns.Users.WORKER_ID,
        'references': Tables.WORKERS,
        'references_key': Columns.Workers.ID
    }

    ROLES_USER_ROLE = {
        'table': Tables.ROLES_USER,
        'foreign_key': Columns.RolesUser.ROLE_ID,
        'references': Tables.ROLES,
        'references_key': Columns.Roles.ID
    }

    ROLES_USER_USER = {
        'table': Tables.ROLES_USER,
        'foreign_key': Columns.RolesUser.USER_ID,
        'references': Tables.USER,
        'references_key': Columns.Users.ID
    }

# Consultas SQL comunes
class CommonQueries:
    GET_USER_WITH_WORKER = """
        SELECT u.*, w.Name as worker_name 
        FROM {users} u 
        LEFT JOIN {workers} w ON u.{worker_id} = w.{worker_id}
    """.format(
        users=Tables.USER,
        workers=Tables.WORKERS,
        worker_id=Columns.Users.WORKER_ID,
        worker_pk=Columns.Workers.ID
    )

    GET_WORKER_WITH_POSITION = """
        SELECT w.*, p.{position} as position_name
        FROM {workers} w
        LEFT JOIN {positions} p ON w.{position_id} = p.{position_pk}
    """.format(
        workers=Tables.WORKERS,
        positions=Tables.POSITIONS,
        position=Columns.Positions.POSITION,
        position_id=Columns.Workers.POSITION_ID,
        position_pk=Columns.Positions.ID
    )

def get_table_columns(table_name: str) -> list:
    """
    Retorna las columnas de una tabla específica.
    
    Args:
        table_name: Nombre de la tabla
        
    Returns:
        Lista de nombres de columnas
    """
    columns_map = {
        Tables.POSITIONS: vars(Columns.Positions),
        Tables.WORKERS: vars(Columns.Workers),
        Tables.USER: vars(Columns.Users),
        Tables.ROLES: vars(Columns.Roles),
        Tables.ROLES_USER: vars(Columns.RolesUser),
        Tables.DIE_DESCRIPTION: vars(Columns.DieDescription),
        Tables.SERIALS: vars(Columns.Serials),
        Tables.DAMAGE_REPORT: vars(Columns.DamageReport),
        Tables.LINE: vars(Columns.Lines),
    }
    
    return [col for col in columns_map.get(table_name, {}).values() 
            if not col.startswith('_')]

def get_table_relations(table_name: str) -> list:
    """
    Retorna las relaciones de una tabla específica.
    
    Args:
        table_name: Nombre de la tabla
        
    Returns:
        Lista de diccionarios con las relaciones
    """
    relations = []
    for relation in vars(Relations).values():
        if isinstance(relation, dict):
            if relation['table'] == table_name:
                relations.append(relation)
    return relations 