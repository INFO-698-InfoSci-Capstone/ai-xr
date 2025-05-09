# An exploratory Approach to AI-Powered Texture Synthesis for Furnitures

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview
This project is an AI-powered texture synthesis platform for generating, previewing, and applying material textures (such as plastic, fabric, metal, etc.) to objects in images, with a focus on XR (Extended Reality) and design applications.

---

## Future Work

- **Room-scale Texture Application:**  
  Extend the platform to apply generated textures to entire rooms or multiple objects within a room, rather than just individual pieces of furniture as is currently supported.

- **Dockerization & Cloud Deployment:**  
  Create Dockerfiles and deployment scripts to make the platform easy to deploy on any server or cloud provider.

- **AR/VR Integration:**  
  Add support for real-time texture preview and interaction in Augmented Reality (AR) and Virtual Reality (VR) environments, possibly using WebXR or similar technologies.

- **Custom Texture Upload & Editing:**  
  Enable users to upload their own textures or edit generated textures (e.g., adjust color, scale, or pattern).


---

The system consists of:
- **Frontend** (in `project/`): A modern web app for users to select, preview, and apply textures to segmented objects in images.
- **Backend** (in `texture_generation/` and `segmentation_app/`): Python services for texture generation (using PIL and Stable Diffusion), instance segmentation, and database management.

---

## File Organization

```
project/                      # Frontend web application (React, Vite, Tailwind)
?
??? src/                      # React source code (components, pages, hooks, etc.)
??? public/textures/          # Generated texture images (used by frontend)
??? index.html                # Main HTML entry point
??? package.json              # Frontend dependencies and scripts
??? ...                       # Other frontend config files

texture_generation/           # Backend for texture generation and management
?
??? app.py                    # Main backend API (Flask or FastAPI)
??? create_textures.py        # Script for generating procedural textures
??? requirements.txt          # Python dependencies
??? models.py                 # Database models
??? utils.py                  # Utility functions for texture generation
??? static/                   # Static files (if any)
??? init_db.py / .sql         # Database initialization scripts
??? update_data.sql           # SQL scripts for updating texture data
??? ...                       # Other backend scripts and helpers

README.md                     # Project documentation
LICENSE                       # License information
CONDUCT.md                    # Code of conduct
```

---

## Frontend (`project/`)
- Built with React, Vite, and Tailwind CSS.
- Allows users to:
  - View and select from a library of material textures
  - Apply generated textures on segmented objects of furniture
  - Interact with backend APIs for texture application
- To run:
  ```bash
  cd project
  npm install
  npm run dev
  ```
  The app will be available at `http://localhost:5173` by default.

---

## Backend (`texture_generation/`)
- Python backend for:
  - Generating textures using PIL (procedural) and Stable Diffusion (AI-generated)
  - Managing texture metadata and images
  - Database scripts for PostgreSQL
- Key files:
  - `app.py`: Main backend API (Flask or FastAPI)
  - `requirements.txt`: Python dependencies
- To run texture generation:
  ```bash
  cd texture_generation
  pip install -r requirements.txt
  ```
- Stable Diffusion: Used for advanced/AI-generated textures. Requires model weights and GPU support.

---


## License
See LICENSE file for details.

---




        

