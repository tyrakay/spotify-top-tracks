# 🎵 Spotify Top Tracks ETL Pipeline (AWS Lambda)

**Project Type:** Data Engineering / ETL / Cloud  
**Tools & Services:** AWS Lambda, S3, Secrets Manager, Python, Requests, Boto3  

---

## **Overview**

As an avid Spotify user, I got curious: which artists sneak into my playlists the most? Which tracks dominate my rotation? This project answers those questions by turning my Spotify playlist obsession into a serverless ETL pipeline.

It fetches tracks from a playlist, transforms the data to extract key fields, calculates summary statistics (like top artists and average popularity), and stores both raw and summarized data in AWS S3. All of this runs automatically on AWS Lambda, keeping my music data organized and ready for analytics.

The pipeline:

1. **Authenticates** with the [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)
 using **client credentials**.  
2. **Fetches tracks** from a specified playlist.  
3. **Transforms** the data to extract key fields: track name, artists, popularity, duration.  
4. **Calculates summary statistics**: top artists, average popularity, total duration.  
5. **Stores raw and summary data** in an S3 bucket for downstream analytics or reporting.



## ⚡ Key Features

Serverless ETL using **AWS Lambda.**

Secure handling of Spotify credentials via **Secrets Manager.**

S3 storage for **raw and summarized playlist data.**

Computes simple but insightful **summary statistics.**

Fully configurable via **environment variables.**






<img width="1347" height="1240" alt="top 50 tracks by popularity" src="https://github.com/user-attachments/assets/24a8fcaf-e5a6-4371-96a9-9860c666d915" />
