# Habit Tracker Backend

## Project Overview

A multi-tenant habit tracking backend to monitor daily habits, track progress, categorize habits, set reminders, and join challenges.

## Features

- Multi-user accounts with roles (`admin`, `user`)
- Create and track habits
- Monitor progress with streaks and units completed
- Categorize habits for better organization
- Set reminders for habits
- Participate in habit challenges

## Database Tables

### Users

- Stores account information
- Columns: `user_id`, `username`, `email`, `password_hash`, `active`, `role`, `created_at`

### Profiles

- Stores user personal info
- Columns: `profile_id`, `user_id`, `full_name`, `dob`, `bio`, `avatar_url`

### Habits

- Stores user habits
- Columns: `habit_id`, `user_id`, `name`, `description`, `frequency`, `goal`, `challenge_id`, `created_at`

### habit_tracking

- Tracks habit completion/progress
- Columns: `tracking_id`, `habit_id`, `status`, `units_completed`, `note`, `streak_count`, `recorded_at`

### HabitCategories

- Categorizes habits
- Columns: `category_id`, `name`, `description`

### HabitCategoryXref

- Xref table for many-to-many Habits ↔ HabitCategories
- Columns: `habit_id`, `category_id`

### HabitReminders

- Stores habit reminders
- Columns: `reminder_id`, `habit_id`, `user_id`, `reminder_time`, `repeat_days`, `message`, `active`, `created_at`

### HabitChallenges

- Stores challenges for habits
- Columns: `challenge_id`, `user_id`, `name`, `description`, `start_date`, `end_date`, `created_at`

### UsersChallengeXref

- Xref table for many-to-many Habits ↔ HabitCategories
- Columns: `user_id`, `challenge_id`

## Roles

- **Admin**: add admin can do
- **User**: add user can do

## Relationships

- Users 1–1 Profiles
- Users 1–M Habits
- Users 1–M HabitReminders
- Users 1–M HabitChallenges
- Habits 1–M habit_tracking
- Habits M–M HabitCategories via HabitCategoryMap
- HabitChallenges 1–M Habits

## Notes

- All PKs are UUIDs
- Supports multi-tenancy
- Designed for future extension: analytics, gamification, social features
