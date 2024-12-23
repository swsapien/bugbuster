# BugBuster

![BugBuster](bugbuster.webp)

## Description

BugBuster is a powerful bug tracking tool that helps you manage and track software issues efficiently. This repository contains the configuration file `action.yml` to integrate BugBuster into your GitHub Actions workflow.

## Usage

To use BugBuster in your workflow, add the following step to your workflow file:

```yaml
    name: Bugster Bot

    on:
    pull_request:
        branches:
        - develop

    jobs:
    run-bugster-bot:
        runs-on: ubuntu-latest
        steps:
        - name: Use Bugster Bot
            uses: swsapien/bugbuster@main
            with:
            ATLASSIAN_API_TOKEN: ${{ secrets.ATLASSIAN_API_TOKEN }}
            OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```