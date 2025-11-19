NEWS AGGREGATOR WEB APPLICATION

Software Requirements Specification (SRS) + Architecture & Development Plan

This is a clean, functional, modern, innovative web software, not just “displaying API results.”
It’s designed so you can actually submit it, deploy it, and use it as a portfolio piece.

1. Project Overview

Build a web application that retrieves and displays news from the NewsAPI platform.
Key functions:

Display real-time top headlines

Allow users to search news via keyword

Provide clean, modern UI

Provide well-structured documentation

Securely hide the API key

2. Core Functional Requirements
2.1 Top Headlines Feature

System fetches latest top headlines from NewsAPI.

Headlines appear in a responsive, card-based grid layout.

Each card displays:

Title

Source

Publication time

Short description

“Read more” link to full article

2.2 Search Feature

User types a keyword in search bar.

System calls: https://newsapi.org/v2/everything?q=<keyword>

Results appear in same card layout.

Pagination (e.g., 10 per page).

If no results → show clean “No results found” UI.

2.3 Filters (Optional but Innovative)

Add sidebar filters:

Category

Language

Country

Date range

Makes your project look well-designed and professional.

2.4 Error Handling

Invalid API key → friendly UI message

API unavailable → fallback message

Search field empty → blocked with UI validation

3. Non-Functional Requirements
3.1 Performance

Page loads under 1.5 seconds on modern hardware.

API calls cached for 1–3 minutes to reduce rate limit.

3.2 Security

API key stored in:

.env file (backend version)

OR server-side environment variable

Never exposed in the frontend.

3.3 Usability

Minimal, modern, mobile-responsive UI (TailwindCSS recommended).

Clear navigation: Home | Search | About

Dark mode optional.

3.4 Maintainability

Clean folder structure

Clear modular files

Good naming conventions

README.md with:

Setup

Features

Screenshots

Tech stack

4. Tech Stack (Recommended)

This is the strongest combination for simplicity + polish:

Backend (API Proxy Layer)

FastAPI

Responsible for:

Calling NewsAPI from server

Protecting your API key

Sending clean JSON to frontend

Frontend

HTML + TailwindCSS + Alpine.js
OR

React (if you want advanced UI)

For your situation:
Tailwind + FastAPI is perfect. Fast, clean, simple, deployable.

5. System Architecture
Client (Browser)
      |
      v
Frontend (HTML + Tailwind + Alpine.js)
      |
      v
Backend API (FastAPI)
      |
      v
External API (NewsAPI.org)

Why this architecture?

Your API key stays safe on backend.

Frontend only talks to your server.

Clean separation of concerns.

6. API Endpoints (Your Backend)
1. GET /api/headlines

Fetch top news:

Response example:

{
  "status": "ok",
  "articles": [...]
}

2. GET /api/search?query=...

Search news keywords.

3. GET /api/filters

Optional:

categories, languages, countries (static or fetched)

7. Folder Structure
news-app/
│
├─ backend/
│   ├─ main.py
│   ├─ routers/
│   │   ├─ headlines.py
│   │   ├─ search.py
│   ├─ services/
│   │   ├─ news_api.py
│   ├─ utils/
│   ├─ .env
│
├─ frontend/
│   ├─ index.html
│   ├─ search.html
│   ├─ styles.css (or Tailwind)
│   ├─ js/
│   │   ├─ api.js
│
├─ README.md
├─ requirements.txt
└─ .gitignore


This looks professional and fits RDI standards.

8. User Interface Requirements
Homepage UI Layout

Header: “News Dashboard”

Search bar

Category chips

News cards grid (3 columns desktop, 1 column mobile)

Card Layout

Rounded, shadowed card

Thumbnail image (if available)

Title

Source + date

Description

Button: “Read Article →”

Search Page

Search bar

Filters

Paginated results

9. Innovative Add-ons (Optional but will boost score)
(A) AI Headline Summaries

Summarize each article in 1 sentence using GPT or a local model.

(B) Sentiment Analysis

Show if headline is:

Positive

Neutral

Negative

(C) Personal “Favorites”

User saves articles locally (browser localStorage).

(D) Auto Theme Detection

Dark/light theme based on user OS.

10. Development Timeline (Fast, Efficient)
Day 1–2

Set up repo

Create FastAPI backend

Implement /headlines and /search endpoints

Hide API key

Day 3–4

Build frontend UI with TailwindCSS

Home page + cards + search page

Day 5

Connect frontend to backend

Handle loading + error UI

Day 6

Add filters + pagination

Day 7

Polish UI

Add README with screenshots

Deployment to Render/Fly.io

This is a 1-week complete production-quality project.

11. Deliverables

Functional web application

Public GitHub repository

Clean README.md

Screenshots

Video demo (optional)

Deployed live link (optional, huge bonus)

If you want, I can now generate:

✅ Complete FastAPI backend code
✅ Complete Tailwind frontend code
✅ The entire folder structure ready to deploy
✅ README.md template
✅ A deployment guide

--------------------------------------------------------------------------
Task Description

Your task is to create a program that retrieves news from the News API. First look in to the API’s documentation and how to get data from the API. Also look into GitHub. You are free to choose which programming languages and technologies you want to use for this. The program should have following functionalities:

Get all the current news from the API and show them to user
Get all the news from the API with user given search parameter. Show results to the user.
This task will be evaluated based on the functionalities, user interface and documentation. After you have developed the functionalities, you should focus more on the user interface and documentation.

General steps

Check the documentation of the News API from this link: Get started - Documentation - News API.
Register to the platform and get yourself an API key
Create yourself a public repository in GitHub and start your project
Choose the programming languages and technologies you feel best to fit for this project.
Remember to hide your API key from your public GitHub repository
Develop the functionalities mentioned above to your program.
Create a README.md file for documentation to your GitHub repository.
Return the task by following the instructions below.
