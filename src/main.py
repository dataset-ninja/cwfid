import json
import os

from dotenv import load_dotenv

import dataset_tools as dtools
import supervisely as sly

# from src.convert import convert_and_upload_supervisely_project

# !    Checklist before running the app:
# * 1. Set project name and project name full.
# * 2. Prepare convert_and_upload_supervisely_project() function in convert.py
#      It should receive API object, workspace_id and project_name and return project_info of the created project.
# * 3. Fill out neccessary fields in custom data dict.
# * 4. Launch the script.
# ? 5. Fill out CITATION.md, EXPERT.md, LICENSE.md, README.md
# ? 6. Push to GitHub.

# * Names of the project that will appear on instance and on Ninja webpage.
PROJECT_NAME = "CWFID"  # str
PROJECT_NAME_FULL = "A Crop/Weed Field Image Dataset"  # str
DOWNLOAD_ORIGINAL_URL = (
    "https://github.com/cwfid/dataset/archive/refs/tags/v1.0.zip"  # Union[None, str, dict]
)
# DOWNLOAD_ORIGINAL_URL = {
#     "link1": "https://github.com/cwfid/dataset/releases",
#     "link2": "https://github.com/cwfid/dataset/releases",
# }
# DOWNLOAD_ORIGINAL_URL = None
CLASS2COLOR = None  # or set manually with {"class" : [R,G,B] } pattern

# * Create instance of supervisely API object.
load_dotenv(os.path.expanduser("~/ninja.env"))
load_dotenv("local.env")
api = sly.Api.from_env()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
agent_id = sly.env.agent_id()

server_address = os.getenv("SERVER_ADDRESS")
sly.logger.info(
    f"Connected to Supervisely. Server address: {server_address}, team_id: {team_id}, workspace_id: {workspace_id}."
)

# * Create directories for result stats and visualizations.
os.makedirs("./stats/", exist_ok=True)
os.makedirs("./visualizations/", exist_ok=True)

# * Trying to retreive project info from instance by name.
project_info = api.project.get_info_by_name(workspace_id, PROJECT_NAME)
if not project_info:
    # * If project doesn't found on instance, create it and use new project info.
    # project_info = convert_and_upload_supervisely_project(api, workspace_id, PROJECT_NAME)
    sly.logger.info(f"Project {PROJECT_NAME} not found on instance. Created new project.")
else:
    sly.logger.info(f"Found project {PROJECT_NAME} on instance, will use it.")

project_id = project_info.id

# * How the app will work: from instance or from local directory.
from_instance = True  # ToDo: Automatically detect if app is running from instance or locally.

# * Step 1: Read project and project meta
# ? Option 1: From supervisely instance


if from_instance:
    sly.logger.info("The app in the instance mode. Will download data from Supervisely.")

    project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
    if CLASS2COLOR is not None:
        items = []
        for obj_class in project_meta.obj_classes.items():
            if obj_class.name in CLASS2COLOR:
                items.append(obj_class.clone(color=CLASS2COLOR[obj_class.name]))
            else:
                items.append(obj_class)
        project_meta = sly.ProjectMeta(obj_classes=items)
        api.project.update_meta(project_id, project_meta)

    datasets = api.dataset.get_list(project_id)
    sly.logger.info(
        f"Prepared project meta and read {len(datasets)} datasets for project with id={project_id}."
    )

# ? Option 2: From local directory
# ! Not implemented yet
# project_path = os.environ["LOCAL_DATA_DIR"]
# sly.download(api, project_id, project_path, save_image_info=True, save_images=False)
# project_meta = sly.Project(project_path, sly.OpenMode.READ).meta
# datasets = None

# * Step 2: Get download link
download_sly_url = dtools.prepare_download_link(project_info)
dtools.update_sly_url_dict(
    {
        PROJECT_NAME: {
            "id": project_id,
            "download_sly_url": download_sly_url,
            "download_original_url": DOWNLOAD_ORIGINAL_URL,
        }
    }
)
sly.logger.info(f"Prepared download link: {download_sly_url}")

# dtools.download(PROJECT_NAME, f"./APP_DATA/{PROJECT_NAME}.tar")
# * Step 3: Update project custom data
sly.logger.info("Updating project custom data...")
custom_data = {
    #####################
    # ! required fields #
    #####################
    "name": PROJECT_NAME,  # * Should be filled in the beginning of file
    "fullname": PROJECT_NAME_FULL,  # * Should be filled in the beginning of file
    "cv_tasks": [
        "semantic segmentation",
        "object detection",
        "instance segmentation",
    ],
    "annotation_types": ["instance segmentation"],
    "industries": ["agriculture"],
    "release_year": 2015,
    "homepage_url": "https://github.com/cwfid/dataset",
    "license": "non-commercial research",
    "license_url": "https://github.com/cwfid/dataset#use",
    "preview_image_id": 295363,  # ! This should be filled AFTER uploading images to instance, just ID of any image
    "github_url": "https://github.com/dataset-ninja/cwfid",  # ! input url to GitHub repo in dataset-ninja
    "github": "dataset-ninja/cwfid",  # ! input GitHub repo in dataset-ninja (short way)
    "download_sly_url": download_sly_url,
    #####################
    # ? optional fields #
    #####################
    "download_original_url": DOWNLOAD_ORIGINAL_URL,
    "paper": r"http://rd.springer.com/chapter/10.1007%2F978-3-319-16220-1_8",
    "citation_url": "https://github.com/cwfid/dataset#paper",
    # "organization_name": Union[None, str, list],
    # "organization_url": Union[None, str, list],
    # "tags": [],
}

# * Update custom data and retrieve updated project info and custom data from instance.
api.project.update_custom_data(project_id, custom_data)
project_info = api.project.get_info_by_id(project_id)
custom_data = project_info.custom_data
sly.logger.info("Successfully updated project custom data.")


def build_stats():
    sly.logger.info("Starting to build stats...")

    stats = [
        dtools.ClassBalance(project_meta, force=False),
        dtools.ClassCooccurrence(project_meta, force=False),
        dtools.ClassesPerImage(project_meta, datasets),
        dtools.ObjectsDistribution(project_meta),
        dtools.ObjectSizes(project_meta),
        dtools.ClassSizes(project_meta),
    ]
    heatmaps = dtools.ClassesHeatmaps(project_meta)
    classes_previews = dtools.ClassesPreview(project_meta, project_info.name, force=False)
    previews = dtools.Previews(project_id, project_meta, api, team_id)

    for stat in stats:
        if not sly.fs.file_exists(f"./stats/{stat.basename_stem}.json"):
            stat.force = True
    stats = [stat for stat in stats if stat.force]

    if not sly.fs.file_exists(f"./stats/{heatmaps.basename_stem}.png"):
        heatmaps.force = True
    if not sly.fs.file_exists(f"./visualizations/{classes_previews.basename_stem}.webm"):
        classes_previews.force = True
    if not api.file.dir_exists(team_id, f"/dataset/{project_id}/renders/"):
        previews.force = True
    vstats = [stat for stat in [heatmaps, classes_previews, previews] if stat.force]

    dtools.count_stats(
        project_id,
        stats=stats + vstats,
        sample_rate=1,
    )

    sly.logger.info("Saving stats...")
    for stat in stats:
        with open(f"./stats/{stat.basename_stem}.json", "w") as f:
            json.dump(stat.to_json(), f)
        stat.to_image(f"./stats/{stat.basename_stem}.png")

    if len(vstats) > 0:
        if heatmaps.force:
            heatmaps.to_image(f"./stats/{heatmaps.basename_stem}.png", draw_style="outside_black")
        if classes_previews.force:
            classes_previews.animate(f"./visualizations/{classes_previews.basename_stem}.webm")
        if previews.force:
            previews.close()

    sly.logger.info("Successfully built and saved stats.")


def build_visualizations():
    sly.logger.info("Starting to build visualizations...")

    renderers = [
        dtools.Poster(project_id, project_meta, force=False),
        dtools.SideAnnotationsGrid(project_id, project_meta),
    ]
    animators = [
        dtools.HorizontalGrid(project_id, project_meta),
        dtools.VerticalGrid(project_id, project_meta, force=False),
    ]

    for vis in renderers + animators:
        if not sly.fs.file_exists(f"./visualizations/{vis.basename_stem}.png"):
            vis.force = True
    renderers, animators = [r for r in renderers if r.force], [a for a in animators if a.force]

    for a in animators:
        if not sly.fs.file_exists(f"./visualizations/{a.basename_stem}.webm"):
            a.force = True
    animators = [a for a in animators if a.force]

    # ? Download fonts from: https://fonts.google.com/specimen/Fira+Sans
    dtools.prepare_renders(
        project_id,
        renderers=renderers + animators,
        sample_cnt=40,
    )

    sly.logger.info("Saving visualizations...")

    for vis in renderers + animators:
        vis.to_image(f"./visualizations/{vis.basename_stem}.png")
    for a in animators:
        a.animate(f"./visualizations/{a.basename_stem}.webm")

    sly.logger.info("Successfully built and saved visualizations.")


def build_summary():
    sly.logger.info("Starting to build summary...")

    summary_data = dtools.get_summary_data_sly(project_info)

    classes_preview = None
    if sly.fs.file_exists("./visualizations/classes_preview.webm"):
        classes_preview = (
            f"{custom_data['github_url']}/raw/main/visualizations/classes_preview.webm"
        )

    summary_content = dtools.generate_summary_content(
        summary_data,
        vis_url=classes_preview,
    )

    with open("SUMMARY.md", "w") as summary_file:
        summary_file.write(summary_content)

    sly.logger.info("Successfully built and saved summary.")


def build_download():
    # replace later
    HOMEPAGE_URL = custom_data["homepage_url"]
    # replace later

    sly.logger.info("Starting to build 'DOWNLOAD.md'...")

    DOWNLOAD_SLY_TEMPLATE = "Dataset **{project_name}** can be downloaded in Supervisely format:\n\n [Download]({download_sly_url})\n\n"

    DOWNLOAD_SLY_TEMPLATE += "As an alternative, it can be downloaded with dataset-tools package:\n``` bash\npip install --upgrade dataset-tools\n```"

    DOWNLOAD_SLY_TEMPLATE += "\n\n... using following python code:\n``` python\nimport dataset_tools as dtools\n\ndtools.download(dataset='{project_name}', dst_dir='~/dtools/datasets/{project_name}.tar')\n```\n"

    download_content = ""

    licensecheck = True
    if DOWNLOAD_ORIGINAL_URL is not None and licensecheck:
        download_content += DOWNLOAD_SLY_TEMPLATE.format(
            project_name=PROJECT_NAME,
            download_sly_url=download_sly_url,
        )
        if isinstance(DOWNLOAD_ORIGINAL_URL, str):
            download_content += (
                f"The data in original format can be 🔗 [downloaded here]({DOWNLOAD_ORIGINAL_URL})"
            )
        elif isinstance(DOWNLOAD_ORIGINAL_URL, dict):
            download_content += f"The data in original format can be downloaded here:\n\n"
            for key, val in DOWNLOAD_ORIGINAL_URL.items():
                download_content += f"- 🔗[{key}]({val})\n"
    else:
        download_content += (
            f"Please visit dataset [homepage]({HOMEPAGE_URL}) to download the data. \n\n"
        )
        download_content += "Later you can convert it to the universal supervisely format using dataset-tools package:\n``` bash\npip install --upgrade dataset-tools\n```"
        download_content += (
            "\n\n... using following python code:\n``` python\nimport dataset_tools as dtools\n\n"
        )
        download_content += f"dtools.download(dataset='{PROJECT_NAME}', dst_dir='~/dtools/datasets/{PROJECT_NAME}.tar')\n```\n"

    with open("DOWNLOAD.md", "w") as download_file:
        download_file.write(download_content)

    sly.logger.info("Successfully built and saved 'DOWNLOAD.md'.")


def main():
    pass

    sly.logger.info("Script is starting...")

    build_stats()
    build_visualizations()
    build_summary()
    build_download()

    sly.logger.info("Script finished successfully.")


if __name__ == "__main__":
    main()
