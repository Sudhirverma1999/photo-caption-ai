# Photo Caption AI

A powerful web application that uses AI to analyze photos and generate creative captions, mood-based song recommendations, and smart tags. Built with Django and modern web technologies.

![Photo Caption AI](https://via.placeholder.com/800x400?text=Photo+Caption+AI)

## 🌟 Features

- **AI-Powered Image Analysis**
  - Smart caption generation
  - Mood detection
  - Automatic tag generation
  - Image orientation detection
  - Detailed image information

- **Song Recommendations**
  - Mood-based song suggestions
  - Mix of Bollywood and Western music
  - Curated playlist integration

- **Modern User Interface**
  - Responsive design
  - Drag-and-drop image upload
  - Real-time image preview
  - Interactive gallery view
  - Copy-to-clipboard functionality

- **Smart Features**
  - File type validation
  - Size restrictions
  - Error handling
  - Loading states
  - User feedback

## 🛠️ Technologies Used

- **Backend**
  - Django 4.2
  - Python 3.8+
  - Pillow (PIL)
  - Django REST Framework

- **Frontend**
  - HTML5
  - CSS3 (with CSS Variables)
  - JavaScript (ES6+)
  - Bootstrap 5
  - Font Awesome 6

- **Development Tools**
  - Git
  - VS Code
  - Chrome DevTools

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/photo-caption-ai.git
   cd photo-caption-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit `http://localhost:8000` in your browser

## 📁 Project Structure

```
photo_caption/
├── media/              # Uploaded images
├── photo_analysis/     # Main application
│   ├── templates/     # HTML templates
│   ├── static/        # Static files
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   └── urls.py        # URL routing
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
```

## 💻 Usage

1. **Upload an Image**
   - Click the upload area or drag and drop an image
   - Supported formats: JPEG, PNG, GIF, WebP
   - Maximum file size: 5MB

2. **View Analysis**
   - AI-generated caption
   - Mood detection
   - Recommended song
   - Generated tags
   - Image details

3. **Gallery Features**
   - View all analyzed images
   - Delete images
   - Copy captions and tags

## 🔒 Security Features

- CSRF protection
- File upload validation
- Secure file handling
- Error logging
- Input sanitization

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📝 API Documentation

The application provides the following endpoints:

- `POST /upload/` - Upload and analyze an image
- `GET /gallery/` - View all analyzed images
- `DELETE /delete/<image_id>/` - Delete an image

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Font Awesome
- All contributors and supporters

## 📞 Support

For support, email sudhirverma324@gmail.com.com or create an issue in the repository.

---

Made with ❤️ by [Your Name] 
