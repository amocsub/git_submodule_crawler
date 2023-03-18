# Git Submodule Crawler
Super basic tool to list given a list of repositories all of the nested gitmodules that you could have in them.

## What is a submodule?
In Git, a submodule is a way to include another Git repository as a subdirectory within your own repository. If you want to know more please refer to [the docs](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

**Security risks:** Submodules can potentially introduce security risks if you're including code from untrusted sources or not carefully managing the versions of your dependencies. For example, if a submodule contains a vulnerability or malicious code, it could compromise the security of your entire project.

## What for?
- You could spot out easily repositories that you may not know that you are importing with it because they would be printed as red.
- In large ecosystems there are times when you might need to know which are the repos that are serving more than one tool, within this you can spot them out.

## Usage
```
$ python git_submodule_crawler.py --h
usage: git_submodule_crawler.py [-h] (--repoUrl REPOURL | --file FILE) [--allDependenciesGroupedByLevel] [--format {json,table}] [--githubEnterpriseHost GITHUBENTERPRISEHOST]
                                [--githubToken GITHUBTOKEN]

Git Submodule Crawler is used to fetch given a particular repository or a file containing several repos all of the submodules they depend on recursively

options:
  -h, --help            show this help message and exit
  --repoUrl REPOURL, -r REPOURL
                        Github Repository HTTPS/SSH url to be fetched but it could also be Owner/Name
  --file FILE, -f FILE  File containing Github Repository HTTPS/SSH url to be fetched but it could also be Owner/Name separated with new lines, you can select to display the info returned
                        ordered by having first the repos that have no dependency and the others after that
  --allDependenciesGroupedByLevel, -adgbl
                        Specifies to the script to group the output repos by lvl so you can first pull the data of repos that have no dependencies
  --format {json,table}
                        Specifies the format used to print the data found
  --githubEnterpriseHost GITHUBENTERPRISEHOST, -geh GITHUBENTERPRISEHOST
                        Github Enterprise host that is going to be used to fetch the information, wont be required if env var GITHUB_ENTERPRISE_HOST is set, if not defined would try to
                        fetch the repos in the Github Public API
  --githubToken GITHUBTOKEN, -gt GITHUBTOKEN
                        Github token that is going to be used to fetch the information, wont be required if env var GITHUB_TOKEN is set
```

## Examples

### Fetching all the dependencies from the given repos and listing the path where they are pretended to be mounted.

bash```
$ git_submodule_crawler.py --file test-repos.txt --format table
# Repo https://github.com/google/skywater-pdk depends from submodules
# Dep.lvl: 1 -> https://github.com/SymbiFlow/make-env - path: third_party/make-env
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.20.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.20.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.13.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.12.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.12.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.11.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.10.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.10.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr - path: libraries/sky130_fd_pr/v0.0.9
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd - path: libraries/sky130_fd_sc_hd/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd - path: libraries/sky130_fd_sc_hd/v0.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd - path: libraries/sky130_fd_sc_hd/v0.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hdll - path: libraries/sky130_fd_sc_hdll/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hdll - path: libraries/sky130_fd_sc_hdll/v0.1.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hdll - path: libraries/sky130_fd_sc_hdll/v0.1.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs - path: libraries/sky130_fd_sc_hs/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs - path: libraries/sky130_fd_sc_hs/v0.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs - path: libraries/sky130_fd_sc_hs/v0.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms - path: libraries/sky130_fd_sc_ms/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms - path: libraries/sky130_fd_sc_ms/v0.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms - path: libraries/sky130_fd_sc_ms/v0.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls - path: libraries/sky130_fd_sc_ls/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls - path: libraries/sky130_fd_sc_ls/v0.1.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls - path: libraries/sky130_fd_sc_ls/v0.1.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_lp - path: libraries/sky130_fd_sc_lp/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_lp - path: libraries/sky130_fd_sc_lp/v0.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_lp - path: libraries/sky130_fd_sc_lp/v0.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl - path: libraries/sky130_fd_sc_hvl/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl - path: libraries/sky130_fd_sc_hvl/v0.0.3
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl - path: libraries/sky130_fd_sc_hvl/v0.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl - path: libraries/sky130_fd_sc_hvl/v0.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io - path: libraries/sky130_fd_io/latest
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io - path: libraries/sky130_fd_io/v0.2.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io - path: libraries/sky130_fd_io/v0.2.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io - path: libraries/sky130_fd_io/v0.1.0
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io - path: libraries/sky130_fd_io/v0.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io - path: libraries/sky130_fd_io/v0.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr_reram - path: libraries/sky130_fd_pr_reram/v0.0.9
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr_reram - path: libraries/sky130_fd_pr_reram/v2.0.1
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr_reram - path: libraries/sky130_fd_pr_reram/v2.0.2
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr_reram - path: libraries/sky130_fd_pr_reram/v2.0.3
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr_reram - path: libraries/sky130_fd_pr_reram/latest

# Repo https://github.com/google/bloaty depends from submodules
# Dep.lvl: 1 -> https://github.com/google/re2 - path: third_party/re2
# Dep.lvl: 1 -> https://github.com/google/googletest - path: third_party/googletest
# Dep.lvl: 1 -> https://github.com/abseil/abseil-cpp - path: third_party/abseil-cpp
# Dep.lvl: 1 -> https://github.com/protocolbuffers/protobuf - path: third_party/protobuf
# Dep.lvl: 1 -> https://github.com/capstone-engine/capstone - path: third_party/capstone
# Dep.lvl: 1 -> https://github.com/nico/demumble - path: third_party/demumble
# Dep.lvl: 1 -> https://github.com/madler/zlib - path: third_party/zlib
# Dep.lvl: 2 -> https://github.com/open-source-parsers/jsoncpp - path: third_party/protobuf/third_party/jsoncpp

# Repo https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk depends from submodules
# Dep.lvl: 1 -> https://github.com/ThrowTheSwitch/Unity - path: test/unit-test/Unity

# Repo https://github.com/aws/amazon-ecs-agent depends from submodules
# Dep.lvl: 1 -> https://github.com/aws/amazon-ecs-cni-plugins - path: amazon-ecs-cni-plugins
# Dep.lvl: 1 -> https://github.com/aws/amazon-vpc-cni-plugins - path: amazon-vpc-cni-plugins
```

### Fetching all of the repos and grouping the result by the ones without any dependency and so

bash```
$ git_submodule_crawler.py --file test-repos.txt --format table --allDependenciesGroupedByLevel
# This repositories have no dependencies
# Dep.lvl: 2 -> https://github.com/SymbiFlow/make-env
# Dep.lvl: 2 -> https://github.com/google/googletest
# Dep.lvl: 2 -> https://github.com/abseil/abseil-cpp
# Dep.lvl: 2 -> https://github.com/open-source-parsers/jsoncpp

# This repositories have dependencies from the group/s above
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hdll
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_lp
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_io
# Dep.lvl: 1 -> https://github.com/google/skywater-pdk-libs-sky130_fd_pr_reram
# Dep.lvl: 1 -> https://github.com/google/re2
# Dep.lvl: 1 -> https://github.com/protocolbuffers/protobuf
# Dep.lvl: 1 -> https://github.com/capstone-engine/capstone
# Dep.lvl: 1 -> https://github.com/nico/demumble
# Dep.lvl: 1 -> https://github.com/madler/zlib
# Dep.lvl: 1 -> https://github.com/ThrowTheSwitch/Unity
# Dep.lvl: 1 -> https://github.com/aws/amazon-ecs-cni-plugins
# Dep.lvl: 1 -> https://github.com/aws/amazon-vpc-cni-plugins

# This repositories have dependencies from the group/s above
# Dep.lvl: 0 -> https://github.com/google/skywater-pdk
# Dep.lvl: 0 -> https://github.com/google/bloaty
# Dep.lvl: 0 -> https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk
# Dep.lvl: 0 -> https://github.com/aws/amazon-ecs-agent
```