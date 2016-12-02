import logging
import os

from rhsclbuilder.utils import pushd

LOG = logging.getLogger(__name__)


class BaseBuilder(object):
    """A base class for the package builder."""

    def __init__(self, package_dict):
        self._package_dict = package_dict

    @property
    def built_directory(self):
        return self._built_directory

    @built_directory.setter
    def built_directory(self, value):
        self._built_directory = value

    def prepare(self):
        if 'macros' in self._package_dict:
            self.edit_spec_file_by_macro()

    def edit_spec_file_by_macros(self):
        macros_dict = self._package_dict['macros']
        if not isinstance(macros_dict, dict):
            return ValueError('macros should be dict object.')

        name = self._package_dict['name']
        spec_file = '{0}.spec'.format(name)
        spec_file_origin = '{0}.orig'.format(spec_file)

        os.rename(spec_file, spec_file_origin)
        fh_w = None
        fh_r = None
        try:
            fh_w = open(spec_file, 'w')
            fh_w.write('# Generated by rhscl-builder')
            for key in list(macros_dict.keys()):
                value = macros_dict[key]
                if not value:
                    raise ValueError('macro is invalid in {0}.'.format(name))
                content = '%global {0} {1}\n'.format(key, value)
                fh_w.write(content)
            fh_w.write('\n')
            fh_r = open(spec_file_origin, 'r')
            fh_w.write(fh_r.read())
        finally:
            if fh_r:
                fh_r.close()
            if fh_w:
                fh_w.close()

    def run(self, **kwargs):
        if not self._built_directory:
            raise ValueError('built directory is not set.')

        with pushd(self._built_directory):
            self.prepare()
            self.build(**kwargs)

    def build(self, **kwargs):
        raise NotImplementedError('Implement this method.')