from cfnprovider import CustomResourceProvider, get_logger, policy
import boto3
import os
logger = get_logger(__name__)
env = os.environ


class NotFoundError(Exception):
    def __init__(self, name):
        super().__init__('Name: {name} not found in exports'.format(name=name))


class ImportValue(CustomResourceProvider):
    def init(self):
        self._region = self.get('Region', env.get('AWS_REGION'))
        self._name = self.get('Name')

        self._cfn = boto3.client('cloudformation', region_name=self._region)
        self.response.set_data('Name', self._name)

    @property
    def id(self):
        return "{}:{}:{}".format(self._region, self._name, self._value)

    def list_exports(self, next_token=None):
        ret = None
        if next_token:
            ret = self._cfn.list_exports(NextToken=next_token)
        else:
            ret = self._cfn.list_exports()
        l = ret['Exports']
        if 'NextToken' in ret:
            l.extend(self.list_exports(next_token=ret['NextToken']))
        return l

    def get_value(self):
        exports = self.list_exports()
        try:
            value = list(filter(lambda x: x["Name"] == self._name, exports))[0]["Value"]
            return value
        except Exception:
            raise NotFoundError(self._name)

    def value(self):
        self._value = self.get_value()
        self.response.physical_resource_id = self.id
        self.response.set_data('Value', self._value)

    def create(self, policies):
        self.value()

    def update(self, policies):
        self.value()

    def delete(self, policies):
        return


def handler(event, context):
    c = ImportValue(event, context)
    c.handle()
