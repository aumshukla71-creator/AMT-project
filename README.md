# Solar System 1 FPS Video Generator

An optimized Python automation tool that generates a **2-minute and 40-second (160 seconds total)** educational video of our solar system with a synchronized AI narrative voiceover. 

To overcome heavy memory allocation limits (`ArrayMemoryError`) when processing ultra-high-resolution images, this script uses **OpenCV** to stream and scale frame blocks smoothly inside a 1080p profile while using **gTTS (Google Text-to-Speech)** to generate clear planetary descriptions.

## 🚀 Features
* **Perfect 2:40 Timeline Alignment:** Automatically maps the introduction scene to 16 seconds and all 8 primary planets to 18 seconds each.
* **Memory Shield Engine:** Pre-scales large assets frame-by-frame using OpenCV matrix borders to prevent RAM crashes during encoding.
* **Media Player Compliance:** Outputs standard `.mp4` structures at a smooth 24 FPS baseline, resolving the `0x80004005` playback errors common in Windows Media Player with low frame-rate files.

## 📁 Repository Structure
Place your script and source `.jpg` graphics directly inside your working directory:
```text
├── solar_system.jpg  (Intro Scene Overlay)
├── mercury.jpg
├── venus.jpg
├── earth.jpg
├── mars.jpg
├── jupiter.jpg
├── saturn.jpg
├── uranus.jpg
├── neptune.jpg
└── generate_video.py
```

## ⚙️ Installation & Requirements

Ensure you have Python 3.12+ installed, then install the required framework libraries through your terminal:

```bash
pip install gtts opencv-python moviepy
```

## 🛠️ How to Run

1. Open your Command Prompt (`cmd`) or terminal.
2. Navigate to your project directory:
   ```bash
   cd path/to/your/folder
   ```
3. Run the generator engine script:
   ```bash
   python generate_video.py
   ```

## 📝 Script Breakdown
The pipeline utilizes three structural core execution phases:
1. **Visual Raster Canvas:** OpenCV handles structural graphic streaming to scale assets safely into letterboxed high-definition frames without saturating system RAM.
2. **Audio Wave Compiler:** The system reads the target timeline requirements and synthesizes clean narration audio blocks dynamically via the standard Python `wave` array wrapper.
3. **Muxing Multiplexer:** MoviePy acts strictly at the final step as a safe multiplexer to bind the completed image stream and compiled audio tracks into a unified `.mp4` file.
