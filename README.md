# FastAPI Blog API

This is a RESTful API built using **FastAPI** that allows users to register, log in using JWT authentication, create blog posts, and vote (upvote/downvote) on posts. The system is designed to demonstrate key backend features such as secure authentication, CRUD operations, and relational data management using PostgreSQL and SQLAlchemy.

## ✨ Core Functionality

- **User Registration & Authentication**  
  Secure JWT-based login and token management.

- **Post Management (CRUD)**  
  Users can create, read, update, and delete their own blog posts.

- **Voting System**  
  Users can upvote or remove their vote from any post (1 vote per user per post).

- **User Profiles**  
  Retrieve user details using their ID.

## 🔒 Tech Used

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic for validation
- JWT for authentication

This project is modular and follows best practices, making it easy to extend and maintain.
