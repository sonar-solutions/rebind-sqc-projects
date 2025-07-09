# rebind-sqc-projects

By default, SonarQube Cloud organizations cannot be transferred to another devops platform. By leveraging the recovery
behavior of SonarQube Cloud, you can override the existing Org Binding and replace it with a new binding.

This repository provides an example of the required API calls to pull the existing bindings and bind the projects to a
new repository. This initial example showcases rebinding from Github to Github

## Requirements
* Install the dependencies with `pip install -r requirements.txt`
* Set the SONARQUBE_TOKEN environment variable with `EXPORT SONARQUBE_TOKEN='{{TOKEN}}'`

## Process

1. Pull the current repository mappings by calling the SonarQube Cloud API and store the results in a bindings.csv using `python pull_project_bindings.py {{ORG KEY}}`
2. Within GitHub, delete the installed SonarQube Cloud application
3. Within the SonarQube Cloud organization, go to Administration > Organization Settings > Organization Binding
4. Update the CSV to point to the new repositories (repo slug for Github)
5. Bind the SonarQube organization to the new DevOps Organization
6. Bind the projects to the new repositories using `python rebinding_projects.py`