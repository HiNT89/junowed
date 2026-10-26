// Music Player Controls - Manual play only
document.addEventListener('DOMContentLoaded', function () {
    const music1 = document.getElementById('music1');
    const music2 = document.getElementById('music2');
    const musicBtn1 = document.getElementById('musicBtn1');
    const musicBtn2 = document.getElementById('musicBtn2');

    // Setup music button functionality
    function setupMusicButton(btn, audio, otherAudio, otherBtn) {
        if (!btn || !audio) return;

        btn.addEventListener('click', function (e) {
            e.stopPropagation(); // Prevent triggering other click events

            if (audio.paused) {
                // Stop the other audio first
                if (otherAudio && !otherAudio.paused) {
                    otherAudio.pause();
                    if (otherBtn) otherBtn.classList.remove('playing');
                }

                // Play this audio
                audio.play().then(() => {
                    btn.classList.add('playing');
                }).catch(err => {
                    console.log('Play failed:', err);
                });
            } else {
                // Pause this audio
                audio.pause();
                btn.classList.remove('playing');
            }
        });

        // Update button state when audio ends (if not looping)
        audio.addEventListener('ended', function () {
            btn.classList.remove('playing');
        });
    }

    // Initialize both music buttons
    setupMusicButton(musicBtn1, music1, music2, musicBtn2);
    setupMusicButton(musicBtn2, music2, music1, musicBtn1);

    // Wax Seal Click Handler
    const waxSeal = document.getElementById('waxSeal');

    // Function to handle navigation
    function handleWaxSealClick(e) {
        // Prevent default behavior and stop propagation
        e.preventDefault();
        e.stopPropagation();

        // Add click animation
        waxSeal.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        waxSeal.style.transform = 'scale(0.9)';
        waxSeal.style.opacity = '0.5';

        // Navigate to page 2 after animation completes
        setTimeout(() => {
            window.location.href = 'page2.html';
        }, 400);
    }

    // Add both click and touchend event listeners for better mobile support
    waxSeal.addEventListener('click', handleWaxSealClick);
    waxSeal.addEventListener('touchend', handleWaxSealClick);

    // Hover effects removed to prevent movement
});

// Breaking animation for wax seal
const style = document.createElement('style');
style.textContent = `
    @keyframes break {
        0% {
            transform: translate(-50%, -50%) scale(1) rotate(0deg);
            opacity: 1;
        }
        50% {
            transform: translate(-50%, -50%) scale(1.2) rotate(5deg);
            opacity: 0.8;
        }
        100% {
            transform: translate(-50%, -50%) scale(0.5) rotate(15deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Add particle effect on interaction (optional enhancement)
function addParticleEffect(e) {
    const x = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
    const y = e.clientY || (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
    if (x && y) {
        createParticles(x, y);
    }
}
waxSeal.addEventListener('click', addParticleEffect);
waxSeal.addEventListener('touchstart', addParticleEffect);

function createParticles(x, y) {
    const particleCount = 12;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: fixed;
            width: 6px;
            height: 6px;
            background: #8b7355;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            left: ${x}px;
            top: ${y}px;
        `;

        document.body.appendChild(particle);

        const angle = (Math.PI * 2 * i) / particleCount;
        const velocity = 3 + Math.random() * 2;
        const tx = Math.cos(angle) * velocity * 20;
        const ty = Math.sin(angle) * velocity * 20;

        particle.animate([
            { transform: 'translate(0, 0)', opacity: 1 },
            { transform: `translate(${tx}px, ${ty}px)`, opacity: 0 }
        ], {
            duration: 600,
            easing: 'cubic-bezier(0, .9, .57, 1)'
        }).onfinish = () => particle.remove();
    }
}

// Improved mobile touch handling
// Removed preventDefault to allow click events to fire properly on mobile
