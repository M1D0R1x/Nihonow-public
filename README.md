# Nihonow-Public - Japanese Learning Platform

**Nihonow-Public** is a comprehensive web application designed to help users learn the Japanese language efficiently. The platform offers various tools and resources for learners at different proficiency levels, from beginners to advanced students preparing for the Japanese Language Proficiency Test (JLPT).

## Features

### Learning Resources
- **JLPT Level Content**: Structured learning materials for all JLPT levels (N5 to N1)
- **Hiragana & Katakana**: Complete guides for learning Japanese syllabaries
- **Kanji Learning**: Detailed kanji information including meanings, readings, and stroke counts
- **Daily Japanese Words**: New Japanese vocabulary delivered daily

### Interactive Learning Tools
- **Flashcards**: Interactive flashcards for hiragana, katakana, and kanji
- **Quizzes**: Level-specific quizzes to test your knowledge
- **Progress Tracking**: Monitor your learning progress over time
- **Dojo**: Practice rooms for interactive learning sessions

### User Features
- **User Dashboard**: Personalized dashboard showing progress and recommendations
- **User Authentication**: Secure login with email verification
- **Profile Management**: Customize your learning experience

### Additional Features
- **Chatbot**: AI-powered assistant to help with your Japanese learning
- **Resources Page**: Curated external resources for further learning

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nihonow-public.git
   cd nihonow-public
````

2. **Create and activate a virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ````

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database and environment variables**

   * Create a PostgreSQL database
   * *Update the following sensitive settings in `Nihonow/settings.py`:**

     * Database credentials (name, user, password, host, port)
     * Email application keys
     * Ably API keys

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**

   ```bash
   python manage.py collectstatic
   ```

## Running the Application

### Development Server

To run the application locally for development:

```bash
python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Production Deployment

The application is configured for deployment on Vercel. Follow these steps:

1. Install Vercel CLI

   ```bash
   npm install -g vercel
   ```

2. Deploy to Vercel

   ```bash
   vercel
   ```

## Usage

1. **Registration and Login**

   * Register for an account and verify your email
   * Log in to access all features

2. **Learning Path**

   * Start with Hiragana and Katakana if you're a beginner
   * Progress to N5 level content and gradually move up
   * Use flashcards and quizzes to reinforce your learning

3. **Admin Features**

   * Access the admin panel at `/admin/` with your superuser credentials
   * Bulk upload content using CSV files through the admin interface
   * Manage users, quizzes, and learning content

## Chatbot Configuration

To ensure the chatbot works properly:

* **Update the model name, API endpoint, and API key** in `chatbot/bot.py` with your desired configuration and credentials.

## Contributing

Contributions to Nihonow-Public are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, please contact us through the Contact form on the website.
