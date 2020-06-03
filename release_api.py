#!/usr/bin/env python
import os
import gitlab
from datetime import datetime

if __name__ == '__main__':
    # TODO: set by protected enviroment variable 
    access_token = os.environ['RELEASE_TOKEN']

    gitlab_url = os.environ['GITLAB_URL']

    project_id = int(os.environ['CI_PROJECT_ID'])
    
    # TODO: need to automate generate these tags in the CI pipeline. 
    tag_name = os.environ['CI_PIPELINE_ID']
    ref = os.environ['CI_COMMIT_REF_NAME']
    
    # artifactory_links
    artifactory_link = os.environ['ARTIFACTORY_PATH']
    group_name = os.environ['GROUP_NAME']
    project_name = os.environ['PROJECT_NAME']
    directory = f'{datetime.now():%Y%m%d}'
    artifact_name_cms = os.environ['ARTIFACT_NAME_CMS']
    artifact_name_bscs = os.environ['ARTIFACT_NAME_BSCS']
    artifact_name_ixc = os.environ['ARTIFACT_NAME_IXC']
    package_type = os.environ['PACKAGE_TYPE']
    
    # artifacts_links
    artifact_link_cms = f'{artifactory_link}/{group_name}/{project_name}/{directory}/{artifact_name_cms}.{package_type}'
    artifact_link_bscs = f'{artifactory_link}/{group_name}/{project_name}/{directory}/{artifact_name_bscs}.{package_type}'
    artifact_link_ixc = f'{artifactory_link}/{group_name}/{project_name}/{directory}/{artifact_name_ixc}.{package_type}'
    
    # release note
    release_note = os.environ['RELEASE_NOTE']

    # authenticate with gitlab
    gl = gitlab.Gitlab(gitlab_url, private_token=access_token)
    gl.auth()

    # obtain the project object by id
    project = gl.projects.get(project_id)

    # creating the project tags
    project.tags.create({'tag_name': tag_name, 'ref': ref})

    # creating the project releases
    release = project.releases.create(
        {
            'name': f'Release for Pipeline ID {tag_name}',
            'tag_name': tag_name,
            'description': release_note,
            'assets': {
                'links': [{'name': artifact_name_cms, 'url': artifact_link_cms}, {'name': artifact_name_bscs, 'url': artifact_link_bscs}, {'name': artifact_name_ixc, 'url': artifact_link_ixc}]
            }
        }
    )
