import os
import sys
import random
import numpy as np

try:
    from gtts import gTTS
    import cv2
    from moviepy import VideoFileClip, AudioFileClip, concatenate_audioclips
except ImportError as e:
    print(f"\n[ERROR] Core module loading failed: {e}")
    print("Please run: pip install gtts opencv-python moviepy")
    sys.exit(1)

# 1. Path Configuration
desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
output_video_only_path = os.path.join(desktop_dir, "temp_animated_video.mp4")
final_output_path = os.path.join(desktop_dir, "solar_system_animated.mp4")

planets_data = [
    {"file": "solar_system.png", "label": "THE SOLAR SYSTEM"},
    {"file": "mercury.png",      "label": "MERCURY"},
    {"file": "venus.png",        "label": "VENUS"},
    {"file": "earth.png",        "label": "EARTH"},
    {"file": "mars.png",         "label": "MARS"},
    {"file": "jupiter.png",      "label": "JUPITER"},
    {"file": "saturn.png",       "label": "SATURN"},
    {"file": "uranus.png",       "label": "URANUS"},
    {"file": "neptune.png",      "label": "NEPTUNE"}
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

fps = 24

# -------------------------------------------------------------
# PHASE 1: GENERATE AI NARRATION & TIMINGS
# -------------------------------------------------------------
print("\n[INFO] Phase 1: Generating AI voice tracks and calculating dynamic slide timings...")
audio_clips = []
durations = []

for i, text in enumerate(narration_script):
    temp_mp3 = os.path.join(desktop_dir, f"temp_{i}.mp3")
    tts = gTTS(text=text, lang='en', tld='com', slow=(i == 0))
    tts.save(temp_mp3)
    
    a_clip = AudioFileClip(temp_mp3)
    durations.append(a_clip.duration)
    audio_clips.append(a_clip)

# -------------------------------------------------------------
# PHASE 2: LAUNCH TWINKLING STARFIELD BACKDROP ENGINE
# -------------------------------------------------------------
print("\n[INFO] Phase 2: Compiling real-time shimmering minimal starfield layouts...")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_only_path, fourcc, fps, (1920, 1080))

h, w = 1080, 1920
r_center_x, r_center_y = w // 2, h // 2
radius = 320

# Create sphere coordinates shading maps
y_indices, x_indices = np.ogrid[-radius:radius, -radius:radius]
circle_mask = x_indices**2 + y_indices**2 <= radius**2
shading = 0.4 + 0.6 * np.maximum(0, (x_indices + np.sqrt(np.maximum(0, radius**2 - x_indices**2 - y_indices**2))) / (radius * 1.414))

for i, target in enumerate(planets_data):
    img_path = os.path.join(desktop_dir, target["file"])
    if not os.path.exists(img_path):
        print(f"\n[ERROR] Missing file on Desktop: {target['file']}")
        video_writer.release()
        sys.exit(1)
        
    img_rgb = cv2.imread(img_path, cv2.IMREAD_COLOR)
    total_frames = int(durations[i] * fps)
    
    print(f"[ANIMATING] Rendering twinkling space backdrop for: {target['label']}...")
    
    if i == 0:
        base_canvas = cv2.resize(img_rgb, (2400, 1350), interpolation=cv2.INTER_AREA)
        for f in range(total_frames):
            p = f / total_frames
            z = 1.0 - (p * 0.10)
            cw, ch = int(2400 * z), int(1350 * z)
            sx, sy = int((2400 - cw) * 0.5 * p), int((1350 - ch) * 0.5 * p)
            frame = cv2.resize(base_canvas[sy:sy+ch, sx:sx+cw], (1920, 1080))
            cv2.putText(frame, target["label"], (100, 980), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 4, cv2.LINE_AA)
            video_writer.write(frame)
    else:
        # Center crop to make rectangular PNGs into perfect 1:1 squares
        img_h, img_w = img_rgb.shape[:2]
        min_dim = min(img_h, img_w)
        cx, cy = (img_w - min_dim) // 2, (img_h - min_dim) // 2
        cropped_texture = img_rgb[cy:cy+min_dim, cx:cx+min_dim]
        
        sphere_face = cv2.resize(cropped_texture, (radius*2, radius*2), interpolation=cv2.INTER_AREA)
        shaded_sphere = (sphere_face * shading[:, :, np.newaxis]).astype(np.uint8)
        
        for f in range(total_frames):
            frame = np.zeros((h, w, 3), dtype=np.uint8)
            
            # Absolute Fix: Use a dynamic combination seed of (planet_index + frame_number) 
            # to calculate slight, fluid brightness shifts so the stars actively sparkle!
            np.random.seed(i * 1000)
            
            for size, base_brightness in [(2, 140), (3, 200), (4, 240)]:
                num_stars = 25 if size == 2 else (12 if size == 3 else 4)
                sx = np.random.randint(40, w - 40, num_stars)
                sy = np.random.randint(40, h - 40, num_stars)
                
                for idx, (x_pos, y_pos) in enumerate(zip(sx, sy)):
                    if not (r_center_x - 380 < x_pos < r_center_x + 380 and r_center_y - 380 < y_pos < r_center_y + 380):
                        # Use a math sine wave equation over time to cycle the star twinkle cleanly
                        twinkle_shift = int(35 * np.sin((f + idx * 7) * 0.45))
                        current_brightness = min(255, max(80, base_brightness + twinkle_shift))
                        
                        cv2.circle(frame, (x_pos, y_pos), size, (current_brightness, current_brightness, current_brightness), -1, cv2.LINE_AA)
            
            # 1. Saturn Behind-Planet Ring Layer
            if i == 6:
                cv2.ellipse(frame, (r_center_x, r_center_y), (600, 110), -15, 182, 358, (120, 160, 190), 28, cv2.LINE_AA)
                cv2.ellipse(frame, (r_center_x, r_center_y), (540, 85), -15, 182, 358, (170, 210, 235), 16, cv2.LINE_AA)
                cv2.ellipse(frame, (r_center_x, r_center_y), (460, 65), -15, 182, 358, (80, 100, 130), 10, cv2.LINE_AA)
            
            # 2. Paste Core Planet Mask onto canvas
            frame[r_center_y - radius : r_center_y + radius, r_center_x - radius : r_center_x + radius][circle_mask] = shaded_sphere[circle_mask]
            
            # 3. Saturn Front-Planet Wrapping Ring Layer
            if i == 6:
                cv2.ellipse(frame, (r_center_x, r_center_y), (600, 110), -15, 2, 178, (120, 160, 190), 28, cv2.LINE_AA)
                cv2.ellipse(frame, (r_center_x, r_center_y), (540, 85), -15, 2, 178, (170, 210, 235), 16, cv2.LINE_AA)
                cv2.ellipse(frame, (r_center_x, r_center_y), (460, 65), -15, 2, 178, (80, 100, 130), 10, cv2.LINE_AA)
                
            cv2.putText(frame, target["label"], (100, 980), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 4, cv2.LINE_AA)
            video_writer.write(frame)

video_writer.release()
print("[INFO] Video rendering pipeline closed successfully.")

# -------------------------------------------------------------
# PHASE 3: MULTIPLEX MASTER TRACKS TOGETHER
# -------------------------------------------------------------
print("\n[INFO] Phase 3: Multiplexing sound layers onto master video track...")
combined_audio = concatenate_audioclips(audio_clips)
video_clip = VideoFileClip(output_video_only_path)

final_movie = video_clip.with_audio(combined_audio) if hasattr(video_clip, 'with_audio') else video_clip.set_audio(combined_audio)
final_movie.write_videofile(final_output_path, fps=fps, codec="libx264", audio_codec="aac")

final_movie.close()
video_clip.close()
combined_audio.close()

if os.path.exists(output_video_only_path):
    os.remove(output_video_only_path)
for i in range(len(narration_script)):
    p = os.path.join(desktop_dir, f"temp_{i}.mp3")
    if os.path.exists(p):
        os.remove(p)

print(f"\n[SUCCESS] Your elegant animated video is complete! Saved directly on your Desktop:\n{final_output_path}")
