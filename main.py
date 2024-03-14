import os
import vlc
import sqlite3
from urllib.parse import unquote
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QSlider, QHBoxLayout
from PyQt5.QtGui import QLinearGradient, QColor, QPalette, QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve


# Create a VLC player instance
player = vlc.MediaPlayer()

# Paths to media directories
current_movie_dir = '/home/kmb/Entretainment/Movies'
current_song_dir = '/home/kmb/Entretainment/Songs'

# Function to show movies in the list
def show_movies():
	global current_movie_dir
	movies = os.listdir(current_movie_dir)
	listbox_movies.clear()
	listbox_movies.addItems(movies)

# Function to show songs in the list
def show_songs():
	global current_movie_dir
	songs = os.listdir(current_song_dir)
	listbox_songs.clear()
	listbox_songs.addItems(songs)

# Function to play media file
def play_media(file_path):
	player.set_media(vlc.Media(file_path))
	player.play()

# Function to reset directories
def reset_dirs():
	global current_movie_dir, current_song_dir
	current_movie_dir = '/home/kmb/Entretainment/Movies'
	current_song_dir = '/home/kmb/Entretainment/Songs'

# Function to set volume
def set_volume(value):
    player.audio_set_volume(value)


def play_movie():
	global current_movie_dir
	selected_movie = listbox_movies.currentItem().text()
	movie_path = os.path.join(current_movie_dir, selected_movie)
	movie_path = unquote(movie_path)
	if os.path.isdir(movie_path):
		current_movie_dir = movie_path
		listbox_movies.clear()
		show_movies()
	else:
		play_media(movie_path)

def play_song():
	global current_song_dir
	selected_song = listbox_songs.currentItem().text()
	song_path = os.path.join(current_song_dir, selected_song)
	song_path = unquote(song_path)
	if os.path.isdir(song_path):
		current_song_dir = song_path
		listbox_songs.clear()
		show_songs()
	else:
		play_media(song_path)

# Function to stop media playback
def stop_media():
    player.stop()

# Function to pause media playback
def pause_media():
	player.pause()  # Pause the player

# Function to play next media file
# Define current_directory and current_file_index as global variables
current_directory = None
current_file_index = 0

# Function to play the next media file in the same directory
def play_next_song():
	global current_file_index, current_song_dir

	if listbox_songs.currentItem():
		current_directory = current_song_dir
		current_file = listbox_songs.currentItem().text()
	else:
		return

	files = sorted(os.listdir(current_directory))
	current_file_index = (files.index(current_file) + 1) % len(files)
	next_file_path = os.path.join(current_directory, files[current_file_index])

	listbox_songs.setCurrentRow(current_file_index)
	play_song()

def play_next_movie():
	global current_file_index, current_movie_dir

	if listbox_movies.currentItem():
		current_directory = current_movie_dir
		current_file = listbox_movies.currentItem().text()
	else:
		return

	files = sorted(os.listdir(current_directory))
	current_file_index = (files.index(current_file) + 1) % len(files)
	next_file_path = os.path.join(current_directory, files[current_file_index])

	listbox_movies.setCurrentRow(current_file_index)
	play_movie()

def play_previous_song():
	global current_file_index, current_song_dir

	if listbox_songs.currentItem():
		current_directory = current_song_dir
		current_file = listbox_songs.currentItem().text()
	else:
		return

	files = sorted(os.listdir(current_directory))
	current_file_index = (files.index(current_file) - 1) % len(files)
	previous_file_path = os.path.join(current_directory, files[current_file_index])

	listbox_songs.setCurrentRow(current_file_index)
	play_song()

def play_previous_movie():
	global current_file_index, current_movie_dir

	if listbox_movies.currentItem():
		current_directory = current_movie_dir
		current_file = listbox_movies.currentItem().text()
	else:
		return

	files = sorted(os.listdir(current_directory))
	current_file_index = (files.index(current_file) - 1) % len(files)
	previous_file_path = os.path.join(current_directory, files[current_file_index])

	listbox_movies.setCurrentRow(current_file_index)
	play_movie()


# Initialize PyQt application
app = QApplication([])

# Create a button
reset_button = QPushButton('Reset Directories')

# Connect the button to the function
reset_button.clicked.connect(reset_dirs)

# Create a slider for volume control
volume_slider = QSlider(Qt.Horizontal)
volume_slider.setMinimum(0)
volume_slider.setMaximum(100)
volume_slider.setValue(50)  # Set initial volume to 50%
volume_slider.valueChanged.connect(set_volume)

# Create main window
window = QWidget()
layout = QVBoxLayout()
window.setLayout(layout)

# Create a QPixmap object with the path to your image
background = QPixmap('/home/kmb/Desktop/My_projects/entretainment_manager/background.jpg')

# Create a QBrush object with the QPixmap
brush = QBrush(background)

# Create a QPalette object
palette = QPalette()

# Set the QBrush as the background of the QPalette
palette.setBrush(QPalette.Background, brush)

# Set the QPalette as the palette of the window
window.setPalette(palette)

window.resize(1200, 800)  # Set the default resolution to 1200x800

# Add the slider to the layout
layout.addWidget(volume_slider)

# Create labels, listboxes, and buttons for songs
font = QFont("Arial", 24)  # Increase the font size to 24

# Create a horizontal box layout
button_layout = QHBoxLayout()

pause_button = QPushButton('⏸️')  # Pause emoji
pause_button.setFont(font)
reset_button = QPushButton('🔄')  # Loading emoji
reset_button.setFont(font)
stop_button = QPushButton('⏹️')  # Stop emoji
stop_button.setFont(font)

# Connect the buttons to their functions
pause_button.clicked.connect(pause_media)
reset_button.clicked.connect(reset_dirs)
stop_button.clicked.connect(stop_media)

# Add the buttons to the layout
button_layout.addWidget(pause_button)
button_layout.addWidget(reset_button)
button_layout.addWidget(stop_button)

# Add the button layout to the main layout
font = QFont("Arial", 18)  # Increase the font size to 24

layout.addLayout(button_layout)

label_songs = QLabel("Songs")
label_songs.setFont(font)
label_songs.setStyleSheet("color: white")
layout.addWidget(label_songs)

listbox_songs = QListWidget()
listbox_songs.setFont(font)
listbox_songs.itemClicked.connect(play_song)
layout.addWidget(listbox_songs)

button_songs = QPushButton("Show Songs")
button_songs.setFont(font)
button_songs.clicked.connect(show_songs)
layout.addWidget(button_songs)

# Create next and previous buttons for songs
next_song_button = QPushButton('➡️')
next_song_button.setFont(font)
prev_song_button = QPushButton('⬅️')
prev_song_button.setFont(font)

# Connect the buttons to their functions
next_song_button.clicked.connect(play_next_song)
prev_song_button.clicked.connect(play_previous_song)

# Create a horizontal layout for the song buttons
song_button_layout = QHBoxLayout()
song_button_layout.addWidget(prev_song_button)
song_button_layout.addWidget(next_song_button)

# Add the song button layout to the main layout
layout.addLayout(song_button_layout)

label_movies = QLabel("Movies")
label_movies.setFont(font)
label_movies.setStyleSheet("color: white")
layout.addWidget(label_movies)

listbox_movies = QListWidget()
listbox_movies.setFont(font)
listbox_movies.itemClicked.connect(play_movie)
layout.addWidget(listbox_movies)

button_movies = QPushButton("Show Movies")
button_movies.setFont(font)
button_movies.clicked.connect(show_movies)
layout.addWidget(button_movies)

# Create next and previous buttons for movies
next_movie_button = QPushButton('➡️')
next_movie_button.setFont(font)
prev_movie_button = QPushButton('⬅️')
prev_movie_button.setFont(font)

# Connect the buttons to their functions
next_movie_button.clicked.connect(play_next_movie)
prev_movie_button.clicked.connect(play_previous_movie)

# Create a horizontal layout for the movie buttons
movie_button_layout = QHBoxLayout()
movie_button_layout.addWidget(prev_movie_button)
movie_button_layout.addWidget(next_movie_button)

# Add the movie button layout to the main layout
layout.addLayout(movie_button_layout)

# Start the application
window.show()

# Create animations for labels' font size
animations = [QPropertyAnimation(label, b"font") for label in [label_songs, label_movies]]
for animation in animations:
	animation.setDuration(1000)
	animation.setStartValue(QFont("Arial", 14))
	animation.setEndValue(QFont("Arial", 20))
	animation.setEasingCurve(QEasingCurve.InOutBounce)
	animation.start()

# Execute the application
app.exec_()
