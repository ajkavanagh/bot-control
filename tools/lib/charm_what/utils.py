# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
charm-what utils

Attempt to identify whether a directory contains a Juju charm, charm layer,
charm interface, a built charm, or a source charm (top layer), based on
presence and/or absence of certain files.
'''

import glob
import os


def f_exists(*args):
    return os.path.isfile(os.path.join(*args))

def glob_match(*args):
    return glob.glob(os.path.join(*args))

def is_built_charm(asset_path):
    '''Return True if the contents of asset_path appear to
    be a Juju charm built from layers and/or interfaces.'''
    return (
        f_exists(asset_path, 'config.yaml') and
        f_exists(asset_path, 'metadata.yaml') and
        f_exists(asset_path, 'layer.yaml') and
        f_exists(asset_path, '.build.manifest') and not
        f_exists(asset_path, 'interface.yaml')
    )


def is_source_charm(asset_path):
    '''Return True if the contents of asset_path appear to
    be a Juju charm source (containing a top layer).'''
    return (
        f_exists(asset_path, 'src', 'layer.yaml') and
        f_exists(asset_path, 'src', 'metadata.yaml') and not
        f_exists(asset_path, 'src', '.build.manifest') and not
        f_exists(asset_path, 'src', 'interface.yaml') and not
        f_exists(asset_path, 'layer.yaml') and not
        f_exists(asset_path, '.build.manifest') and not
        f_exists(asset_path, 'interface.yaml')
    )


def is_source_operator_charm(asset_path):
    '''Return True if the contents of asset_path appear to
    be a Juju charm source (containing a top layer).'''
    return (
        f_exists(asset_path, 'src', 'charm.py') and
        f_exists(asset_path, 'metadata.yaml') and not
        glob_match(asset_path, 'src', 'reactive', '*') and not
        glob_match(asset_path, '*.charm')
    )


def is_built_operator_charm(asset_path):
    '''Return True if the contents of asset_path appear to
    be a Juju charm source (containing a top layer).'''
    return (
        glob_match(asset_path, '*.charm')
    )


def is_classic_charm(asset_path):
    '''Return True if the contents of asset_path appear to
    be a classic (non-layered) Juju charm.'''
    return (
        f_exists(asset_path, 'metadata.yaml') and not
        f_exists(asset_path, 'layer.yaml') and not
        f_exists(asset_path, '.build.manifest') and not
        f_exists(asset_path, 'interface.yaml') and not
        f_exists(asset_path, 'src', 'charm.py')
    )


def is_charm_interface(asset_path):
    '''Return True if the contents of asset_path appear to
    be a Juju charm interface.'''
    return (
        f_exists(asset_path, 'interface.yaml') and not
        f_exists(asset_path, '.build.manifest') and not
        f_exists(asset_path, 'layer.yaml')
    )


def is_charm_layer(asset_path):
    '''Return True if the contents of asset_path appear to
    be a Juju charm layer.'''
    return (
        f_exists(asset_path, 'layer.yaml') and not
        f_exists(asset_path, '.build.manifest') and not
        f_exists(asset_path, 'interface.yaml')
    )


def is_func_bundle(asset_path):
    '''Return True if the contents of asset_path appear to
    be a testable Juju bundle.'''
    return (
        f_exists(asset_path, 'bundle.yaml') and
        f_exists(asset_path, 'tests', 'tests.yaml')
    )

def is_bundle_test_collection(asset_path):
    '''Return True if the contents of asset_path appear to
    be a collection of bundles and tests.'''
    return (
        glob_match(asset_path, 'tests', '*', 'tests', 'tests.yaml') and not
        f_exists(asset_path, 'bundle.yaml')
    )


def whatis(asset_path):
    '''Attempt to determine if the contents of asset_path appear
    to be a classic charm, a built charm, a layer, or
    an interface.'''
    if is_built_charm(asset_path):
        return 'charm (built)'
    elif is_classic_charm(asset_path):
        return 'charm (classic)'
    elif is_source_charm(asset_path):
        return 'charm (source)'
    elif is_source_operator_charm(asset_path):
        return 'charm (source operator)'
    elif is_built_operator_charm(asset_path):
        return 'charm (built operator)'
    elif is_charm_layer(asset_path):
        return 'layer'
    elif is_charm_interface(asset_path):
        return 'interface'
    elif is_func_bundle(asset_path):
        return 'bundle (func)'
    elif is_bundle_test_collection(asset_path):
        return 'bundle (bundle_test_collection)'
    else:
        return None
