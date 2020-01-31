# 110yards.ca

**110 yards is now an open source project!** (The front end, anyway).

There's more work to be done as I port this project from C#/MVC to a cloud-native, VueJS app, but I welcome any pull requests, should anyone wish to contribute.

I am targetting the end of February to have the web site back up and running, then I'm hoping to do some test leagues with randomized data and a small set of users.

If you are interested in testing, or contributing, please feel free to contact me at pudds55 (at) gmail.com or via the issue tracker.

## How to run locally

Included in this repository is a devcontainer configuration - if you are using docker and VSCode with the Remote Containers extension, getting this project up and running should be as simple as opening it in the devcontainer and running the following commands:

> yarn install

> yarn serve

You can also run locally - if running locally, you will need yarn and node 12.

By default, this project is configured to point at the 110yards test environment (firebase and web service).

At least for now, the back end components of 110yards are not open source, but if you are interested in contributing to that part of the project as well, please reach out to me.

## How to contribute

If you have made changes you think should be introduced into the project, please create a pull request. Please run all unit tests and apply the project formatting rules before creating the PR. Unit and/or UI tests for your PR are greatly encouraged
