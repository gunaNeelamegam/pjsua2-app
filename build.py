"""
Building the presentation using the reveal js .

command to build html page.
    - python3 build.py
        or 
    - make slide
"""

from subprocess import run
import os
from bs4 import BeautifulSoup
import os
import base64

SOURCE_FILE_NAME = ""

DEPS = [
    "npm init -y",
    "npm i --save asciidoctor @asciidoctor/reveal.js",
]


class RevealJsException(Exception):
    pass


def install_script(command):
    return run(command, shell=True, stderr=open(os.devnull))


def install_deps():
    """
    Installation for building the reveal js presentation.
    """
    map(install_script, DEPS)


def run_npx_with_asciidoc(source_filename="slides.adoc"):
    if not source_filename:
        raise RevealJsException("Provide the RST FILE PATH ....")
    if not os.path.exists(source_filename):
        raise RevealJsException("RST FILE PATH NOT YET EXIST....")

    if SOURCE_FILE_NAME := source_filename.strip().split(".")[0]:
        command = (
            f"npx asciidoctor-revealjs -o  {SOURCE_FILE_NAME}.html {source_filename}"
        )
        response = run(f"{command}", stderr=open(os.devnull), shell=True)
        print(response)
        if response.returncode != 0:
            raise RevealJsException(
                "Something went's wrong when runing building the slides adoc file into html file."
            )
        else:
            print("Successfully Builded html")
    else:
        raise RevealJsException("FILE NAME IS NOT PRESEN ...")


def extract_paths(html_file):
    print(html_file)
    with open(html_file, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        script_tags = soup.find_all("script")
        link_tags = soup.find_all("link")
        img_tag = soup.find_all("img")

        paths = []

        # Extract paths from <script> tags
        for script in script_tags:
            if "src" in script.attrs:
                path = script["src"]
                if "node_modules/" in path:
                    empty_script_tag = soup.new_tag("script")
                    empty_script_tag.string = open(path).read()
                    empty_script_tag.attrs = {"crossorgin": ""}
                    script.replace_with(empty_script_tag)
                    paths.append(os.path.join(os.path.dirname(html_file), path))

        for link in link_tags:
            if "href" in link.attrs:
                path = link["href"]
                if "node_modules/" in path:
                    empty_link_tag = soup.new_tag("style")
                    empty_link_tag.attrs = {"type": "text/css"}
                    empty_link_tag.string = open(path).read()
                    link.replace_with(empty_link_tag)
                    paths.append(os.path.join(os.path.dirname(html_file), path))

        for img in img_tag:
            if "src" in img.attrs:
                path = img.get("src")
                image_type = path.split(".")[-1]
                if ("figures/" or "images/") in path:
                    empty_img_tag = soup.new_tag("img")
                    empty_img_tag.attrs = {
                        **img.attrs,
                        "src": f"data:image/{image_type};base64, {get_base64_data(path)}",
                    }
                    img.replace_with(empty_img_tag)
        modified_html = str(soup)
        modified_file_path = html_file.replace(".html", "_modified.html")
        create_file(modified_file_path, modified_html)
        return (modified_file_path, paths)


def create_file(content, file_path):
    with open(file_path, "w") as modified_file:
        modified_file.write(content)


def get_base64_data(file_name):
    with open(file_name, "rb") as fp:
        return base64.b64encode(fp.read())


"""
FIXME:
    when appending the content with jinja templates or using the string format wont works
"""


def render_template(paths):
    from collections import ChainMap

    data_with_path = []
    for path in paths:
        data_with_path.append({path: open(path, "r").read()})

    data = dict(ChainMap(*data_with_path))
    return data


def build(filename=None):
    run_npx_with_asciidoc(filename)
    _, paths = extract_paths(filename.split(".")[0] + ".html")
    content = render_template(paths)
    create_file(content, "index.html")


def get_rstfilename():
    import sys

    return filter(lambda filename: (".adoc" or ".asciidoc") in filename, sys.argv)


if __name__ == "__main__":
    """
    creating the index.html file from your asciidoc file
    """
    for file in get_rstfilename():
        build(file)
