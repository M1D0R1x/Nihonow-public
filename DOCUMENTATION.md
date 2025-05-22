# Nihonow - Detailed Documentation

This document provides detailed information about the Nihonow Japanese Learning Platform, including its architecture, project structure, and in-depth usage instructions.

## Project Architecture

Nihonow is built using the Django web framework and follows a standard Django project structure with multiple apps:

### Main Components

1. **Nihonow** - The main project container
2. **treasures** - Core application handling user authentication, progress tracking, and learning content
3. **chatbot** - AI-powered assistant for Japanese learning
4. **dojo** - Interactive practice rooms for learning sessions

### Technology Stack

- **Backend**: Django 4.2.20
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Admin Interface**: Django Jazzmin
- **Deployment**: Vercel
- **Real-time Communication**: Ably
- **Static File Serving**: Whitenoise

## Project Structure

```
Nihonow/
├── Nihonow/                 # Main project settings
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── treasures/               # Core app
│   ├── models.py            # Data models
│   ├── views.py             # View functions
│   ├── urls.py              # URL patterns
│   ├── forms.py             # Form definitions
│   └── admin.py             # Admin interface configuration
├── chatbot/                 # Chatbot functionality
│   ├── models.py
│   ├── views.py
│   └── bot.py               # Chatbot logic
├── dojo/                    # Interactive practice rooms
│   ├── models.py
│   ├── views.py
│   └── data/                # Japanese language data
├── static/                  # Static files (CSS, JS)
├── templates/               # HTML templates
├── manage.py                # Django management script
├── requirements.txt         # Project dependencies
└── vercel.json              # Vercel deployment configuration
```

## Database Schema

### User-related Models

- **User** - Django's built-in user model
- **UserProfile** - Extended user information and email confirmation
- **UserProgress** - Tracks user progress across different JLPT levels

### Content Models

- **DailyWord** - Japanese word of the day
- **Kanji** - Kanji characters with readings and meanings
- **QuizQuestion** - Questions for JLPT level quizzes

### Dojo Models

- **DojoRoom** - Virtual rooms for practice sessions

## Detailed Feature Documentation

### User Authentication System

Nihonow implements a custom authentication system that allows users to:
- Register with username and email
- Verify their email through a confirmation link
- Log in with either username or email
- Reset password via email
- Manage their profile

The system uses Django's built-in authentication framework with custom extensions for email verification.

### JLPT Learning Content

Content is organized by JLPT levels (N5 to N1):
- **N5**: Beginner level with basic vocabulary and grammar
- **N4**: Basic level building on N5
- **N3**: Intermediate level
- **N2**: Upper intermediate level
- **N1**: Advanced level

Each level includes:
- Learning materials
- Kanji lists
- Practice quizzes
- Progress tracking

### Kanji Learning System

The kanji learning system includes:
- Categorized kanji lists (numbers, environment, people, etc.)
- Detailed information for each kanji (on'yomi, kun'yomi, meanings)
- Stroke count information
- Example words using the kanji

### Flashcard System

Interactive flashcards for:
- Hiragana
- Katakana
- N5 Kanji

The flashcard system allows users to:
- Flip cards to see readings and meanings
- Mark cards as known/unknown
- Filter cards by category

### Quiz System

The quiz system:
- Presents multiple-choice questions
- Randomizes answer options
- Calculates and stores user scores
- Updates user progress

### Dojo Practice Rooms

The dojo feature allows:
- Creating practice rooms
- Joining existing rooms
- Real-time interaction between participants
- Different question types and categories

### Admin Content Management

Administrators can:
- Add/edit content through the Django admin interface
- Bulk upload content using CSV files
- Manage user accounts
- Monitor user progress

## Development Guidelines

### Adding New Features

1. Create appropriate models in the relevant app
2. Add views and templates
3. Update URL patterns
4. Add tests for new functionality

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Testing

- Write unit tests for models and views
- Test user authentication flows thoroughly
- Ensure responsive design works on different devices

## Deployment Process

### Local Development

1. Make changes to the codebase
2. Test locally using `python manage.py runserver`
3. Run tests with `python manage.py test`

### Production Deployment

1. Ensure all tests pass
2. Update requirements.txt if new dependencies are added
3. Deploy to Vercel using the Vercel CLI
4. Verify the deployment works correctly

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check PostgreSQL credentials in settings.py
   - Ensure the database server is running

2. **Email Verification Problems**
   - Verify EMAIL_* settings in settings.py
   - Check spam folders for verification emails

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings

4. **Deployment Failures**
   - Check Vercel logs for error messages
   - Ensure build_files.sh has correct permissions

## Future Development Roadmap

1. **Mobile Application**
   - Develop native mobile apps for iOS and Android

2. **Enhanced Chatbot**
   - Improve AI capabilities for more natural conversations
   - Add voice recognition for pronunciation practice

3. **Community Features**
   - Forums for user discussions
   - User-generated content and corrections

4. **Expanded Content**
   - Add more vocabulary and grammar lessons
   - Include audio pronunciations for all words

5. **Gamification**
   - Add achievements and badges
   - Implement leaderboards and challenges