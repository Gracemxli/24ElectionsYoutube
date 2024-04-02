from googleapiclient.discovery import build

# Your API key
api_key = 'AIzaSyBxeS6UCM7wQBWn_li_xeP_3wYnYrUSFbI'

# Create a YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Perform a search for videos related to '2024 US Presidential Election'
nextPageToken = None
search_term = '2024 US Presidential Election'
while True:
    search_response = youtube.search().list(
        q=search_term,
        part='id',
        maxResults=100,
        pageToken=nextPageToken
    ).execute()

    # Extract video IDs from the search results
    video_ids = [search_result['id']['videoId'] for search_result in search_response['items']]

    # Iterate over the video IDs and retrieve comments for each video
    for video_id in video_ids:
        # Retrieve video details
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # Extract video title
        video_title = video_response['items'][0]['snippet']['title']

        # Extract uploader's name
        uploader_name = video_response['items'][0]['snippet']['channelTitle']

    # Iterate over the video IDs and retrieve comments for each video
    for video_id in video_ids:
        print(f"Comments for video with ID {video_id}:")
        comment_nextPageToken = None
        while True:
            # Retrieve comments for the video
            comments_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,  # Maximum number of comments to retrieve per request
                pageToken=comment_nextPageToken  # Use nextPageToken for pagination
            ).execute()

            # Iterate over the comments and print them
            for comment in comments_response['items']:
                # Extract comment text
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']

                # Extract user/channel details
                author_channel_id = comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
                author_details_response = youtube.channels().list(
                    part='snippet',
                    id=author_channel_id
                ).execute()

                # Extract user/channel name
                author_name = author_details_response['items'][0]['snippet']['title']

                print(f"Comment by {author_name}: {comment_text}")

            # Check if there are more comments to retrieve
            comment_nextPageToken = comments_response.get('nextPageToken')
            if not comment_nextPageToken:
                break  # Exit loop if there are no more comments
            break
        break

        print("\n")

    # Check if there are more videos to retrieve
    nextPageToken = search_response.get('nextPageToken')
    if not nextPageToken:
        break  # Exit loop if there are no more videos
    break
