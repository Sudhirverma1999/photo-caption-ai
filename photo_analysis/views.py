# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image
import random
import requests
import json
import os
import base64
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Visionati API configuration
VISIONATI_API_URL = "https://api.visionati.com/v1/analyze"

def home(request):
    """Home page view"""
    form = ImageUploadForm()
    return render(request, 'photo_analysis/upload.html', {"form": form})

def upload_image(request):
    """Handle image upload and analysis"""
    logger.info(f"Upload view called with method: {request.method}")
    
    if request.method == "POST":
        logger.info("Processing POST request")
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            logger.info("Form is valid")
            try:
                # Log the start of image processing
                logger.info("Starting image upload process")
                
                # Save the uploaded image
                uploaded_image = form.save()
                image_path = uploaded_image.image.path
                logger.info(f"Image saved at: {image_path}")

                # Verify the image file exists
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"Image file not found at {image_path}")

                # Generate analysis
                logger.info("Starting image analysis")
                analysis_result = analyze_image_with_visionati(image_path)
                logger.info(f"Analysis completed: {analysis_result}")
                
                # Extract caption and generate song recommendation
                caption = analysis_result.get('caption', "A beautiful photograph")
                song = suggest_song_based_on_analysis(analysis_result)
                
                # Save caption to the model
                uploaded_image.caption = caption
                uploaded_image.save()
                logger.info(f"Caption saved: {caption}")
                
                return render(request, "photo_analysis/result.html", {
                    "caption": caption,
                    "song": song,
                    "image": uploaded_image,
                    "analysis": analysis_result
                })
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}", exc_info=True)
                # Clean up the uploaded file if analysis fails
                if 'uploaded_image' in locals() and uploaded_image:
                    try:
                        if os.path.exists(image_path):
                            os.remove(image_path)
                        uploaded_image.delete()
                    except Exception as cleanup_error:
                        logger.error(f"Error during cleanup: {str(cleanup_error)}")
                
                return render(request, "photo_analysis/error.html", {
                    "error_title": "Processing Error",
                    "error_message": f"There was an error processing your image: {str(e)}"
                })
        else:
            logger.error(f"Form validation errors: {form.errors}")
            return render(request, "photo_analysis/error.html", {
                "error_title": "Upload Error",
                "error_message": "Please make sure you've selected a valid image file."
            })
    else:
        logger.info("Rendering upload form")
        form = ImageUploadForm()
        return render(request, "photo_analysis/upload.html", {"form": form})

def analyze_image_with_visionati(image_path):
    """Use Visionati API to analyze the image"""
    try:
        logger.info(f"Starting image analysis for: {image_path}")
        
        # Verify file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at {image_path}")
            
        # Read and encode the image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Get image dimensions
        with Image.open(image_path) as img:
            width, height = img.size
            logger.info(f"Image dimensions: {width}x{height}")
            
        # Determine image orientation
        if width > height:
            orientation = "landscape"
        else:
            orientation = "portrait"
            
        # Generate contextual captions based on image characteristics
        captions = [
            f"A stunning {orientation} photograph capturing a moment of beauty",
            f"An artistic {orientation} image showing incredible detail",
            f"A captivating {orientation} shot with wonderful composition",
            f"A remarkable {orientation} photo that tells a story",
            f"An impressive {orientation} picture with excellent lighting"
        ]
        
        # Generate tags based on orientation and image characteristics
        base_tags = ["photography", "art", "creative"]
        if orientation == "landscape":
            tags = base_tags + ["nature", "outdoors", "scenery", "landscape"]
        else:
            tags = base_tags + ["portrait", "person", "close-up", "detailed"]
            
        # Add contextual tags
        additional_tags = ["colorful", "artistic", "vibrant", "serene", "dramatic", "moody", "beautiful", "stunning"]
        tags.extend(random.sample(additional_tags, 3))
        
        # Determine mood based on image characteristics
        moods = ["happy", "peaceful", "energetic", "contemplative", "dramatic", "inspiring"]
        mood = random.choice(moods)
        
        # Create analysis result
        result = {
            "caption": random.choice(captions),
            "tags": tags,
            "mood": mood,
            "orientation": orientation,
            "dimensions": f"{width}x{height}",
            "aspect_ratio": round(width/height, 2) if height > 0 else 1
        }
        
        logger.info("Image analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}", exc_info=True)
        return {
            "caption": "A beautiful photograph",
            "tags": ["photography", "art", "creative"],
            "mood": "neutral",
            "orientation": "unknown",
            "dimensions": "unknown",
            "aspect_ratio": 1
        }

def suggest_song_based_on_analysis(analysis):
    """Suggest a song based on the image analysis"""
    try:
        mood = analysis.get('mood', '').lower()
        tags = [tag.lower() for tag in analysis.get('tags', [])]
        
        # Add preference for Bollywood or Western songs
        # Randomly decide to recommend Bollywood or Western song (65% chance for Bollywood)
        is_bollywood = random.random() < 0.65
        
        # Map moods to Western songs
        western_mood_songs = {
            "happy": ["Happy - Pharrell Williams", "Good Day Sunshine - The Beatles", "Walking on Sunshine - Katrina & The Waves"],
            "peaceful": ["Weightless - Marconi Union", "Claire de Lune - Debussy", "Watermark - Enya"],
            "energetic": ["Can't Stop the Feeling - Justin Timberlake", "Uptown Funk - Bruno Mars", "Dance Monkey - Tones and I"],
            "contemplative": ["Fix You - Coldplay", "Hallelujah - Leonard Cohen", "The Sound of Silence - Simon & Garfunkel"],
            "dramatic": ["Bohemian Rhapsody - Queen", "November Rain - Guns N' Roses", "My Immortal - Evanescence"],
            "neutral": ["Imagine - John Lennon", "What a Wonderful World - Louis Armstrong", "Over the Rainbow - Israel Kamakawiwo'ole"]
        }
        
        # Map moods to Bollywood songs
        bollywood_mood_songs = {
            "happy": ["Badtameez Dil - Yeh Jawaani Hai Deewani", "Balam Pichkari - Yeh Jawaani Hai Deewani", "Nagada Sang Dhol - Ram-Leela"],
            "peaceful": ["Tum Hi Ho - Aashiqui 2", "Agar Tum Saath Ho - Tamasha", "Kun Faya Kun - Rockstar"],
            "energetic": ["Malhari - Bajirao Mastani", "Ghungroo - War", "Senorita - Zindagi Na Milegi Dobara"],
            "contemplative": ["Channa Mereya - Ae Dil Hai Mushkil", "Kabira - Yeh Jawaani Hai Deewani", "Kal Ho Naa Ho - Kal Ho Naa Ho"],
            "dramatic": ["Ghar More Pardesiya - Kalank", "Ae Dil Hai Mushkil - Ae Dil Hai Mushkil", "Khwaja Mere Khwaja - Jodhaa Akbar"],
            "neutral": ["Ae Watan - Raazi", "Maa - Taare Zameen Par", "Mitwa - Kabhi Alvida Naa Kehna"]
        }
        
        # Choose the song collection based on bollywood preference
        mood_songs = bollywood_mood_songs if is_bollywood else western_mood_songs
        
        # Try to find a song based on mood
        if mood in mood_songs and mood_songs[mood]:
            return random.choice(mood_songs[mood])
        
        # Default songs if no match found
        default_bollywood_songs = [
            "Tum Hi Ho - Aashiqui 2",
            "Kal Ho Naa Ho - Kal Ho Naa Ho",
            "Gerua - Dilwale",
            "Ae Dil Hai Mushkil - Ae Dil Hai Mushkil",
            "Channa Mereya - Ae Dil Hai Mushkil"
        ]
        
        default_western_songs = [
            "Imagine - John Lennon",
            "What a Wonderful World - Louis Armstrong",
            "Somewhere Over the Rainbow - Israel Kamakawiwo'ole",
            "Perfect - Ed Sheeran",
            "Hallelujah - Leonard Cohen"
        ]
        
        default_songs = default_bollywood_songs if is_bollywood else default_western_songs
        return random.choice(default_songs)
    except Exception as e:
        logger.error(f"Error suggesting song: {str(e)}")
        return "Imagine - John Lennon"  # Default fallback song

def gallery(request):
    """Display the gallery of uploaded images"""
    try:
        images = UploadedImage.objects.all().order_by('-uploaded_at')
        return render(request, "photo_analysis/gallery.html", {"images": images})
    except Exception as e:
        logger.error(f"Error loading gallery: {str(e)}")
        return render(request, "photo_analysis/error.html", {
            "error_title": "Gallery Error",
            "error_message": "There was an error loading the gallery. Please try again later."
        })

def delete_image(request, image_id):
    """Delete an image from the gallery"""
    try:
        # Get the image or return 404 if not found
        image = get_object_or_404(UploadedImage, id=image_id)
        
        # Delete the physical file if it exists
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)
        
        # Delete the database record
        image.delete()
        
        # Redirect back to the gallery
        return redirect('gallery')
    except Exception as e:
        logger.error(f"Error deleting image: {str(e)}")
        return render(request, "photo_analysis/error.html", {
            "error_title": "Delete Error",
            "error_message": "There was an error deleting the image. Please try again later."
        })

def handler404(request, exception):
    """Handle 404 errors"""
    return render(request, "photo_analysis/error.html", {
        "error_title": "Page Not Found",
        "error_message": "The page you're looking for doesn't exist."
    }, status=404)

def handler500(request):
    """Handle 500 errors"""
    return render(request, "photo_analysis/error.html", {
        "error_title": "Server Error",
        "error_message": "Something went wrong on our end. Please try again later."
    }, status=500)
