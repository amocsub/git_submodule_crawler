from json import dumps
from argparse import ArgumentParser
from os import getenv
import sys
import requests

cache = {}


def show_data(data, output_format, hostname):
    """Print the information retrieved in as a JSON or us a table"""
    if output_format == "json":
        print(dumps(result))
    else:
        if isinstance(data[0], list):
            print("# This repositories have no dependencies")
            for group in data:
                if data.index(group) != 0:
                    print(
                        "\n# This repositories have dependencies from the group/s above")
                for repo in group:
                    if hostname != "api.github.com" and "github.com" in repo['url']:
                        print(
                            f"\033[31m# Dep.lvl: {repo['level']} -> {repo['url']}\033[0m")
                    else:
                        print(f"# Dep.lvl: {repo['level']} -> {repo['url']}")
        else:
            for repo in data:
                if repo['gitmodules']:
                    print(f"# Repo {repo['url']} depends from submodules")
                    for gitmodule in repo['gitmodules']:
                        if hostname != "api.github.com" and "github.com" in gitmodule['url']:
                            print(
                                f"\033[31m# Dep.lvl: {gitmodule['level']} -> {gitmodule['url']} - path: {gitmodule['path']}\033[0m")
                        else:
                            print(
                                f"# Dep.lvl: {gitmodule['level']} -> {gitmodule['url']} - path: {gitmodule['path']}")
                else:
                    print(f"# Repo {repo['url']} has no dependencies")
                print("")


def is_public_repo(url):
    """Verify if a url is from Public Github"""
    return "github.com" in url


def parse_gitmodules(text):
    """Given a string text would parse it and return a list of all submodules referenced"""
    modules = []
    current = None

    for line in text.split("\n"):
        line = line.strip()

        if line.startswith("[submodule"):
            if current is not None:
                modules.append(current)

            current = {"url": None, "path": None}

        elif current is not None:
            if line.startswith("url"):
                current["url"] = line.split("=")[1].strip()

            elif line.startswith("path"):
                current['path'] = line.split("=")[1].strip()

    if current is not None:
        modules.append(current)

    return modules


def clear_repo_url(url, github_host):
    """Given a repo URL would try to return RepoOwner and RepoName from the info provided"""
    other_owner = True
    # Case when url is in HTTPS format from Enterprise Github Repo
    if f"https://{github_host}/" in url:
        url = url.replace(f"https://{github_host}/", "")
    # Case when url is in HTTPS format from Public Github Repo
    elif "https://github.com/" in url:
        url = url.replace("https://github.com/", "")
    # Case when url is in SSH format from Enterprise Github Repo
    elif f"git@{github_host}:" in url:
        url = url.replace(f"git@{github_host}:", "")
    # Case when url is in SSH format from Public Github Repo
    elif "git@github.com:" in url:
        url = url.replace("git@github.com:", "")
    # Case when url is in referencing a traversal path from Enterprise Github Repo from other owner
    elif "../../" in url:
        url = url.replace("../../", "")
    # Case when url is in referencing a traversal path from Enterprise Github Repo from same owner
    elif "../" in url:
        other_owner = False
        url = url.replace("../", "")
    # Always replace '.git' and aditional spaces
    url = url.replace(".git", "")
    url = url.replace(" ", "")
    url = url.replace("\n", "")

    # At this point we should have something like "OWNER/NAME"
    if other_owner:
        try:
            module_owner, module_name = url.split("/")
        except ValueError:
            print(
                f"The repo url: '{url}' is not a valid repo URL, valid formats are Github HTTPS/SSH or Owner/RepoName")
            sys.exit(1)
    else:
        module_name = url
        return None, module_name

    return module_owner, module_name


def fetch_repo_through_api(repo_owner, repo_name, github_host, github_token):
    """Will try to fetch the information related to the repository and the .gitmodules file"""
    query = """query queryRepos($name: String!, $owner: String!){
      repository(owner:$owner, name:$name){
          sshUrl
          url
          nameWithOwner
          diskUsage
          gitmodules_file: object(expression: "HEAD:.gitmodules"){
              ... on Blob {
                  text
              }
          }
      }
  }"""
    headers = {'Authorization': f'Bearer {github_token}',
               'Content-Type': 'application/json'}
    variables = {"owner": repo_owner, "name": repo_name}
    request_body = {"query": query, "variables": variables}
    try:
        if github_host == "api.github.com":
            response = requests.post(
                f"https://{github_host}/graphql", headers=headers, json=request_body, timeout=2)
        else:
            response = requests.post(
                f"https://{github_host}/api/graphql", headers=headers, json=request_body, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException as request_exception:
        # In case there was an error trying to fetch the repo
        print(
            f"There was an error when trying to make the request to the Github API\n{request_exception}")
        sys.exit(1)
    data = response.json()
    if not data['data']['repository']:  # ACA
        # In case the repository could not be found
        print(
            f"The repo https://{'github.com' if github_host == 'api.github.com' else github_host}/{repo_owner}/{repo_name} could not be found with this token, or it may not exist")
        sys.exit(1)
    return data['data']['repository']  # ACA


def fetch_repo_data(repo_owner, repo_name, github_host, github_token, call_level):
    """Given a repo owner and name would try to fetch its data or either through the API or cache, and then parse the submodules within it if they exist"""
    # First we chack if we already have the repo in the cache
    if f"{repo_owner}/{repo_name}" in cache:
        # In case we are looking for this repo in the cache but the level where we are is higher we update it
        if cache[f'{repo_owner}/{repo_name}']['level'] < call_level:
            cache[f'{repo_owner}/{repo_name}']['level'] = call_level
        return cache[f'{repo_owner}/{repo_name}'].copy()
    # If we do not find the repo we need to seach it through the API
    else:
        repo_data = fetch_repo_through_api(
            repo_owner, repo_name, github_host, github_token)
        repo_data['gitmodules'] = list()
        if repo_data['gitmodules_file']:
            for gitmodule in parse_gitmodules(repo_data['gitmodules_file']["text"]):
                module_owner, module_name = clear_repo_url(
                    url=gitmodule["url"], github_host=github_host)
                # In case the owner is not found, it means is from the same owner as the repo we are looking at
                if not module_owner:
                    # In case there is not module owner it means its a ../ reference so the owner should be the same as the repo father.
                    module_owner = repo_owner

                if is_public_repo(url=gitmodule["url"]) and github_host != "api.github.com":
                    # This is in the case we are fetching through an enterprise github host and we got a submodule from a public repo, the token wont work
                    module = {
                        "sshUrl": f"git@github.com:{module_owner}/{module_name}",
                        "url": f"https://github.com/{module_owner}/{module_name}",
                        "nameWithOwner": f"{module_owner}/{module_name}",
                        "gitmodules": [],
                        "gitmodules_file": None,
                        "path": "",
                        "level": call_level+1
                    }
                    if f"{module_owner}/{module_name}" not in cache:
                        cache[f'{module_owner}/{module_name}'] = module.copy()
                else:
                    # We call recursively the function for all the gitmodules a module may have
                    module = fetch_repo_data(
                        repo_owner=module_owner, repo_name=module_name, github_host=github_host, github_token=github_token, call_level=call_level+1)
                module['path'] = f"{gitmodule['path']}/{module['path']}" if module['path'] else gitmodule['path']
                repo_data['gitmodules'].append(module)
                if "gitmodules" in module:
                    for sub_module in module['gitmodules']:
                        if sub_module["nameWithOwner"] not in [m["nameWithOwner"] for m in repo_data['gitmodules']]:
                            submodule_copy = sub_module.copy()
                            submodule_copy['path'] = f"{gitmodule['path']}/{submodule_copy['path']}"
                            repo_data['gitmodules'].append(submodule_copy)
            repo_data['gitmodules'] = sorted(
                repo_data['gitmodules'], key=lambda x: x['level'])

        repo_data['path'] = ""
        repo_data['level'] = call_level
        if repo_data['nameWithOwner'] not in cache:
            cache[f'{repo_owner}/{repo_name}'] = repo_data.copy()
        return repo_data


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Git Submodule Crawler is used to fetch given a particular repository or a file containing several repos all of the submodules they depend on recursively")
    source_parser = parser.add_mutually_exclusive_group(required=True)
    source_parser.add_argument(
        "--repoUrl", "-r", help="Github Repository HTTPS/SSH url to be fetched but it could also be Owner/Name", type=str)
    source_parser.add_argument("--file", "-f", help="File containing Github Repository HTTPS/SSH url to be fetched but it could also be Owner/Name separated with new lines, you can select to display the info returned ordered by having first the repos that have no dependency and the others after that", type=str)
    parser.add_argument("--allDependenciesGroupedByLevel", "-adgbl",
                        help="Specifies to the script to group the output repos by lvl so you can first pull the data of repos that have no dependencies", action="store_true")
    parser.add_argument("--format", help="Specifies the format used to print the data found",
                        choices=("json", "table"), default="table")
    parser.add_argument("--githubEnterpriseHost", "-geh",
                        help="Github Enterprise host that is going to be used to fetch the information, wont be required if env var GITHUB_ENTERPRISE_HOST is set, if not defined would try to fetch the repos in the Github Public API", type=str)
    parser.add_argument("--githubToken", "-gt",
                        help="Github token that is going to be used to fetch the information, wont be required if env var GITHUB_TOKEN is set", type=str)
    args = parser.parse_args()
    if not args.githubEnterpriseHost:
        host = getenv("GITHUB_ENTERPRISE_HOST")
    else:
        host = args.githubEnterpriseHost
    if not args.githubToken:
        token = getenv("GITHUB_TOKEN")
    else:
        token = args.githubToken
    if not host:
        host = "api.github.com"
    if not token:
        print("A Github token is needed to fetch the information through the API\n")
        parser.print_help()
        sys.exit(1)
    if args.repoUrl:
        repo_urls = [args.repoUrl]
    else:
        with open(args.file, "r") as f:
            repo_urls = f.readlines()
    result = []
    for repo_url in repo_urls:
        owner, name = clear_repo_url(url=repo_url, github_host=host)
        if owner and name:
            result.append(fetch_repo_data(repo_owner=owner, repo_name=name,
                          github_host=host, github_token=token, call_level=0))
        else:
            print(
                f"# Repo url {repo_url} is bad formated, it should be a valid HTTPS/SSH URL or at least RepoOwner/RepoName")
            sys.exit(1)
    if not args.allDependenciesGroupedByLevel:
        show_data(result, args.format, host)
    else:
        sorted_list = sorted(cache.values(), key=lambda x: -x['level'])
        all_levels = list(set([v['level'] for v in cache.values()]))
        all_levels.sort(reverse=True)
        grouped_list = list()
        for level in all_levels:
            grouped_list.append(
                [v for v in cache.values() if v['level'] == level])
        show_data(grouped_list, args.format, host)
