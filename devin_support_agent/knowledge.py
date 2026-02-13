"""Curated Devin AI knowledge base sourced from official documentation."""

DEVIN_OVERVIEW = """
Devin is the AI software engineer built by Cognition Labs. It helps ambitious engineering
teams crush their backlogs. Devin is an autonomous AI software engineer that can write,
run, and test code. It can refactor code, handle small bugs and user requests, review PRs,
write unit tests, reproduce bugs, build internal tools, and much more.

Access Devin at: https://app.devin.ai
Documentation: https://docs.devin.ai
"""

DEVIN_STRENGTHS = """
Devin excels at:

1. Tackling many small tasks in parallel before they pile up in your backlog:
   - Targeted refactors
   - Small user feature requests, frontend tasks, bug fixes, and edge cases
   - Improving test coverage
   - Investigating and fixing CI failures
   - Addressing lint/static analysis errors
   - CVE remediation and dependency security updates

2. Code migrations, refactors, and modernization:
   - Language migrations (e.g., JavaScript to TypeScript)
   - Framework upgrades (e.g., Angular 16 -> 18)
   - Monorepo to submodule conversions
   - Removing unused feature flags
   - Extracting common code into libraries

3. Common, repetitive engineering tasks:
   - PR Review
   - Codebase Q&A
   - Reproducing & fixing bugs
   - Writing unit tests
   - Maintaining documentation

4. Customer engineering support:
   - Building new integrations and working with unfamiliar APIs
   - Creating customized demos
   - Prototyping solutions
   - Building internal tools

The most successful Devin tasks are typically:
- Quick for you to verify correctness (e.g., checking CI passes or testing an automatic deployment)
- Junior engineer level complexity
- Follow best practices and pre-task checklist
"""

DEVIN_LIMITATIONS = """
Current limitations to keep in mind:

- Large-scale challenges: Devin performs better on smaller, clearly scoped tasks. For complex
  edits, break up the project into smaller, isolated tasks across separate sessions.
- Reliability: Devin may sometimes get off-track. Give clear completion criteria in the initial
  prompt and collaborate on the plan with Ask Devin to improve reliability.
- UI-related aesthetics: Devin can build functional frontends but needs help with aesthetics.
- Mobile development: Devin can help with mobile apps but doesn't have a phone to test with.
- Security: Exercise caution when sharing credentials. Always use the Secrets Manager for credentials.
"""

DEVIN_INTERFACE = """
The Devin Interface includes:

- Shell: Devin's terminal where you can watch commands being executed and view output logs.
  You can also copy the shell output for debugging.
- IDE: Devin's embedded code editor with all standard IDE tools and shortcuts. Follow Devin's
  work in real-time and take over to run commands, make direct code edits, or test code.
- Browser: Watch Devin browse through documentation, test web applications it builds,
  download/upload information, etc. You can jump in via the Interactive Browser.

Devin is designed as a conversational UI that allows you to follow and take over
Devin's development process in the embedded IDE. It's also available via the Devin API.
"""

PRICING_INFO = {
    "currency": "USD",
    "acu_explanation": (
        "Agent Compute Units (ACUs) are a measure of Devin's work. "
        "ACU consumption is based on: number and complexity of actions, "
        "virtual machine time, and networking bandwidth."
    ),
    "plans": [
        {
            "name": "Core",
            "type": "Pay-as-you-go",
            "monthly_fee": 0,
            "acu_cost": 2.25,
            "included_acus": 0,
            "details": (
                "No monthly subscription. Purchase ACUs as needed at $2.25 each. "
                "Optional auto-reload for automatic credit replenishment. "
                "Unused PAYG ACUs never expire."
            ),
        },
        {
            "name": "Teams",
            "type": "Subscription",
            "monthly_fee": 500,
            "acu_cost": 2.25,
            "included_acus": 250,
            "details": (
                "$500/month subscription includes 250 ACUs. "
                "Additional ACUs at $2.25 each with optional auto-reload. "
                "Subscription ACUs reset at the end of billing cycle. "
                "No concurrent session limits — run as many sessions in parallel as you want."
            ),
        },
        {
            "name": "Enterprise",
            "type": "Custom",
            "monthly_fee": None,
            "acu_cost": None,
            "included_acus": None,
            "details": (
                "Custom pricing. Contact Cognition for details. "
                "Enterprise Admins can set Organization ACU Limits. "
                "Track consumption at Enterprise and Organization level. "
                "Includes all Teams features plus advanced admin controls."
            ),
        },
    ],
    "acu_consumption_order": "Subscription ACUs -> PAYG ACUs -> Gift ACUs",
    "acu_saving_tips": [
        "Delegate clearly scoped tasks with a well-defined end goal",
        "Keep prompts and sessions short",
        "Avoid asking Devin to do many different tasks in the same session",
        "Split big projects into sub-tasks across sessions",
    ],
    "free_actions": [
        "Waiting for your response",
        "Waiting for a test suite to run",
        "Setting up and cloning repositories",
    ],
}

FEATURES = [
    {
        "category": "Core Capabilities",
        "items": [
            "Autonomous code writing, running, and testing",
            "Code refactoring",
            "Bug fixing and reproduction",
            "PR Review (Devin Review)",
            "Unit test generation",
            "Internal tool building",
            "Codebase Q&A (Ask Devin)",
            "Data Analyst Agent",
        ],
    },
    {
        "category": "Developer Tools",
        "items": [
            "Embedded IDE with real-time collaboration",
            "Shell/Terminal access",
            "Interactive Browser",
            "Session Insights",
            "Slash Commands",
        ],
    },
    {
        "category": "Knowledge & Context",
        "items": [
            "Knowledge base per workspace",
            "DeepWiki — AI-powered documentation for repos",
            "AGENTS.md support for repo-specific instructions",
            "Repository indexing",
            "Secrets & Site Cookies management",
        ],
    },
    {
        "category": "Automation",
        "items": [
            "Playbooks (creating & using)",
            "Scheduled Sessions",
            "Deployments",
            "Autofix Settings / Bot Comments",
            "Batch sessions via Advanced Mode or API",
        ],
    },
    {
        "category": "MCP (Model Context Protocol)",
        "items": [
            "MCP Marketplace",
            "DeepWiki MCP — query repo documentation programmatically",
            "Devin MCP — interact with Devin from other AI tools",
        ],
    },
]

INTEGRATIONS = [
    {"name": "Slack", "description": "Tag Devin in threads, get notifications"},
    {"name": "Microsoft Teams", "description": "Teams integration for Devin interactions"},
    {"name": "GitHub", "description": "PR creation, review, issue tracking, PR templates"},
    {"name": "GitLab", "description": "Full GitLab SCM integration"},
    {"name": "Bitbucket", "description": "Bitbucket SCM support"},
    {"name": "Linear", "description": "Project management integration"},
    {"name": "Jira", "description": "Issue tracking integration"},
    {"name": "Self-Hosted SCM & Artifacts", "description": "Support for self-hosted Git servers"},
    {"name": "Devin API", "description": "Programmatic access to create sessions and retrieve results"},
    {"name": "VPN Configuration", "description": "Connect Devin to private networks"},
]

BEST_PRACTICES = """
Best practices for working with Devin:

1. Tag Devin on a Slack or Teams thread about a bug you're discussing with coworkers.
2. Delegate complex tasks via the web app and take over in Devin's IDE once it gives a good first draft.
3. Carve out tasks from your todo list at the start of your day and return to draft PRs waiting for review.
4. Give Devin clear, specific instructions — think about what you'd tell a junior engineer.
5. Provide completion criteria in the initial prompt.
6. Use Playbooks for repeatable workflows.
7. Use Knowledge to give Devin context about your codebase conventions.
8. Break large tasks into smaller, isolated sub-tasks across separate sessions.
9. Use AGENTS.md in your repo to give Devin repo-specific instructions.
10. Devin is most effective when it's part of your team and your existing workflow.
"""

COMMON_ISSUES_FAQ = [
    {
        "question": "How do I get started with Devin?",
        "answer": (
            "Sign up for a Teams account at app.devin.ai, set up your repos, "
            "and start your first session. Follow the onboarding guide at docs.devin.ai."
        ),
    },
    {
        "question": "What programming languages does Devin support?",
        "answer": (
            "Devin can work with virtually any programming language. It excels at "
            "popular languages like Python, JavaScript/TypeScript, Java, Go, Ruby, etc. "
            "It can also handle language migrations between these."
        ),
    },
    {
        "question": "Can Devin access private repositories?",
        "answer": (
            "Yes. Connect your GitHub, GitLab, or Bitbucket account during onboarding. "
            "Devin can also be configured with VPN access for self-hosted SCM."
        ),
    },
    {
        "question": "How does Devin handle security?",
        "answer": (
            "Security is Cognition's top priority. Use the Secrets Manager for credentials. "
            "Never hardcode secrets in prompts. Review Cognition's security documentation "
            "for details on data handling and compliance."
        ),
    },
    {
        "question": "What is DeepWiki?",
        "answer": (
            "DeepWiki is Devin's AI-powered documentation tool. It automatically generates "
            "and maintains documentation for your repositories. It's also available as an "
            "MCP tool (DeepWiki MCP) for programmatic access to repo documentation."
        ),
    },
    {
        "question": "What is the Devin API?",
        "answer": (
            "The Devin API lets you programmatically create sessions, send messages, "
            "and retrieve structured results. It's useful for automation, batch processing, "
            "and integrating Devin into your existing workflows and CI/CD pipelines."
        ),
    },
    {
        "question": "Can I use Devin with my existing CI/CD?",
        "answer": (
            "Yes. Devin integrates with GitHub, GitLab, and Bitbucket. It can create PRs, "
            "fix CI failures, and work within your existing SDLC. You can also use Autofix "
            "Settings to automatically trigger Devin on bot comments."
        ),
    },
    {
        "question": "How many sessions can I run at once?",
        "answer": (
            "On the Teams plan, there are no concurrent session limits. You can run as many "
            "sessions in parallel as you want. For Enterprise, limits can be configured "
            "by your admin."
        ),
    },
    {
        "question": "What are Playbooks?",
        "answer": (
            "Playbooks are reusable templates that define a workflow for Devin to follow. "
            "You can create custom Playbooks for common tasks like code reviews, bug fixes, "
            "or specific refactoring patterns. They help ensure consistency and quality."
        ),
    },
    {
        "question": "Does Devin remember context between sessions?",
        "answer": (
            "Each session is independent, but Devin uses your workspace Knowledge base "
            "and AGENTS.md for persistent context. You can also use Session Insights "
            "to review what happened in previous sessions."
        ),
    },
]
