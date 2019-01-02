#!/usr/bin/python

# Copyright (c) Ontic. (http://www.ontic.com.au). All rights reserved.
# See the COPYING file bundled with this package for license details.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: kong_route
short_description: Manage Kong route entities
options:
  admin_url:
    required: false
    default: http://localhost:8001
    description:
      - Kong admin URL in the form (http|https)://host.domain[:port]
  admin_username:
    required: false
    description:
      - Username used when Basic authentication is required to access the Kong Admin API.
  admin_password:
    required: false
    description:
      - Password used when Basic authentication is required to access the Kong Admin API.
  action:
    required: true
    choices:
      - create
      - delete
      - find
      - plugins
      - list
    description:
      - An action to perform. If `create` a route will be created or updated. If `delete` a
        route will be removed. If `find` the response will contain route information. If `list`
        the response will contain a collection of routes and all their information. If `plugins` the
        response will contain a collection of plugins and all their information.
  id:
    required: false
    description:
      - A unique name or UUID used as the route primary key.
  protocols:
    required: false
    default: ["http", "https"]
    description:
      - A list of supported protocols.
  methods:
    required: false
    description:
      - A list of accepted HTTP methods.
  hosts:
    required: false
    description:
      - A list of hostnames, supporting a wildcard at the beginning or end.
  paths:
    required: false
    description:
      - A list of path components, which may use regexes.
  regex_priority:
    required: false
    default: 0
    description:
      - The priority for sorting routing routes containing regular expressions.
  strip_path:
    required: false
    default: yes
    description:
      - When matching an API via one of the paths, strip that matching prefix from the upstream URI to be requested.
  preserve_host:
    required: false
    default: no
    description:
      - When matching an API via one of the hosts, forward the Host header to the upstream service.
  service:
    required: false
    description:
      - A foreign key linking it to a service entity.
  size:
    required: false
    description:
      - A limit on the number of objects to be returned. Only applicable when the
        `action` field is set to `list`.
  offset:
    required: false
    description:
      - A cursor used for pagination. `offset` is an object identifier that defines a place in the list.
'''

EXAMPLES = '''
- name: Create a route
  kong_route:
    id: example-route
    service: example-service
    hosts: example.com
    action: create
  register: route_create

- name: Debug route create
  debug: var=route_create

- name: Find a route
  kong_route:
    id: example-route
    action: find
  register: route_find

- name: Debug route find
  debug: var=route_find

- name: List all route plugins
  kong_route:
    id: example-route
    action: plugins
  register: route_plugins

- name: Debug route plugins
  debug: var=route_plugins

- name: List all routes
  kong_route:
    action: list
  register: route_list

- name: Debug route list
  debug: var=route_list

- name: Delete a route
  kong_route:
    id: example-route
    action: delete
  register: route_delete

- name: Debug route delete
  debug: var=route_delete
'''

RETURN = '''
msg:
  description: The HTTP message from the request
  returned: always
  type: str
  sample: OK (unknown bytes)
status:
  description: The HTTP status code from the request
  returned: always
  type: int
  sample: 200
url:
  description: The actual URL used for the request
  returned: always
  type: str
  sample: http://localhost:8001/routes
output:
  description: The data returned from the request
  returned: always
  type: dic
'''

from ansible.module_utils.kong import KongRouteApi
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec

def main():

    module_spec = {
        'admin_url': dict(required=False, default='http://localhost:8001', type='str'),
        'url_username': dict(required=False, default=None, type='str', aliases=['admin_username']),
        'url_password': dict(required=False, default=None, type='str', aliases=['admin_password'], no_log=True),
        'action': dict(required=True, default=None, type='str', choices=['create', 'delete', 'find', 'plugins', 'list']),
        'id': dict(required=False, default=None, type='str', include=True, uuid=True),
        'protocols': dict(required=False, default=None, type='list', include=True),
        'methods': dict(required=False, default=None, type='list', include=True),
        'hosts': dict(required=False, default=None, type='list', include=True),
        'paths': dict(required=False, default=None, type='list', include=True),
        'regex_priority': dict(required=False, default=None, type='int', include=True),
        'strip_path': dict(required=False, default=None, type='bool', include=True),
        'preserve_host': dict(required=False, default=None, type='bool', include=True),
        'service': dict(required=False, default=None, type='str', include=True, foreign='id', uuid=True),
        'size': dict(required=False, default=None, type='int', include=True),
        'offset': dict(required=False, default=None, type='int', include=True),
        'created_at': dict(required=False, default=None, type='int', include=False),
        'updated_at': dict(required=False, default=None, type='int', include=False)
    }

    argument_spec = url_argument_spec()
    argument_spec.update(module_spec)

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    api = KongRouteApi(module)

    try:
        if api.action == 'create':
            result = api.required('id, service').either('methods, hosts, paths').create()
        elif api.action == 'delete':
            result = api.required('id').delete()
        elif api.action == 'find':
            result = api.required('id').find()
        elif api.action == 'plugins':
            result = api.required('id').plugins()
        elif api.action == 'list':
            result = api.list()
    except ValueError, error:
        result = {
            'message': str(error),
            'failed': True
        }

    module.exit_json(**result)

if __name__ == '__main__':
    main()
