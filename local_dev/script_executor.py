"""
poetry scripts can be ran using
poetry run function_name
"""

import subprocess


def test_all():
    """
    Runs unittests for the repo
    """
    run_subprocess_command('poetry run pytest -vvv rptrc/tests/')


def test_unit():
    """
    Runs unittests for the repo
    """
    run_subprocess_command('poetry run pytest -vvv rptrc/tests/unit_tests/')


def test_integration():
    """
    Runs unittests for the repo
    """
    run_subprocess_command('poetry run pytest -vvv rptrc/tests/integration_tests/')


def test_changed_files():
    """
    Runs unittests for changed tests
    """
    changed_files = get_changed_files()
    for file in changed_files:
        run_subprocess_command(f'poetry run pytest -vvv {file}')


def lint_all():
    """
    Lint all files in repo
    """
    run_subprocess_command('poetry run  pylint --output-format=colorized \
                            --score=y rptrc/')
    run_subprocess_command('poetry run flake8 rptrc/')


def lint_changed_files():
    """
    Lint staged changed files
    """
    changed_files = get_changed_files()
    if not changed_files:
        print('No changed files')
        return None
    run_subprocess_command(f'poetry run  pylint --output-format=colorized \
        --disable=C0328,R0801 --score=y {changed_files}')
    run_subprocess_command(f'poetry run flake8 {changed_files}')
    return None


def get_changed_files():
    """
    Gets all file changes in current patchset
    :return changed_files: The staged changed files
    :rtype list:
    """
    changed_files = get_subprocess_command_output('git diff --name-only "rptrc/*.py"').split('\n')
    print(f'changed_files:\n]{changed_files}[')
    return changed_files


def run_subprocess_command(cmd):
    """
    Runs commands as subproccesses
    :param cmd: The command to run as a subproccess
    :return process_output:
    :rtype stdout:
    :raises
    """
    try:
        print(f'Running cmd:\n\t{cmd}')
        subprocess.run(
            cmd,
            shell=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print("⚡ ")


def get_subprocess_command_output(cmd):
    """
    Runs commands as subproccesses and returns the output
    :param cmd: The command to run as a subproccess
    :return subprocess_output:
    :rtype str:
    """
    try:
        print(f'Running cmd {cmd}')
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            check=True
        )
        result = str(result.stdout.decode("utf-8").strip())
        return result
    except subprocess.CalledProcessError:
        print("⚡")
    return None
