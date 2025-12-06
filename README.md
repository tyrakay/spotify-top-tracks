# 🎵 Spotify Top Tracks ETL Pipeline (AWS Lambda)

**Project Type:** Data Engineering / ETL / Cloud  
**Tools & Services:** AWS Lambda, S3, Secrets Manager, Python, Requests, Boto3  

---

## **Overview**

As an avid Spotify user, I got curious: which artists sneak into my playlists the most? Which tracks dominate my rotation? This project answers those questions by turning my Spotify playlist obsession into a serverless ETL pipeline.


It quietly fetches your playlist data, crunches the numbers, and gives you simple summary statistics into which artists dominate your rotation or which tracks you just can’t stop replaying. All of this happens automatically in AWS Lambda while you go about your day.

The pipeline:

1. **Authenticates** with the [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
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






## 📊 Output of the Pipeline

<img width="1347" height="1240" alt="top 50 tracks by popularity" src="https://github.com/user-attachments/assets/24a8fcaf-e5a6-4371-96a9-9860c666d915" />
