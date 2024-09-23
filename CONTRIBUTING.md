
# Skill Forge Contributing Guidelines

### ➡️ **Contributing Guidelines:**

### 1️⃣ Fork the repository
### 2️⃣ Create your own branch with the proper name. Branch naming convention:

**New Feature Development:**
Includes new user stories or whole new feature introduction, e.g.:
```
• feature/user-authentication
• feature/ui-redesign
• feature/add-search-functionality
• feature/update-profile-page
```
**Bug Fixes:**
Priority 1 and 2 bug fixes, not critical, e.g.:
```
• bugfix/login-issue
• bugfix/resolve-signup-error
• bugfix/api-response-fix
• bugfix/database-connection-error
```
**Hot-fixes:**
Priority 0 bug fixes, production critical, e.g.:
```
• hotfix/critical-security-patch
• hotfix/fix-broken-build
• hotfix/urgent-ui-fix
• hotfix/authentication-issue
```

**Miscellaneous:**
```
• chore/update-dependencies
• chore/code-cleanup
• test/add-unit-tests
• refactor/remove-legacy-code
• refactor/new-database-integration
```

### 3️⃣ After you are done with you changes open an Pull-Request and submit you commits. 

To ensure a smooth and efficient code review process, please follow these guidelines when creating a pull request (PR):

**Descriptive Title**
* Provide a concise and clear title that summarizes the purpose of the PR. Avoid generic titles like “Fixes” or “Changes”—be specific.
* ✅  Add user authentication with JWT
*  ❌  Fixed stuff

**Detailed Description**
* **What was changed:** Provide a summary of the changes made in the PR.
* **Why it was changed:** Explain the problem you’re solving or the new feature you’re adding.
* **How it was changed:** Outline the approach taken, and any relevant design decisions.
* **Dependencies:** List any other PRs, issue, libraries, or configurations this PR depends on.
* **Additional context or screenshots:** If relevant, include screenshots for UI changes or logs of issues solved.

**Break Down Large PRs**
* Keep your pull requests small and focused. If the change is large, consider splitting it into smaller, incremental PRs. This makes reviews quicker and less error-prone.

**Link to Relevant Issues**
* If the PR fixes a bug or implements a feature request, reference the issue number using the appropriate keywords so it can be closed automatically after merging.

**Follow Coding Standards**
* Ensure your code follows the project’s coding conventions, such as:
* Code style (e.g., naming conventions, formatting)
* Consistent use of comments and documentation
* Tests for new or updated functionality

**Document Changes**
* Update any relevant documentation, such as API endpoints, configuration files, or README.md, as part of the PR.
* If this change requires environment-specific setup (e.g., new environment variables), clearly explain this in the description.

**Keep PRs Up-to-date**
* If your PR remains open for an extended period, rebase it with the latest changes from the main or development branch. Resolve any merge conflicts early to prevent delays in the review process.

**Request Review**
* Assign appropriate reviewers ([@karastoyanov](https://github.com/karastoyanov)).
* Tag them in the description or use the platform’s review request feature.
* If a specific area of code needs attention, mention it to the reviewer(s).

**Be Open to Feedback**
* Be responsive to reviewer comments.
* If feedback requires changes, update the PR promptly and re-request reviews.
* For larger discussions or significant design changes, consider discussing them in a separate issue or meeting.
