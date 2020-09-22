from py2neo import NodeMatcher

from connector.models import *

log = logging.getLogger(__name__)


class Pipeline:
    """
    The Pipeline to define the processing of the data
    """

    def __init__(self, config, *args, **kwargs):
        self._name = type(self).__name__
        self._config = config
        self.graph = None
        self.matcher = None
        self._init_neo4j()

    def _init_neo4j(self):
        hostname = self._config['NEO4J']['hostname']
        protocol = self._config['NEO4J']['protocol']
        port = self._config['NEO4J']['port']
        db = self._config['NEO4J']['db']
        user = self._config['NEO4J']['user']
        password = self._config['NEO4J']['password']
        self.graph = Graph(f"{protocol}://{hostname}:{port}/{db}",
                           user=user,
                           password=password)
        self.matcher = NodeMatcher(self.graph)

    @property
    def full_name(self):
        return self._name

    @property
    def name(self):
        name, _ = self._name.split("Pipeline")
        return name

    def get_config_attribute(self, attr: str, section: str = None) -> str:
        """
        Extracts an attribute from an certain section in the configuration file. \
        The default section is the pipeline name it self.
        """
        if section is None:
            section = self.full_name
        try:
            pipe_section = self._config[section]
            attr_value = pipe_section[attr]
            return attr_value
        except KeyError:
            # raise PipelineException(f"Attribute '{attr}' is not defined in {section}.")
            # raise PipelineException(f"Requested pipeline '{section}' is not configured.")
            pass

    def transform_data(self, *args, **kwargs):
        """
        Abstract method to transform the requested data into a another format
        """
        raise NotImplementedError()


class CrawlPipeline(Pipeline):
    """
    A pipeline to process Job
    """

    def __init__(self, config, *arg, **kwargs):
        super().__init__(config, *arg, **kwargs)
        self.crawl_result = None

    def transform_data(self):

        entity_model = Entity.get_or_create(self.graph, self.crawl_result.attributes.get('entity'))

        for job in self.crawl_result.attributes.get('jobs'):
            job_model = Job.get_or_create(self.graph, job.attributes)
            entity_model.add_job(job_model)

            for language in self.crawl_result.attributes.get('languages'):
                id = language['id']
                language_model = Language.match(self.graph, id).first()
                if language_model is None:
                    language_model = Language.create(self.graph, language.attributes)
                    language_model.in_job(job_model)
                    language_model.save(self.graph)
                job_model.languages.update(language_model)

            for framework in self.crawl_result.attributes.get('frameworks'):
                id = framework['id']
                framework_model = Framework.match(self.graph, id).first()
                if framework_model is None:
                    framework_model = Framework.create(self.graph, framework.attributes)
                    framework_model.in_job(job_model)
                    framework_model.save(self.graph)
                job_model.frameworks.update(framework_model)

            for knowledge in self.crawl_result.attributes.get('knowledges'):
                id = knowledge['id']
                knowledge_model = Language.match(self.graph, id).first()
                if knowledge_model is None:
                    knowledge_model = Knowledge.create(self.graph, knowledge.attributes)
                    knowledge_model.in_job(job_model)
                    knowledge_model.save(self.graph)
                job_model.knowledges.update(knowledge_model)

            for device in self.crawl_result.attributes.get('devices'):
                id = device['id']
                device_model = Device.match(self.graph, id).first()
                if device_model is None:
                    device_model = Device.create(self.graph, device.attributes)
                    device_model.in_job(job_model)
                    device_model.save(self.graph)
                job_model.devices.update(device_model)

            for experience in self.crawl_result.attributes.get('experiences'):
                id = experience['id']
                exp_model = Experience.match(self.graph, id).first()
                if exp_model is None:
                    exp_model = Experience.create(self.graph, experience.attributes)
                    exp_model.in_job(job_model)
                    exp_model.save(self.graph)
                job_model.experiences.update(exp_model)

            job_model.save(self.graph)

        entity_model.save(self.graph)
