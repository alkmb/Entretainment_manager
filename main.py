import os
import vlc
import sqlite3
from urllib.parse import unquote
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel
from PyQt5.QtGui import QLinearGradient, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

# Initialize SQLite database connection
conn = sqlite3.connect('media_library.db')
c = conn.cursor()

# Create a VLC player instance
player = vlc.MediaPlayer()

# Function to show movies in the list
def show_movies():
    movies = os.listdir(current_movie_dir)
    listbox_movies.clear()
    listbox_movies.addItems(movies)

# Function to show songs in the list
def show_songs():
    songs = os.listdir(current_song_dir)
    listbox_songs.clear()
    listbox_songs.addItems(songs)

# Function to play media file
def play_media(file_path):
    player.set_media(vlc.Media(file_path))
    player.play()

# Paths to media directories
current_movie_dir = '/home/akambou/Entretainment/Movies'
current_song_dir = '/home/akambou/Entretainment/Songs'

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

# Initialize PyQt application
app = QApplication([])

# Create main window
window = QWidget()
layout = QVBoxLayout()
window.setLayout(layout)

# Set background gradient
gradient = QLinearGradient(0, 0, window.width(), window.height())
gradient.setColorAt(0, QColor('blue'))
gradient.setColorAt(1, QColor('purple'))
palette = QPalette()
palette.setBrush(QPalette.Background, gradient)
window.setPalette(palette)

# Create labels, listboxes, and buttons for songs
font = QFont("Arial", 14)

label_songs = QLabel("Songs")
label_songs.setFont(font)
label_songs.setStyleSheet("color: white")
layout.addWidget(label_songs)

listbox_songs = QListWidget()
listbox_songs.itemClicked.connect(play_song)
layout.addWidget(listbox_songs)

button_songs = QPushButton("Show Songs")
button_songs.clicked.connect(show_songs)
layout.addWidget(button_songs)

# Create labels, listboxes, and buttons for movies
label_movies = QLabel("Movies")
label_movies.setFont(font)
label_movies.setStyleSheet("color: white")
layout.addWidget(label_movies)

listbox_movies = QListWidget()
listbox_movies.itemClicked.connect(play_movie)
layout.addWidget(listbox_movies)

button_movies = QPushButton("Show Movies")
button_movies.clicked.connect(show_movies)
layout.addWidget(button_movies)

# Create stop button
button_stop = QPushButton("Stop")
button_stop.clicked.connect(stop_media)
layout.addWidget(button_stop)

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
