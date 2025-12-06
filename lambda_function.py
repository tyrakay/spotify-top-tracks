import boto3
import requests
import json
import datetime
import os
from botocore.exceptions import ClientError
from typing import Tuple, Dict, Any, List

# --- Helpers ---
def get_spotify_credentials() -> Tuple[str, str]:
    """
    Fetch Spotify Client ID and Secret from AWS Secrets Manager.
    """
    secret_name = os.environ.get("SPOTIFY_SECRET_NAME")
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    if not secret_name:
        raise ValueError("Environment variable SPOTIFY_SECRET_NAME not set")

    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error fetching secret: {e}")
        raise e

    secret_dict = json.loads(response['SecretString'])
    return secret_dict['SPOTIFY_CLIENT_ID'], secret_dict['SPOTIFY_CLIENT_SECRET']

def get_spotify_token(client_id: str, client_secret: str) -> str:
    """
    Get Spotify access token using client credentials flow.
    """
    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret)
    )
    auth_response.raise_for_status()
    return auth_response.json()['access_token']

def fetch_playlist_tracks(access_token: str) -> Dict[str, Any]:
    """
    Fetch playlist tracks from Spotify API using environment variable SPOTIFY_PLAYLIST_ID.
    """
    playlist_id = os.environ.get("SPOTIFY_PLAYLIST_ID")
    if not playlist_id:
        raise ValueError("Environment variable SPOTIFY_PLAYLIST_ID not set")

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def transform_tracks(data: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Transform raw Spotify data to simplified track list and summary statistics.
    """
    tracks: List[Dict[str, Any]] = []
    artist_count: Dict[str, int] = {}

    for item in data.get("items", []):
        track_info = item.get("track", {})
        track_name = track_info.get("name")
        artists = [a.get("name") for a in track_info.get("artists", [])]
        popularity = track_info.get("popularity", 0)
        duration_ms = track_info.get("duration_ms", 0)

        tracks.append({
            "track_name": track_name,
            "artists": artists,
            "popularity": popularity,
            "duration_ms": duration_ms
        })

        for artist in artists:
            artist_count[artist] = artist_count.get(artist, 0) + 1

    top_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)[:5]
    avg_popularity = sum(t["popularity"] for t in tracks) / max(len(tracks), 1)
    total_duration_ms = sum(t["duration_ms"] for t in tracks)

    summary = {
        "total_tracks": len(tracks),
        "top_artists": top_artists,
        "average_popularity": avg_popularity,
        "total_duration_ms": total_duration_ms,
        "fetched_at": datetime.datetime.utcnow().isoformat()
    }

    return tracks, summary

def save_to_s3(tracks: List[Dict[str, Any]], summary: Dict[str, Any]) -> Tuple[str, str]:
    """
    Save raw tracks and summary JSON to S3 bucket specified in environment variable S3_BUCKET_NAME.
    """
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("Environment variable S3_BUCKET_NAME not set")

    s3 = boto3.client("s3")
    today = datetime.datetime.utcnow()
    date_path = f"{today.year}/{today.month}/{today.day}"

    raw_key = f"raw/top50/{date_path}/data.json"
    summary_key = f"raw/top50/{date_path}/summary.json"

    s3.put_object(Bucket=bucket_name, Key=raw_key, Body=json.dumps(tracks))
    s3.put_object(Bucket=bucket_name, Key=summary_key, Body=json.dumps(summary))

    return raw_key, summary_key

# --- Lambda Handler ---
def lambda_handler(event: dict, context: Any) -> dict:
    """
    AWS Lambda entry point.
    """
    print("Starting Lambda execution")
    try:
        client_id, client_secret = get_spotify_credentials()
        token = get_spotify_token(client_id, client_secret)
        raw_data = fetch_playlist_tracks(token)
        tracks, summary = transform_tracks(raw_data)
        raw_key, summary_key = save_to_s3(tracks, summary)

        print(f"Execution completed: raw={raw_key}, summary={summary_key}")
        return {
            "status": "success",
            "raw_s3_key": raw_key,
            "summary_s3_key": summary_key
        }

    except Exception as e:
        print(f"Lambda execution failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
