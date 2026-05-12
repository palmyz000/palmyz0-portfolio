(function() {
    let isReady = false;
    let pendingShow = false;
    let showRobotInstance;

    window.showRobot = function() {
        if (isReady && showRobotInstance) {
            showRobotInstance();
        } else {
            pendingShow = true;
        }
    };

    window.addEventListener('DOMContentLoaded', () => {
        // SVG Markup for Wall-E style robot
        const robotSVG = `
            <svg width="60" height="70" viewBox="0 0 60 70" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="2" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#f59e0b" />
                        <stop offset="100%" stop-color="#d97706" />
                    </linearGradient>
                </defs>
                
                <g id="robot-group">
                    <!-- Tracks -->
                    <rect x="5" y="55" width="15" height="12" rx="4" fill="#334155" />
                    <rect x="40" y="55" width="15" height="12" rx="4" fill="#334155" />
                    <rect x="10" y="58" width="40" height="8" rx="2" fill="#1e293b" />
                    
                    <!-- Neck -->
                    <rect x="26" y="25" width="8" height="15" fill="#64748b" />
                    
                    <!-- Body -->
                    <rect id="robot-body" x="12" y="35" width="36" height="22" rx="3" fill="url(#bodyGrad)" stroke="#b45309" stroke-width="2"/>
                    <rect x="18" y="40" width="24" height="12" fill="#475569" opacity="0.3" rx="1" />
                    <circle cx="22" cy="46" r="2" fill="#ef4444" id="status-led" filter="url(#glow)" />
                    
                    <!-- Head -->
                    <g id="robot-head" class="robot-head-anim">
                        <rect x="14" y="10" width="16" height="14" rx="3" fill="#475569" stroke="#1e293b" stroke-width="2" />
                        <rect x="30" y="10" width="16" height="14" rx="3" fill="#475569" stroke="#1e293b" stroke-width="2" />
                        <circle cx="22" cy="17" r="4" fill="#0f172a" />
                        <circle cx="38" cy="17" r="4" fill="#0f172a" />
                        <circle cx="22" cy="17" r="2" fill="#38bdf8" id="eye-left" filter="url(#glow)" />
                        <circle cx="38" cy="17" r="2" fill="#38bdf8" id="eye-right" filter="url(#glow)" />
                    </g>

                    <!-- Arm & Broom -->
                    <g id="robot-arm">
                        <path d="M 48 45 Q 60 45, 55 60" fill="none" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
                        <line x1="50" y1="50" x2="60" y2="70" stroke="#b45309" stroke-width="2" />
                        <polygon points="56,70 64,70 66,75 54,75" fill="#fcd34d" />
                    </g>
                </g>
            </svg>
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes robot-bob {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-2px); }
            }
            @keyframes sweep {
                0%, 100% { transform: rotate(0deg); transform-origin: 55px 60px; }
                50% { transform: rotate(-15deg); transform-origin: 55px 60px; }
            }
            @keyframes blink {
                0%, 96%, 98%, 100% { transform: scaleY(1); }
                97% { transform: scaleY(0.1); }
            }
            .robot-walking #robot-group { animation: robot-bob 0.5s infinite; }
            .robot-walking #robot-arm { animation: sweep 0.5s infinite; }
            .robot-cleaning #robot-arm { animation: sweep 0.2s infinite; } /* Faster sweep when stopped */
            .robot-head-anim { transform-origin: 30px 17px; animation: blink 4s infinite; }
        `;
        document.head.appendChild(style);

        // Container wrapper for physics
        const wrapper = document.createElement('div');
        Object.assign(wrapper.style, {
            position: 'fixed',
            zIndex: '9999',
            top: '0', left: '0',
            width: '60px', height: '70px',
            pointerEvents: 'none', // wrapper doesn't catch clicks
            display: 'none', // Hidden by default
            opacity: '0',
            transition: 'opacity 0.8s ease-in-out'
        });

        const container = document.createElement('div');
        container.innerHTML = robotSVG;
        Object.assign(container.style, {
            width: '100%', height: '100%',
            cursor: 'grab',
            userSelect: 'none',
            touchAction: 'none',
            pointerEvents: 'auto',
            transformOrigin: 'center center'
        });
        
        wrapper.appendChild(container);

        // Speech bubble
        const bubble = document.createElement('div');
        Object.assign(bubble.style, {
            position: 'fixed',
            padding: '8px 12px',
            background: 'rgba(15, 23, 42, 0.95)',
            color: '#38bdf8',
            border: '1px solid #38bdf8',
            borderRadius: '8px',
            borderBottomLeftRadius: '0',
            fontFamily: 'monospace',
            fontSize: '12px',
            fontWeight: 'bold',
            boxShadow: '0 0 10px rgba(56, 189, 248, 0.3)',
            zIndex: '10000',
            opacity: '0',
            pointerEvents: 'none',
            transition: 'opacity 0.3s',
            whiteSpace: 'nowrap'
        });
        
        document.body.appendChild(wrapper);
        document.body.appendChild(bubble);

        // Expose function to show robot
        showRobotInstance = function() {
            if (wrapper.style.display === 'none') {
                wrapper.style.display = 'block';
                // Small delay to trigger transition
                setTimeout(() => {
                    wrapper.style.opacity = '1';
                }, 50);
            }
        };

        isReady = true;
        if (pendingShow) showRobotInstance();

        // Audio System (Vacuum noise)
        let isMuted = false;
        let audioCtx;
        let noiseGain;

        const dMute = document.getElementById('desktop-mute-btn');
        const mMute = document.getElementById('mobile-mute-btn');
        const toggleMute = () => {
            isMuted = !isMuted;
            const iconClass = isMuted ? 'fa-volume-mute text-red-400' : 'fa-volume-up';
            if(dMute) dMute.innerHTML = `<i class="fas ${iconClass} text-lg"></i>`;
            if(mMute) mMute.innerHTML = `<i class="fas ${iconClass} text-lg"></i>`;
            if(isMuted && noiseGain) noiseGain.gain.setTargetAtTime(0, audioCtx.currentTime, 0.1);
        };
        if(dMute) dMute.addEventListener('click', toggleMute);
        if(mMute) mMute.addEventListener('click', toggleMute);

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                noiseGain = audioCtx.createGain();
                noiseGain.gain.value = 0;
                noiseGain.connect(audioCtx.destination);
                
                const bufferSize = audioCtx.sampleRate * 2;
                const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                const output = buffer.getChannelData(0);
                let lastOut = 0;
                for (let i = 0; i < bufferSize; i++) {
                    const white = Math.random() * 2 - 1;
                    output[i] = (lastOut + (0.02 * white)) / 1.02;
                    lastOut = output[i];
                    output[i] *= 3.5; 
                }
                const noiseSource = audioCtx.createBufferSource();
                noiseSource.buffer = buffer;
                noiseSource.loop = true;
                
                const filter = audioCtx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 300;
                
                noiseSource.connect(filter);
                filter.connect(noiseGain);
                noiseSource.start();
            }
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function setVacuumSound(on) {
            if(!audioCtx || isMuted) return;
            if(on) {
                noiseGain.gain.setTargetAtTime(0.03, audioCtx.currentTime, 0.5); // Very low volume
            } else {
                noiseGain.gain.setTargetAtTime(0, audioCtx.currentTime, 0.1);
            }
        }

        // Physics State
        let x = window.innerWidth / 2;
        let y = window.innerHeight - 70;
        let vx = 0;
        let vy = 0;
        let rotation = 0;
        let vrot = 0;
        
        let lastMouseX = 0;
        let lastMouseY = 0;
        
        let state = 'walk'; // walk, clean, drag, fall, tumble, getup
        let walkDirection = 1;
        let walkTimer = 0;
        let baseSpeed = 0.4; // slower walking
        
        const eyes = [document.getElementById('eye-left'), document.getElementById('eye-right')];
        const led = document.getElementById('status-led');

        let bubbleTimeout;
        function speak(text, duration = 4000) {
            bubble.textContent = text;
            bubble.style.opacity = '1';
            
            clearTimeout(bubbleTimeout);
            bubbleTimeout = setTimeout(() => {
                bubble.style.opacity = '0';
            }, duration);
        }

        // Interaction
        const startDrag = (clientX, clientY) => {
            initAudio();
            setVacuumSound(false);
            state = 'drag';
            container.style.cursor = 'grabbing';
            container.classList.remove('robot-walking', 'robot-cleaning');
            
            eyes.forEach(eye => { eye.setAttribute('fill', '#ef4444'); eye.setAttribute('r', '3'); });
            led.setAttribute('fill', '#ef4444');
            
            lastMouseX = clientX;
            lastMouseY = clientY;
            vx = 0; vy = 0; vrot = 0;
            
            speak("Whoa! Put me down!", 3000);
        };

        const doDrag = (clientX, clientY) => {
            if (state !== 'drag') return;
            
            // Calculate velocity based on mouse delta
            vx = (clientX - lastMouseX) * 0.5;
            vy = (clientY - lastMouseY) * 0.5;
            
            x = clientX - 30; // center to mouse
            y = clientY - 35;
            
            // Swing effect while dragging
            rotation = Math.min(Math.max(vx * 2, -45), 45); 
            
            lastMouseX = clientX;
            lastMouseY = clientY;
        };

        const endDrag = () => {
            if (state !== 'drag') return;
            state = 'fall';
            container.style.cursor = 'grab';
            
            // Boost falling velocity slightly to feel weighty
            vy += 2;
            vrot = vx * 0.5; // spin based on throw
            
            speak("Ahhhhh!", 2000);
        };

        container.addEventListener('mousedown', (e) => { startDrag(e.clientX, e.clientY); e.preventDefault(); });
        document.addEventListener('mousemove', (e) => doDrag(e.clientX, e.clientY));
        document.addEventListener('mouseup', endDrag);

        container.addEventListener('touchstart', (e) => startDrag(e.touches[0].clientX, e.touches[0].clientY));
        document.addEventListener('touchmove', (e) => {
            if (state === 'drag') { doDrag(e.touches[0].clientX, e.touches[0].clientY); e.preventDefault(); }
        }, { passive: false });
        document.addEventListener('touchend', endDrag);

        // LED blinking
        setInterval(() => {
            if(state === 'walk' || state === 'clean') {
                led.setAttribute('fill', led.getAttribute('fill') === '#ef4444' ? '#10b981' : '#ef4444');
            }
        }, 1000);

        // Random speaking
        setInterval(() => {
            if ((state === 'walk' || state === 'clean') && Math.random() < 0.3) {
                const phrases = ["Cleaning data...", "Vacuuming cache...", "Beep boop.", "Sweeping bugs..."];
                speak(phrases[Math.floor(Math.random() * phrases.length)]);
            }
        }, 10000);

        // Physics Engine Loop
        function physicsLoop() {
            const floorY = window.innerHeight - 70;
            const maxW = window.innerWidth - 60;

            if (state === 'fall' || state === 'tumble') {
                // Apply Gravity and Friction
                vy += 0.8; // gravity
                vx *= 0.98; // air resistance
                vrot *= 0.98;
                
                x += vx;
                y += vy;
                rotation += vrot;

                // Wall collision
                if (x < 0) { x = 0; vx *= -0.6; vrot += vy * 0.1; }
                else if (x > maxW) { x = maxW; vx *= -0.6; vrot -= vy * 0.1; }

                // Floor collision
                if (y >= floorY) {
                    y = floorY;
                    if (Math.abs(vy) > 2) {
                        // Bounce
                        vy *= -0.5;
                        vx *= 0.8; // ground friction
                        
                        // Add some rotation spin on impact
                        vrot += (vx * 0.5); 
                    } else {
                        // Settled on floor
                        vy = 0;
                        vx = 0;
                        y = floorY;
                        
                        // Check if tumbled over
                        const normalizedRot = ((rotation % 360) + 360) % 360;
                        if (normalizedRot > 45 && normalizedRot < 315) {
                            state = 'tumble';
                            vrot *= 0.9; // damp rotation
                            if (Math.abs(vrot) < 0.5) {
                                state = 'getup';
                                walkTimer = 60; // frames to get up
                                speak("Ouch! Re-orienting...", 2000);
                            }
                        } else {
                            state = 'walk';
                            rotation = 0;
                            vrot = 0;
                            eyes.forEach(eye => { eye.setAttribute('fill', '#38bdf8'); eye.setAttribute('r', '2'); });
                            container.classList.add('robot-walking');
                            speak("Whew! Back to work.", 2000);
                        }
                    }
                }
            } 
            else if (state === 'getup') {
                // Rotate back to 0 smoothly
                rotation = rotation * 0.9;
                y = floorY;
                walkTimer--;
                if (Math.abs(rotation) < 2 && walkTimer <= 0) {
                    rotation = 0;
                    state = 'walk';
                    eyes.forEach(eye => { eye.setAttribute('fill', '#38bdf8'); eye.setAttribute('r', '2'); });
                    container.classList.add('robot-walking');
                }
            }
            else if (state === 'walk') {
                y = floorY;
                x += baseSpeed * walkDirection;
                rotation = 0; // force upright
                
                if (x < 0) { x = 0; walkDirection = 1; }
                else if (x > maxW) { x = maxW; walkDirection = -1; }

                walkTimer++;
                if (walkTimer > 300 && Math.random() < 0.01) {
                    // Randomly stop to clean deeply
                    state = 'clean';
                    walkTimer = 0;
                    container.classList.remove('robot-walking');
                    container.classList.add('robot-cleaning');
                    setVacuumSound(true);
                }
            }
            else if (state === 'clean') {
                y = floorY;
                walkTimer++;
                if (walkTimer > 150) {
                    // Done cleaning
                    state = 'walk';
                    walkTimer = 0;
                    container.classList.remove('robot-cleaning');
                    container.classList.add('robot-walking');
                    setVacuumSound(false);
                }
            }

            // Apply transforms
            wrapper.style.transform = `translate(${x}px, ${y}px)`;
            
            // Container holds the rotation and flip
            const scaleX = walkDirection === -1 && (state === 'walk' || state === 'clean') ? -1 : 1;
            container.style.transform = `rotate(${rotation}deg) scaleX(${scaleX})`;

            // Update bubble position
            const bLeft = x + 40;
            const bBottom = window.innerHeight - y + 10;
            bubble.style.left = Math.min(bLeft, window.innerWidth - bubble.offsetWidth - 10) + 'px';
            bubble.style.bottom = bBottom + 'px';

            requestAnimationFrame(physicsLoop);
        }

        // Start Loop
        physicsLoop();
    });
})();
