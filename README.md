# 📝 Django Blogging Platform

A modern, feature-rich blogging web application built with **Django**, **Tailwind CSS**, and **SQLite**, supporting user registration, post creation with categories/tags, multiple image uploads, likes, comments, and more.

## 🚀 Features

### ✅ User System
- User registration and login
- Profile management with image upload and preview

### 📝 Blog Posts
- Create, edit, delete blog posts
- Add categories and tags (choose or create)
- Upload multiple images per post
- Save posts as **Draft** or **Publish**
- View all posts on homepage with filters

### 📚 Post Management
- Filter by category, tag, author
- Full-text search in title/content
- Paginated post listing
- Like/unlike posts
- Comment system per post

### 🔧 Admin Panel
- Manage categories, tags, posts, and users
- Add default tags/categories from admin

### 📷 Media Handling
- Image upload and preview for profiles and posts
- Media files served via `MEDIA_URL`

---

## 💡 Tech Stack

| Layer         | Technology             |
|---------------|------------------------|
| Backend       | Django 5.x             |
| Frontend      | Tailwind CSS           |
| Database      | SQLite (default)       |
| Auth System   | Django's built-in auth |
| Pagination    | Django Paginator       |
| Image Upload  | `ImageField` + MEDIA   |

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone (https://github.com/hassanshiekh19/blogging_website)
cd blogging_website
