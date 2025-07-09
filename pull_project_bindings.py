from clients import v1_client, v2_client
import sys
import csv

def get_projects(organization_key, page=1):
    """Get list of projects"""
    resp = v1_client.get('projects/search', params=dict(organization=organization_key, p=page, ps=500))
    projects = resp.json().get('components', [])
    if resp.json().get('paging', dict()).get('total', 0) > 500:
        projects.extend(get_projects(organization_key, page=page + 1))
    return projects


def get_project_bindings(project_key):
    """Get the list of project bindings for a project"""
    project_resp = v1_client.get('navigation/component', params=dict(component=project_key))
    project_id = project_resp.json().get('id')
    if project_id is None:
        return []
    binding_resp = v2_client.get('dop-translation/project-bindings', params=dict(projectId=project_id))
    return [dict(project_key=project_key, project_id=i['projectId'], binding_id=i['id'], alm=i['devOpsPlatform'], slug=i.get('slug', ''), repository_id=i['repositoryId'], ) for i in binding_resp.json().get('bindings', [])]

if __name__ == '__main__':
    projects = get_projects(sys.argv[1])
    bindings = []

    for project in projects:
        bindings.extend(get_project_bindings(project['key']))
    with open('bindings.csv', 'wt') as f:
        writer = csv.DictWriter(f, fieldnames=['project_key', 'project_id', 'binding_id', 'alm', 'slug', 'repository_id'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(bindings)