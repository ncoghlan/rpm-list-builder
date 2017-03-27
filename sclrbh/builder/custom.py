import logging

from sclrbh.builder.base import BaseBuilder
from sclrbh import utils
from sclrbh.yaml import Yaml

LOG = logging.getLogger(__name__)


class CustomBuilder(BaseBuilder):
    """A custom builder class."""

    def __init__(self):
        self._yaml_content = None

    def before_run(self, work, **kwargs):
        custom_file = kwargs['custom_file']
        if not custom_file:
            raise ValueError('custom_file is required.')

        for cmd in self.each_yaml_cmd(custom_file, 'before_script'):
            utils.run_cmd(cmd)

    def build(self, package_dict, **kwargs):
        custom_file = kwargs['custom_file']
        if not custom_file:
            raise ValueError('custom_file is required.')

        for cmd in self.each_yaml_cmd(custom_file, 'script'):
            utils.run_cmd(cmd)

    def each_yaml_cmd(self, custom_file, key):
        cmd_dict = self.get_yaml_content(custom_file)
        if key not in cmd_dict:
            return
        cmds = cmd_dict[key]
        for cmd in cmds:
            yield cmd

    def get_yaml_content(self, file_path):
        if self._yaml_content:
            return self._yaml_content
        yaml = Yaml(file_path)
        self._yaml_content = yaml.content
        return self._yaml_content