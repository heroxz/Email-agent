SUMMARY_PROMPT_TEMPLATE = """
Generate a brief summary to below email content. Less than 100 words

---
{content}
---
Summary:
"""

# Template: Classified tasks
CLASSIFY_PROMPT_TEMPLATE = """
Below is an email, please classify its category(business, advertisement, system, social):

---
{content}
---
Email category:
"""

# Template: Generate a reply to an email
REPLY_PROMPT_TEMPLATE = """
Please generate a reply to below email: Keep formal and polite mood

---
{content}
---
Generated reply:
"""


# Template: Archive and tag
ARCHIVE_PROMPT_TEMPLATE = """
Based on below email content, create a proper archive folder and tags, for email classification and index

---
{content}
---
Suggested archive folder and tag
"""

if __name__ == "__main__":
    from context_types import MailBody

    mail_body = MailBody(
        plain_text="There will be a department route meeting at 3pm this Friday afternoon at the meeting room of building C. We will discuss the progress of the project and team adjustment."
    )

    prompt = SUMMARY_PROMPT_TEMPLATE.format(content=mail_body.plain_text)
    print(prompt)