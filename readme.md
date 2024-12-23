# BugBuster

![BugBuster](bugbuster.webp)

## Description

BugBuster Bot is a powerful automation tool designed to detect, analyze, and eliminate code bugs and bad practices in software repositories. Its purpose is to enhance code quality, streamline development workflows, and reduce technical debt by leveraging advanced integrations with Atlassian tools and AI capabilities.

**Key Features:**
Code Quality Assurance: Scans code for errors, anti-patterns, and inconsistencies based on defined file extensions.
AI-Powered Analysis: Uses OpenAI models to provide insights, suggestions, and fixes for problematic code segments.
Integration with Atlassian: Communicates seamlessly with Atlassian tools like Jira to create bug tickets, track issues, and document findings.
Customizable Checks: Allows developers to define specific extensions and branches to monitor, ensuring targeted and efficient scans.

**Purpose:**
BugBuster Bot aims to minimize human effort in identifying and resolving code issues while promoting best practices in software development. It helps teams maintain cleaner codebases, improve collaboration, and accelerate delivery cycles. With BugBuster, developers can focus more on building great features and less on fixing bugs. 🚀


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
