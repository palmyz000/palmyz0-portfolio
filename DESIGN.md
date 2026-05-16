# DESIGN.md (Web Design & UI/UX Standards)

## UI/UX Core Theme
The overall design of the website focuses on a **"Developer / Hacker / Terminal"** aesthetic that looks professional, mysterious, and intriguing, perfectly suited for a Data Scientist and AI Engineer role:
- **Color Palette**: Uses a dark "Cool Tone" background (`#020617`, `#0f172a`, `#1e293b`) and vibrant Neon colors (Cyan/Blue `#0ea5e9` and Emerald Green `#10b981`) to highlight key areas or buttons, creating strong contrast (Accent colors).
- **Typography**: Employs Monospace fonts like `JetBrains Mono` combined with modern Sans-Serif fonts like `Inter` and `Kanit` (for Thai language) to convey a strong developer and programmer identity.
- **Aesthetic Feel**: Incorporates subtle glow shadow effects, light glassmorphism, text gradients, and a Terminal Simulator-style loading screen.

## Layout Structure
- **Multi-page Architecture**: The mandatory structure for this project is a **"Multi-page Website"**. Content must be distinctly separated into different pages (e.g., About, Experience, Projects, Skills). **Do NOT merge everything into one long page or convert it into a Single-page scrolling layout under any circumstances!**
- **Navigation & Framing**: Uses a Fixed Navigation bar at the top with a Backdrop Blur effect. The menu features a Python Function Definition display style (e.g., `def about():`). A Footer must always be present at the bottom.
- **Animation System**: Supports basic animation systems such as Fade-in effects upon page load, Hover effects on buttons and links, and a Loading Screen simulating code execution commands when initially entering the website.

## Component Rules
- **UI Framework**: All HTML code must strictly use Utility-first classes from **Tailwind CSS** for styling.
- **Forms & Inputs (e.g., Contact Form)**: Input box borders should be rounded. Backgrounds should be a dark tone slightly different from the main background to distinguish layers. Upon Hover or Focus, they should display an accent color ring glow.
- **Buttons**: Main Call-to-Action buttons (like Resume or Send Message) must have smooth transition effects, box-shadow glows, and should include icons with subtle micro-animations when the user hovers over them.
- **Icons**: Use Font Awesome for icons throughout the project.
