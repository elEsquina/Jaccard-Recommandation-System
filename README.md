# Video Recommendation System with Jaccard Similarity

## Overview
This is my first year Computer Science Engineering final project.
This project implements a video recommendation system using content-based filtering with the Jaccard similarity algorithm. It aims to deliver personalized video recommendations based on user preferences and video content attributes.

## Objective
The goal is to enhance user experience by providing tailored video suggestions that match their interests and viewing history.

## Dataset
- **Source:** Created for testing and demonstration purposes.
- Generates a list of 300 random video titles stored in JSON format.
- Tags extracted using NLTK for content analysis.

## Implementation
### User and Video Classes
- **User Class:** Manages user profiles, including uploaded videos, subscriptions, watch history, and interests (tags).
- **Video Class:** Represents individual videos with attributes like title, likes, dislikes, views, and tags.

### Data Structures
- **Stack Class:** Efficiently manages user watch history.
- **Heap Class:** Implements a binary minheap for recommendation output.
- **Array Class:** Provides dynamic array functionality for managing video and user data.

### Session Management
- **Session Class:** Handles user sessions, enabling login, logout, recommendation queries, and account management.

### Error Handling
- **ErrorMessages and SystemMessages Classes:** Includes predefined messages for debugging and user feedback.

## Testing and Evaluation
The system's effectiveness and performance will be evaluated through simulations using sample user profiles to assess recommendation quality and algorithm refinement.

## Outcome
This project will deliver a functional video recommendation system that offers top video suggestions based on user preferences and content similarity.
