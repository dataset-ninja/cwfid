import os

from dotenv import load_dotenv

import supervisely as sly

if sly.is_development():
    load_dotenv(os.path.expanduser("~/ninja.env"))
    load_dotenv("local.env")

from dataset_tools.convert.cwfid.main import to_supervisely

api = sly.Api.from_env()
workspace_id = sly.env.workspace_id()

project_id = to_supervisely(api, workspace_id)

print("Project id is", project_id)


def convert_and_upload_supervisely_project():
    raise NotImplementedError()
