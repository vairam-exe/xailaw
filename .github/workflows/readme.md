# AI-Powered Automated Pull Request Review

## Overview

AI-Powered Automated Pull Request Review is a github action designed to streamline the code review process. This GitHub Action checks for changes in your pull requests and utilizes the AI to generate a review. The review is then posted as a comment on the pull request, providing insights and suggestions to improve the code quality.

## Features

- Automatically reviews code changes in pull requests.
- Generates detailed feedback using AI.
- Posts comments directly on the pull request for easy visibility.

## Setup Instructions

To use the Gemini PR Review GitHub Action, you need to set up two secret keys in your GitHub repository:

### 1. Setting Up the Gemini API Key

1. **Obtain Your API Access**: 


2. **Add the API Key to Your GitHub Repository**:
   - Go to your GitHub repository.
   - Click on **Settings**.
   - In the left sidebar, click on **Secrets and variables**.
   - Click on **Actions**.
   - Click on **New repository secret**.
   - Name the secret `API_KEY` and paste your API key into the value field. Click **Add secret**.

### 2. Setting Up the GitHub Personal Access Token (PAT)

1. **Create a Personal Access Token**:
   - Go to your GitHub account settings.
   - Click on **Developer settings**.
   - Click on **Personal access tokens** and then **Tokens (classic)**.
   - Click on **Generate new token**.
   - Give your token a descriptive name and select the scopes you need (at minimum, select `repo` to allow access to your repositories).
   - Click **Generate token** and copy the token.

2. **Add the PAT to Your GitHub Repository**:
   - Go to your GitHub repository.
   - Click on **Settings**.
   - In the left sidebar, click on **Secrets and variables**.
   - Click on **Actions**.
   - Click on **New repository secret**.
   - Name the secret `PAT_TOKEN` and paste your personal access token into the value field. Click **Add secret**.

## Usage

Once you have set up the required secrets, the Gemini PR Review Action will automatically trigger on pull requests that are opened, reopened, or synchronized. The action will:

1. Check out the code.
2. Retrieve the differences in the pull request.
3. Run the AI Based review.
4. Post the review as a comment on the pull request.

## Contact

For any assistance or inquiries, please contact Naresh Vairam V at [nareshvairam.v@dhl.com](mailto:nareshvairam.v@dhl.com).

