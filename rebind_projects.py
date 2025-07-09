from clients import v2_client
import csv




def map_project_integration_id(alm, repository_id, slug, **_):
    if alm == 'github':
        results = slug
    else:
        results = repository_id
    return results


def update_project_bindings(project_binding):
    """Create (or update) the binding for a project"""
    # create new existing binding
    create_resp = v2_client.post(
        'dop-translation/project-bindings',
        json={
            "projectId": project_binding["project_id"],
            "repositoryId": map_project_integration_id(**binding),
        }
    )
    if create_resp.status_code != 200:
        # try to update existing binding
        print(dict(project_key=project_binding['project_key'], **create_resp.json()))
        patch_resp = v2_client.patch(
            f'dop-translation/project-bindings/{project_binding["binding_id"]}',
            json={
                "repositoryId": map_project_integration_id(**project_binding),
            }
        )
        print(dict(project_key=project_binding['project_key'], **patch_resp.json()))




if __name__ == '__main__':
    with open('bindings.csv', 'rt') as f:
        reader = csv.DictReader(f)
        bindings = list(reader)
    # export project & bindings to csv
    # update the slug or repo ID as needed
    for binding in bindings:
        update_project_bindings(project_binding=binding)