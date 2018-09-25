class Project():
    def __init__(self, id_project, name, session_counter, token):
        self.id_project = id_project
        self.name = name
        self.session_counter = session_counter
        self.token = token

class Session():
    def __init__(self, id_session, index, dt_start, dt_end, is_active, id_project):
        self.id_session = id_session
        self.index = index
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.is_active = is_active
        self.id_project = id_project

class Epoch():
    def __init__(self, id_epoch, index, metrics, id_session):
        self.id_epoch = id_epoch
        self.index = index
        self.metrics = metrics
        self.id_session = id_session