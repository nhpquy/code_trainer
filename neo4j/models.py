from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

from neo4j import settings
from neo4j.neo4jconnector import Neo4jConnection

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

    # parent's id
    ent_id = Property()
    job_id = Property()

    # device information
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

    # parent's id
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

    entity = RelatedFrom('Entity', 'in')
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


class Entity(GraphObject):
    url_id = Property()
    ent_id = Property()
    value = Property()
    timestamp = Property()

    job = RelatedTo('Job', 'has_Job')

    def as_dict(self):
        return {
            'url_id': self.url_id,
            'ent_id': self.ent_id,
            'value': self.value,
            'timestamp': self.timestamp
        }

    def get_by_id(self):
        return self.match(graph, self.ent_id).first()


class URL(GraphObject):
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
