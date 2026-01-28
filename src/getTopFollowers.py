#!/usr/bin/env python3
import requests
import os

USERNAME = "lu-value"
TOKEN = os.environ.get("GH_TOKEN")
MAX_FOLLOWERS = 14  # 2 rows of 7

def get_followers():
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    url = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
    response = requests.get(url, headers=headers)
    return response.json()

def get_user_info(username):
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    return response.json()

def generate_table(followers):
    rows = []
    current_row = []

    for i, follower in enumerate(followers[:MAX_FOLLOWERS]):
        user = get_user_info(follower["login"])
        name = user.get("name") or follower["login"]

        cell = f'''    <td align="center">
      <a href="https://github.com/{follower["login"]}">
        <img src="{follower["avatar_url"]}" width="100px;" alt="{follower["login"]}"/>
      </a>
      <br />
      <a href="https://github.com/{follower["login"]}">{name}</a>
    </td>'''

        current_row.append(cell)

        if len(current_row) == 7 or i == len(followers[:MAX_FOLLOWERS]) - 1:
            rows.append("  <tr>\n" + "\n".join(current_row) + "\n  </tr>")
            current_row = []

    return "<table>\n" + "\n".join(rows) + "\n</table>"

def update_readme():
    followers = get_followers()

    if not followers or isinstance(followers, dict):
        print("No followers found or API error")
        return

    table = generate_table(followers)

    with open("README.md", "r") as f:
        content = f.read()

    start_marker = "<!--START_SECTION:top-followers-->"
    end_marker = "<!--END_SECTION:top-followers-->"

    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    new_content = content[:start_idx] + "\n" + table + "\n" + content[end_idx:]

    with open("README.md", "w") as f:
        f.write(new_content)

    print("README updated with top followers!")

if __name__ == "__main__":
    update_readme()
