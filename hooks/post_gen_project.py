#!/usr/bin/env python
import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
DOC_GEN_DIR = f'{PROJECT_DIRECTORY}/docs'

{% if cookiecutter.documentation_engine == 'mkdocs' -%}
DOC_SPEC_DIR = f'{PROJECT_DIRECTORY}/docs-mkdocs'
UNUSED_DOCS_DIRS = [
    f'{PROJECT_DIRECTORY}/docs-sphinx', 
    f'{PROJECT_DIRECTORY}/docs-jupyter-book'
]
shutil.move(f'{PROJECT_DIRECTORY}/images', f'{DOC_SPEC_DIR}')
shutil.move(f'{DOC_SPEC_DIR}/mkdocs.yaml', PROJECT_DIRECTORY)
shutil.move(f'{DOC_SPEC_DIR}/images/favicon.ico', f'{DOC_SPEC_DIR}')
{%- elif cookiecutter.documentation_engine == 'sphinx' -%}
DOC_SPEC_DIR = f'{PROJECT_DIRECTORY}/docs-sphinx'
UNUSED_DOCS_DIRS = [
    f'{PROJECT_DIRECTORY}/docs-mkdocs', 
    f'{PROJECT_DIRECTORY}/docs-jupyter-book'
]
shutil.move(f'{PROJECT_DIRECTORY}/images', f'{DOC_SPEC_DIR}')
{%- elif cookiecutter.documentation_engine == 'jupyter-book' -%}
DOC_SPEC_DIR = f'{PROJECT_DIRECTORY}/docs-jupyter-book'
UNUSED_DOCS_DIRS = [
    f'{PROJECT_DIRECTORY}/docs-sphinx', 
    f'{PROJECT_DIRECTORY}/docs-mkdocs'
]
shutil.move(f'{PROJECT_DIRECTORY}/images', f'{DOC_SPEC_DIR}')
{% endif %}

def move_coc_contrib_to_doc_dir():
    shutil.move(f'{PROJECT_DIRECTORY}/CODE_OF_CONDUCT.md', DOC_SPEC_DIR)
    shutil.move(f'{PROJECT_DIRECTORY}/CONTRIBUTING.md', DOC_SPEC_DIR)

def remove_unused_docs_dirs():
    for dirs in UNUSED_DOCS_DIRS:
        shutil.rmtree(dirs)

def rename_doc_dir():
    os.rename(DOC_SPEC_DIR, DOC_GEN_DIR)

def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def http2ssh(url):
    url = url.replace("https://", "git@")
    return url.replace("/", ":", 1)


def post_gen():
    move_coc_contrib_to_doc_dir()
    remove_unused_docs_dirs()
    rename_doc_dir()

    subprocess.call(["git", "init"])

    git_https_origin = http2ssh("{{cookiecutter.git_https_origin}}")
    git_https_upstream = http2ssh("{{cookiecutter.git_https_upstream}}")
    git_main_branch = http2ssh("{{cookiecutter.git_main_branch}}")
    git_new_branch = "add-initial-structure"

    if git_https_origin != "":
        subprocess.call(["git", "remote", "add", "origin", git_https_origin])
        subprocess.call(["git", "fetch", "--all"])

    if git_https_upstream != "":
        subprocess.call(
            ["git", "remote", "add", "upstream", git_https_upstream]
        )
        subprocess.call(["git", "checkout", f"upstream/{git_main_branch}"])
        subprocess.call(["git", "fetch", "--all"])

    subprocess.call(
        ["git", "config", "user.name", "{{cookiecutter.author_full_name}}"]
    )
    subprocess.call(
        ["git", "config", "user.email", "{{cookiecutter.author_email}}"]
    )

    subprocess.call(["git", "checkout", "-b", git_new_branch])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "Initial commit"])


if __name__ == "__main__":
    post_gen()
