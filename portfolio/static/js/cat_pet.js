(function() {
    // Wait for DOM to be fully loaded
    window.addEventListener('DOMContentLoaded', () => {
        // Create the cat element
        const cat = document.createElement('div');
        cat.id = 'virtual-cat';
        
        // Use the classic Oneko white cat sprite sheet
        const spriteUrl = 'https://raw.githubusercontent.com/adryd325/oneko.js/main/oneko.gif';
        
        Object.assign(cat.style, {
            width: '32px',
            height: '32px',
            position: 'fixed',
            bottom: '0',
            left: '50px', // starting position
            backgroundImage: `url(${spriteUrl})`,
            imageRendering: 'pixelated', // Keep it sharp
            zIndex: '9999',
            pointerEvents: 'auto',
            cursor: 'pointer',
            transition: 'transform 0.1s'
        });

        // Create speech bubble
        const bubble = document.createElement('div');
        Object.assign(bubble.style, {
            position: 'fixed',
            bottom: '40px',
            left: '50px',
            padding: '8px 12px',
            background: 'rgba(255, 255, 255, 0.95)',
            color: '#0f172a', // primary dark
            borderRadius: '12px',
            borderBottomLeftRadius: '0',
            fontFamily: 'monospace',
            fontSize: '13px',
            fontWeight: 'bold',
            boxShadow: '0 4px 15px rgba(0,0,0,0.5)',
            zIndex: '10000',
            opacity: '0',
            pointerEvents: 'none',
            transition: 'opacity 0.3s',
            whiteSpace: 'nowrap'
        });
        
        document.body.appendChild(cat);
        document.body.appendChild(bubble);

        // State machine variables
        let catX = window.innerWidth / 2;
        let direction = 1; // 1 = right, -1 = left
        let speed = 1.5;
        let state = 'idle'; // idle, walk, sit, sleep, groom
        let frameCount = 0;
        let stateTimer = 0;
        
        const messages = [
            "Meow~ 🐾",
            "Hello! Welcome to the portfolio.",
            "Need a Data Scientist?",
            "I love Python and tuna!",
            "Purrr...",
            "Have you checked the Tools menu?",
            "*licks paw*",
            "Data is delicious!"
        ];

        let bubbleTimeout;
        function showMessage(text, duration = 4000) {
            bubble.textContent = text;
            bubble.style.opacity = '1';
            updateBubblePos();
            
            clearTimeout(bubbleTimeout);
            bubbleTimeout = setTimeout(() => {
                bubble.style.opacity = '0';
            }, duration);
        }

        function updateBubblePos() {
            // Adjust bubble position so it doesn't go off-screen
            let bubbleLeft = catX + 20;
            if (bubbleLeft + bubble.offsetWidth > window.innerWidth) {
                bubbleLeft = catX - bubble.offsetWidth - 5;
                bubble.style.borderBottomLeftRadius = '12px';
                bubble.style.borderBottomRightRadius = '0';
            } else {
                bubble.style.borderBottomLeftRadius = '0';
                bubble.style.borderBottomRightRadius = '12px';
            }
            bubble.style.left = bubbleLeft + 'px';
        }

        // Click interaction
        cat.addEventListener('click', () => {
            state = 'sit';
            stateTimer = 80; // force sit for a while
            showMessage("Meow! Don't pet me while I'm working!", 3000);
            cat.style.backgroundPosition = '-96px -32px'; // sit sprite
        });

        // Random message loop
        setInterval(() => {
            if (Math.random() < 0.4 && state !== 'sleep') {
                showMessage(messages[Math.floor(Math.random() * messages.length)]);
            }
        }, 12000);

        // Main animation loop
        function update() {
            stateTimer--;

            if (stateTimer <= 0) {
                // Decide new state
                const r = Math.random();
                if (r < 0.45) {
                    state = 'walk';
                    stateTimer = 100 + Math.random() * 150;
                    // Maybe flip direction
                    if (Math.random() < 0.4) direction *= -1;
                } else if (r < 0.65) {
                    state = 'sit';
                    stateTimer = 50 + Math.random() * 80;
                } else if (r < 0.85) {
                    state = 'groom';
                    stateTimer = 40 + Math.random() * 60;
                } else {
                    state = 'sleep';
                    stateTimer = 150 + Math.random() * 250;
                }
            }

            frameCount++;

            // Apply logic based on state
            if (state === 'walk') {
                catX += speed * direction;
                
                // Screen bounds check
                const maxW = window.innerWidth - 32;
                if (catX < 0) {
                    catX = 0;
                    direction = 1;
                }
                if (catX > maxW) {
                    catX = maxW;
                    direction = -1;
                }
                
                cat.style.left = catX + 'px';
                updateBubblePos();
                
                // Flip image based on direction
                cat.style.transform = direction === -1 ? 'scaleX(-1)' : 'scaleX(1)';
                
                // Animate walk (alternating 2 frames)
                const isStep2 = (Math.floor(frameCount / 8) % 2) === 0;
                cat.style.backgroundPosition = isStep2 ? '-0px -32px' : '-32px -32px';
                
            } else if (state === 'sit') {
                cat.style.transform = direction === -1 ? 'scaleX(-1)' : 'scaleX(1)';
                cat.style.backgroundPosition = '-96px -32px'; // Sit frame
            } else if (state === 'groom') {
                cat.style.transform = direction === -1 ? 'scaleX(-1)' : 'scaleX(1)';
                // Animate groom (alternating 2 frames)
                const isStep2 = (Math.floor(frameCount / 10) % 2) === 0;
                cat.style.backgroundPosition = isStep2 ? '-64px 0px' : '-64px -32px';
            } else if (state === 'sleep') {
                cat.style.transform = direction === -1 ? 'scaleX(-1)' : 'scaleX(1)';
                // Animate sleep (slower alternation)
                const isStep2 = (Math.floor(frameCount / 20) % 2) === 0;
                cat.style.backgroundPosition = isStep2 ? '-64px -64px' : '-96px -64px';
                
                // Occasional Zzz bubble
                if (stateTimer % 120 === 0) {
                    showMessage("Zzz...", 2000);
                }
            }

            requestAnimationFrame(update);
        }

        // Start animation
        update();
    });
})();
