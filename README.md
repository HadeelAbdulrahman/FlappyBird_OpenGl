
## 🐦 Flappy Bird  Game

This is a visually enhanced clone of the classic **Flappy Bird** game implemented using **Python**, **OpenGL (PyOpenGL)**, and **Pygame**. It uses OpenGL for rendering 2D textured sprites, applying transparency, and drawing game elements efficiently using the GPU.

---

### 🛠️ Technologies & Libraries Used

| Feature             | Library/Tool                                                       |
| ------------------- | ------------------------------------------------------------------ |
| **2D Rendering**    | [PyOpenGL](https://pypi.org/project/PyOpenGL/) (OpenGL, GLU, GLUT) |
| **Image Loading**   | [Pygame](https://www.pygame.org/)                                  |
| **Window & Events** | Pygame                                                             |
| **Sound Effects**   | Pygame Mixer                                                       |
| **Text Rendering**  | GLUT Bitmap Fonts                                                  |

---

### 📁 Project Structure

```
Flappy Bird/
│
├── main.py           # Main game logic using OpenGL and Pygame
├── bird.png          # Bird sprite
├── Top.png           # Top pipe sprite
├── Bottom.png        # Bottom pipe sprite
├── jump.wav          # Jump sound effect
├── fall.wav          # Fall/collision sound
├── highscore.dat     # Stores high score locally
```

---

### 🚀 How to Run

1. Make sure you have Python 3.6 or higher installed.
2. Install required libraries:

   ```bash
   pip install pygame PyOpenGL PyOpenGL_accelerate
   ```
3. Run the game:

   ```bash
   python main.py
   ```

---

### 🎮 Gameplay Instructions

* Press the **Spacebar** to make the bird flap upward.
* Avoid hitting the pipes or falling to the ground.
* The game uses OpenGL to draw each frame efficiently, using textured quads.
* Your **score** increases with each pipe passed. The highest score is saved between sessions.

---

### 🔍 OpenGL Features Used

* `glOrtho`, `glEnable(GL_BLEND)`: Set up a 2D projection and enable alpha blending.
* `glTexImage2D`: Upload Pygame image data to GPU.
* `glBegin(GL_QUADS)`: Draw textured quads for bird and pipes.
* `glutBitmapCharacter`: Render score and text using GLUT fonts.
