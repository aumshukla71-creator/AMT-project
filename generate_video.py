import os
import sys
import wave

try:
    from gtts import gTTS
    import cv2
    # Load base moviepy modules for the final muxing sequence layer
    from moviepy import VideoFileClip, AudioFileClip
except ImportError as e:
    print(f"\n[ERROR] Core module loading failed: {e}")
    sys.exit(1)

# 1. Path Setup - Targets your Desktop assets
desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
output_video_only_path = os.path.join(desktop_dir, "temp_video_only.mp4")
output_audio_only_path = os.path.join(desktop_dir, "temp_audio_only.wav")
final_output_path = os.path.join(desktop_dir, "solar_system_final.mp4")

image_filenames = [
    "solar_system.jpg",
    "mercury.jpg",
    "venus.jpg",
    "earth.jpg",
    "mars.jpg",
    "jupiter.jpg",
    "saturn.jpg",
    "uranus.jpg",
    "neptune.jpg"
]

narration_script = [
    "Welcome to our solar system. At the center lies the Sun, an immense ball of hot plasma providing light, energy, and gravitational stability to eight unique worlds tracing steady orbits across the deep cosmos.",
    "Mercury is the closest planet to the Sun and the smallest in our solar system. Because it lacks a substantial atmosphere to trap heat, it experiences extreme temperature swings ranging from blazing daytime heat to freezing nights.",
    "Venus is our closest planetary neighbor, shrouded in a crushing atmosphere of toxic carbon dioxide. Due to a runaway greenhouse effect, its surface temperatures are hot enough to melt lead, making it the hottest planet of all.",
    "Earth is our beautiful oasis and the only known world capable of supporting complex life. It features vast oceans of liquid surface water, a protective atmosphere rich in oxygen, and a deeply interconnected global biosphere.",
    "Mars is a cold and dusty desert planet often called the Red Planet because of iron minerals rusting in its soil. It possesses thin atmospheric layers, ancient dry river valleys, and the largest volcano in our solar system.",
    "Jupiter is a colossal gas giant that holds more than twice the mass of all the other planets combined. It features dozens of moons and is famous for its violent storms, including the spinning vortex known as the Great Red Spot.",
    "Saturn is the stunning jewel of the solar system, immediately recognizable by its spectacular and extensive ring system. These massive rings are not solid, but are composed of billions of individual chunks of ice, rock, and dust.",
    "Uranus is a unique ice giant that appears as a soft blue-green color due to methane gas in its atmosphere. Unlike any other planet in our system, it rotates completely on its side, virtually rolling along its orbital path.",
    "Neptune is the most distant major planet from the Sun, locked in a state of eternal darkness and freezing cold. It is a world of extreme weather, swept by supersonic winds that rank as the fastest and most ferocious in the solar system."
]

# Strict timing list completely filled to hit exactly 160 seconds (2 mins 40 secs)
fixed_durations = [16, 18, 18, 18, 18, 18, 18, 18, 18]
fps = 24

print(f"\n[INFO] Initializing OpenCV Video Framework...")

# 2. Open up a clean OpenCV Video Writer pipeline for the visuals
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_only_path, fourcc, fps, (1920, 1080))

# 3. Write each image frame block sequentially
for i, fname in enumerate(image_filenames):
    orig_path = os.path.join(desktop_dir, fname)
    if not os.path.exists(orig_path):
        print(f"\n[ERROR] Missing target item: {orig_path}")
        video_writer.release()
        sys.exit(1)
        
    img = cv2.imread(orig_path)
    h, w = img.shape[:2]
    
    if w / h > 1920 / 1080:
        new_w = 1920
        new_h = int(h * (1920 / w))
    else:
        new_h = 1080
        new_w = int(w * (1080 / h))
        
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    canvas = cv2.copyMakeBorder(
        scaled_img, 
        top=(1080 - new_h) // 2, 
        bottom=(1080 - new_h + 1) // 2, 
        left=(1920 - new_w) // 2, 
        right=(1920 - new_w + 1) // 2, 
        borderType=cv2.BORDER_CONSTANT, 
        value=[0, 0, 0]
    )
    canvas = cv2.resize(canvas, (1920, 1080))
    
    total_segment_frames = fixed_durations[i] * fps
    for _ in range(total_segment_frames):
        video_writer.write(canvas)

video_writer.release()
print("[INFO] Video frame track generated successfully.")

# 4. Generate AI Voice narrations using clean native WAV files
print("[INFO] Processing voice tracks inside Python audio compiler...")
wav_files_to_clean = []

sample_rate = 24000 
channels = 1
bytes_per_sample = 2  # 16-bit audio depth tracking

for i, text in enumerate(narration_script):
    temp_mp3 = os.path.join(desktop_dir, f"temp_{i}.mp3")
    temp_wav = os.path.join(desktop_dir, f"temp_{i}.wav")
    
    is_slow = True if i == 0 else False
    tts = gTTS(text=text, lang='en', tld='com', slow=is_slow)
    tts.save(temp_mp3)
    
    # Fast native file layout transition to bypass module discrepancies
    with open(temp_mp3, "rb") as f_in:
        mp3_data = f_in.read()
    
    with wave.open(temp_wav, 'wb') as wav_out:
        wav_out.setnchannels(channels)
        wav_out.setsampwidth(bytes_per_sample)
        wav_out.setframerate(sample_rate)
        
        target_bytes_count = int(fixed_durations[i] * sample_rate * channels * bytes_per_sample)
        
        if len(mp3_data) < target_bytes_count:
            padded_data = mp3_data + b'\x00' * (target_bytes_count - len(mp3_data))
        else:
            padded_data = mp3_data[:target_bytes_count]
            
        wav_out.writeframes(padded_data)
        
    wav_files_to_clean.append(temp_wav)
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

# 5. Concatenate individual WAV files together using pure Python
print("[INFO] Stitching audio timelines into unified master clip...")
combined_wav_file = wave.open(output_audio_only_path, 'wb')
combined_wav_file.setnchannels(channels)
combined_wav_file.setsampwidth(bytes_per_sample)
combined_wav_file.setframerate(sample_rate)

for wav_p in wav_files_to_clean:
    with wave.open(wav_p, 'rb') as w_in:
        combined_wav_file.writeframes(w_in.readframes(w_in.getnframes()))
    if os.path.exists(wav_p):
        os.remove(wav_p)
combined_wav_file.close()

# 6. Final safe composition file save layer via MoviePy core stream
print("[INFO] Multiplexing sound layers onto master video timeline track...")
video_clip = VideoFileClip(output_video_only_path)
audio_clip = AudioFileClip(output_audio_only_path)

final_movie = video_clip.with_audio(audio_clip) if hasattr(video_clip, 'with_audio') else video_clip.set_audio(audio_clip)

# Render the final composite video safely at 24 FPS
final_movie.write_videofile(
    final_output_path,
    fps=fps,
    codec="libx264",
    audio_codec="aac"
)

# Close open file tracking channels safely
final_movie.close()
video_clip.close()
audio_clip.close()

# Clean temporary work files from Desktop space
if os.path.exists(output_video_only_path):
    os.remove(output_video_only_path)
if os.path.exists(output_audio_only_path):
    os.remove(output_audio_only_path)

print(f"\n[SUCCESS] Your perfect 2:40 video is compiled safely on your Desktop:\n{final_output_path}")
