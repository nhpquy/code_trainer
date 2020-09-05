from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

from connector import settings
from connector.neo4jconnector import Neo4jConnection

graph = Neo4jConnection(
    settings.NEO4J_URL,
    settings.NEO4J_USER,
    settings.NEO4J_PASSWORD
).get_graph()


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def save(self):
        graph.push(self)


class Device(BaseModel):
    __primarykey__ = "device_id"

    ent_id = Property()
    job_id = Property()
    device_id = Property()
    value = Property()

    jobs = RelatedFrom('Job', 'required_In')

    def as_dict(self):
        return {
            'ent_id': self.ent_id,
            'job_id': self.job_id,
            'device_id': self.device_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.device_id).first()


class Knowledge(BaseModel):
    __primarykey__ = "know_id"

    ent_id = Property()
    job_id = Property()
    know_id = Property()
    value = Property()

    jobs = RelatedFrom('Job', 'required_In')

    def as_dict(self):
        return {
            'ent_id': self.ent_id,
            'job_id': self.job_id,
            'know_id': self.know_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.know_id).first()


class Experience(BaseModel):
    __primarykey__ = "exp_id"

    ent_id = Property()
    lang_id = Property()
    frame_id = Property()
    exp_id = Property()
    value = Property()

    frameworks = RelatedFrom('Framework', 'required_In')
    languages = RelatedFrom('Language', 'required_In')

    def as_dict(self):
        return {
            'ent_id': self.ent_id,
            'lang_id': self.lang_id,
            'frame_id': self.frame_id,
            'exp_id': self.exp_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.exp_id).first()


class Language(BaseModel):
    __primarykey__ = "lang_id"

    ent_id = Property()
    job_id = Property()
    lang_id = Property()
    value = Property()

    jobs = RelatedFrom('Job', 'required_In')
    experiences = RelatedTo('Experience', 'has_Experience')

    def as_dict(self):
        return {
            'ent_id': self.ent_id,
            'job_id': self.job_id,
            'lang_id': self.lang_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.lang_id).first()


class Framework(BaseModel):
    __primarykey__ = "frame_id"

    ent_id = Property()
    job_id = Property()
    frame_id = Property()
    value = Property()

    jobs = RelatedFrom('Job', 'required_In')
    experiences = RelatedTo('Experience', 'has_Experience')

    def as_dict(self):
        return {
            'ent_id': self.ent_id,
            'job_id': self.job_id,
            'frame_id': self.frame_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.frame_id).first()


class Job(BaseModel):
    __primarykey__ = "job_id"

    ent_id = Property()
    job_id = Property()
    value = Property()

    entity = RelatedFrom('Entity', 'in_Entity')
    languages = RelatedTo('Language', 'has_Language')
    frameworks = RelatedTo('Framework', 'has_Framework')
    knowledge = RelatedTo('Knowledge', 'has_Knowledge')
    devices = RelatedTo('Device', 'has_KnowDevice')

    def as_dict(self):
        return {
            'ent_id': self.ent_id,
            'job_id': self.job_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.job_id).first()

    def add_links(self, **kwargs):
        self.languages.add(Language(**kwargs.get("has_Language")))
        self.frameworks.add(Framework(**kwargs.get("has_Framework")))
        self.knowledge.add(Knowledge(**kwargs.get("has_Knowledge")));
        self.devices.add(Device(**kwargs.get("has_KnowDevice")));


class Entity(GraphObject):
    __primarykey__ = "ent_id"

    url_id = Property()
    ent_id = Property()
    value = Property()
    timestamp = Property()

    has_job = RelatedTo('Job', 'has_Job')

    def as_dict(self):
        return {
            'url_id': self.url_id,
            'ent_id': self.ent_id,
            'value': self.value,
            'timestamp': self.timestamp
        }

    def get_by_id(self):
        return self.match(graph, self.ent_id).first()

    def add_job(self, **kwargs):
        self.has_job.add(Job(**kwargs.get("has_job")));


class URL(GraphObject):
    __primarykey__ = "url_id"

    url_id = Property()
    value = Property()

    entities = RelatedTo('Entity', 'has_Entity')

    def as_dict(self):
        return {
            'url_id': self.url_id,
            'value': self.value
        }

    def get_by_id(self):
        return self.match(graph, self.url_id).first()

    def get_by_value(self):
        return self.match(graph, self.value).first()
