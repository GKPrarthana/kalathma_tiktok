from playwright.sync_api import sync_playwright
import csv
import os
import json
import requests

# CSV file setup
csv_file = "tiktok_comments.csv"
file_exists = os.path.isfile(csv_file)

# List to store comments API responses
comments_data = []

# Base headers for API requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Referer": "https://www.tiktok.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Function to fetch replies for a comment
def fetch_replies(comment_id, item_id, cookies, ms_token, verify_fp, device_id, web_id):
    replies = []
    cursor = 0
    count = 10  # Number of replies per request

    while True:
        # Construct the reply API URL
        reply_url = (
            f"https://www.tiktok.com/api/comment/list/reply/?"
            f"comment_id={comment_id}&item_id={item_id}&count={count}&cursor={cursor}&"
            f"WebIdLastTime=1744495712&aid=1988&app_language=en&app_name=tiktok_web&"
            f"browser_language=en-US&browser_name=Mozilla&browser_online=true&"
            f"browser_platform=Win32&browser_version=5.0%20%28Linux%3B%20Android%206.0%3B%20Nexus%205%20Build%2FMRA58N%29%20"
            f"AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20Mobile%20Safari%2F537.36&"
            f"channel=tiktok_web&cookie_enabled=true&data_collection_enabled=true&"
            f"device_id={device_id}&device_platform=web_pc&enter_from=tiktok_web&"
            f"focus_state=true&fromWeb=1&from_page=user&history_len=7&is_fullscreen=false&"
            f"is_page_visible=true&odinId=7478484831431083016&os=android&priority_region=LK&"
            f"referer=https%3A%2F%2Fwww.tiktok.com%2Flogin&region=LK&"
            f"root_referer=https%3A%2F%2Fwww.google.com%2F&screen_height=689&screen_width=877&"
            f"tz_name=Asia%2FColombo&user_is_login=true&verifyFp={verify_fp}&"
            f"webcast_language=en&msToken={ms_token}"
        )

        try:
            response = requests.get(reply_url, headers=headers, cookies=cookies)
            response.raise_for_status()
            data = response.json()

            if "comments" in data and data["comments"]:
                for reply in data["comments"]:
                    reply_text = reply.get("text", "N/A")
                    reply_id = reply.get("cid", "N/A")
                    replies.append({"id": reply_id, "text": reply_text})
                    print(f"  Reply (ID: {reply_id}): {reply_text}")

            if not data.get("has_more", False):
                break

            cursor = data.get("cursor", cursor + count)
        except Exception as e:
            print(f"Failed to fetch replies for comment {comment_id}: {e}")
            break

    return replies

# Function to intercept API responses
def handle_response(response):
    if "/api/comment/list/" in response.url and "/reply/" not in response.url:
        try:
            data = response.json()
            comments_data.append(data)
            print(f"Intercepted comments API response: {response.url}")
        except Exception as e:
            print(f"Failed to parse API response: {e}")

with sync_playwright() as p:
    # Launch a browser in non-headless mode to avoid detection
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")

    # Intercept network responses
    page.on("response", handle_response)

    # Go to the TikTok login page
    login_url = "https://www.tiktok.com/login/phone-or-email/email"
    try:
        page.goto(login_url, timeout=60000, wait_until="domcontentloaded")
        print("Login page loaded successfully")
    except Exception as e:
        print(f"Failed to load login page: {e}")
        browser.close()
        exit()

    # Wait for manual login
    try:
        print("Please manually enter your username and password, then click 'Log in'. The script will wait for the login to complete.")
        page.wait_for_url("https://www.tiktok.com/*", timeout=120000)
        print("Logged in successfully (detected URL change)")
    except Exception as e:
        print(f"Login failed or timeout waiting for redirect: {e}")
        browser.close()
        exit()

    # Extract cookies and authentication tokens after login
    cookies = {cookie["name"]: cookie["value"] for cookie in page.context.cookies()}
    ms_token = "J0b7kjMK3VZ044GA4EEEr10RUQSBJl_knDy91SEw7_qb7Z1oyKF5gK8d2D_9nJlnw1RQxElUrKH56LhnmeM2jfv6tk3RJbEJoBhbdH20j2rbUM4qy2bnbgSUQJud-7Nve9ETA5CSD4qitsk="
    verify_fp = "verify_m9fiz3tt_FcIryXHL_8uPm_4e0f_8zE5_rCQaSibKm9Wz"
    device_id = "7492551987054708232"
    web_id = "7492551987054708232"

    # Go to the TikTok video page after login
    video_url = "https://www.tiktok.com/@rizzcado/photo/7491129701956652306?is_from_webapp=1&sender_device=pc&web_id=7492551987054708232"
    try:
        page.goto(video_url, timeout=60000, wait_until="domcontentloaded")
        print("Video page loaded successfully")
    except Exception as e:
        print(f"Failed to load video page: {e}")
        browser.close()
        exit()

    # Scroll to load more comments
    max_scroll_attempts = 10
    scroll_attempts = 0
    last_response_count = 0

    while scroll_attempts < max_scroll_attempts:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)
        current_response_count = len(comments_data)
        print(f"Scroll attempt {scroll_attempts + 1}: {current_response_count} API responses intercepted")
        if current_response_count == last_response_count and current_response_count > 0:
            print("No more comments to load")
            break
        last_response_count = current_response_count
        scroll_attempts += 1

    # Save intercepted API responses for debugging
    with open("comments_api_responses.json", "w", encoding="utf-8") as f:
        json.dump(comments_data, f, indent=2)
    print("Intercepted API responses saved to comments_api_responses.json")

    # Open CSV file to write comments
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Comment", "Reply"])

        # Process intercepted comments
        for data in comments_data:
            if "comments" not in data:
                print("No comments found in this API response")
                continue

            for comment in data["comments"]:
                try:
                    comment_text = comment.get("text", "N/A")
                    comment_id = comment.get("cid", "N/A")
                    print(f"Comment (ID: {comment_id}): {comment_text}")

                    # Check for replies
                    replies_list = []
                    reply_count = comment.get("reply_comment_total", 0)

                    if reply_count > 0:
                        # Fetch all replies using the reply API
                        replies = fetch_replies(
                            comment_id=comment_id,
                            item_id="7491129701956652306",
                            cookies=cookies,
                            ms_token=ms_token,
                            verify_fp=verify_fp,
                            device_id=device_id,
                            web_id=web_id
                        )
                        for reply in replies:
                            replies_list.append(reply["text"])

                    # Write to CSV
                    if replies_list:
                        for reply_text in replies_list:
                            writer.writerow([comment_text, reply_text])
                    else:
                        writer.writerow([comment_text, ""])
                except Exception as e:
                    print(f"Error processing comment: {e}")

    browser.close()

print(f"Comments and replies saved to {csv_file}")