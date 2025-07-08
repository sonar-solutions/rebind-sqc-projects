import sys

import httpx
import os

v1_client = httpx.Client(base_url=os.getenv('SONARCLOUD_HOST', 'https://sonarcloud.io/api/'),
                         headers={'Authorization': 'Bearer ' + os.environ['SONARQUBE_TOKEN']})
v2_client = httpx.Client(base_url=os.getenv('SONARCLOUD_API_HOST', 'https://api.sonarcloud.io/'),
                         headers={'Authorization': 'Bearer ' + os.environ['SONARQUBE_TOKEN']})


def get_projects(organization_key, page=1):
    resp = v1_client.get('projects/search', params=dict(organization=organization_key, p=page, ps=500))
    projects = resp.json().get('components', [])
    if resp.json().get('paging', dict()).get('total', 0) > 500:
        projects.extend(get_projects(organization_key, page=page + 1))
    return projects


def get_project_bindings(project_key):
    project_resp = v1_client.get('navigation/component', params=dict(component=project_key))
    project_id = project_resp.json().get('id')
    if project_id is None:
        return []
    binding_resp = v2_client.get('dop-translation/project-bindings', params=dict(projectId=project_id))
    return binding_resp.json().get('bindings', [])


def map_project_integration_id(devOpsPlatform, repositoryId, slug, **_):
    if devOpsPlatform == 'github':
        results = slug
    else:
        results = repositoryId
    print(results)
    return results


def update_project_bindings(binding):
    resp = v2_client.patch(
        f'dop-translation/project-bindings/{binding["id"]}',
        json={
            "repositoryId": map_project_integration_id(**binding),
        }
    )
    print(resp.json())


if __name__ == '__main__':
    projects = get_projects(sys.argv[1])
    bindings = []

    for project in projects:
        bindings.extend(get_project_bindings(project['key']))
    for binding in bindings:
        update_project_bindings(binding=binding)