// Smooth scroll behavior
document.addEventListener('DOMContentLoaded', function () {
    // Music Player Controls - Manual play only
    const music1 = document.getElementById('music1');
    const music2 = document.getElementById('music2');
    const musicBtn1 = document.getElementById('musicBtn1');
    const musicBtn2 = document.getElementById('musicBtn2');

    // Setup music button functionality
    function setupMusicButton(btn, audio, otherAudio, otherBtn) {
        if (!btn || !audio) return;

        btn.addEventListener('click', function () {
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


    // Countdown Timer
    const weddingDate = new Date('2026-02-20T09:30:00').getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = weddingDate - now;

        if (distance < 0) {
            // Wedding day has passed
            document.getElementById('days').textContent = '00';
            document.getElementById('hours').textContent = '00';
            document.getElementById('minutes').textContent = '00';
            document.getElementById('seconds').textContent = '00';
            return;
        }

        // Calculate time units
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Update display with leading zeros
        document.getElementById('days').textContent = String(days).padStart(2, '0');
        document.getElementById('hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
    }

    // Update countdown immediately and then every second
    updateCountdown();
    setInterval(updateCountdown, 1000);

    // Add scroll reveal animations
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        observer.observe(section);
    });

    // First section should be visible immediately
    if (sections[0]) {
        sections[0].style.opacity = '1';
        sections[0].style.transform = 'translateY(0)';
    }

    // Animate wedding-date-grid columns on scroll
    const dateGrid = document.querySelector('.wedding-date-grid');
    if (dateGrid) {
        const dateColumns = dateGrid.querySelectorAll('.date-column');

        const dateGridObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add animate class to all columns with stagger effect
                    dateColumns.forEach((column, index) => {
                        setTimeout(() => {
                            column.classList.add('animate');
                        }, index * 200); // 200ms delay between each column
                    });
                    dateGridObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        dateGridObserver.observe(dateGrid);
    }

    // Animate date-display-full on scroll
    const dateDisplayFull = document.querySelector('.date-display-full');
    if (dateDisplayFull) {
        const dateGroupLeft = dateDisplayFull.querySelector('.date-group-left');
        const dateGroupRight = dateDisplayFull.querySelector('.date-group-right');
        const dateNumberHuge = dateDisplayFull.querySelector('.date-number-huge');

        const dateDisplayObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add animate class to trigger animations
                    if (dateGroupLeft) dateGroupLeft.classList.add('animate');
                    if (dateGroupRight) dateGroupRight.classList.add('animate');
                    if (dateNumberHuge) dateNumberHuge.classList.add('animate');

                    dateDisplayObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        dateDisplayObserver.observe(dateDisplayFull);
    }

    // Directions button functionality
    const directionsBtn = document.getElementById('directionsBtn');
    if (directionsBtn) {
        directionsBtn.addEventListener('click', function () {
            // Google Maps URL with coordinates
            const mapsUrl = 'https://www.google.com/maps/dir/?api=1&destination=10.5594176,105.3300511';

            // Open in new tab
            window.open(mapsUrl, '_blank');
        });
    }

    // Add parallax effect to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function () {
            const scrolled = window.pageYOffset;
            const heroImage = document.querySelector('.hero-image');
            if (heroImage && scrolled < window.innerHeight) {
                heroImage.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        });
    }

    // Animate couple names on load
    const coupleNames = document.querySelector('.couple-names');
    if (coupleNames) {
        setTimeout(() => {
            coupleNames.querySelectorAll('p').forEach((name, index) => {
                name.style.animation = `fadeIn 1s ease-out ${0.5 + index * 0.3}s both`;
            });
        }, 1000);
    }

    // Add floral decorations animation
    const floralDecorations = document.querySelectorAll('.floral-decoration');
    floralDecorations.forEach((decoration, index) => {
        decoration.style.animation = `floatAnimation ${3 + index}s ease-in-out infinite`;
    });

    // Create floating animation keyframes dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatAnimation {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
            }
            50% {
                transform: translateY(-10px) rotate(5deg);
            }
        }
    `;
    document.head.appendChild(style);

    // RSVP Form Handling
    const rsvpForm = document.getElementById('rsvpForm');
    const formMessage = document.getElementById('formMessage');

    // TODO: Replace this URL with your Google Apps Script Web App URL
    const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyDExXoJpaHfHOT4fnmGkT7pBXvc3J55rGvrvY1jlARxlLOnY5-LY_sQAXpjPpgBLAW0w/exec';

    if (rsvpForm) {
        rsvpForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Get form values
            const formData = {
                name: document.getElementById('guestName').value.trim(),
                message: document.getElementById('guestMessage').value.trim(),
                attendance: document.getElementById('attendance').value,
                guestCount: document.getElementById('guestCount').value
            };

            // Validate
            if (!formData.name || !formData.attendance || !formData.guestCount) {
                showMessage('Vui lòng điền đầy đủ thông tin bắt buộc!', 'error');
                return;
            }

            // Disable form during submission
            const submitBtn = rsvpForm.querySelector('.form-submit-btn');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'ĐANG GỬI...';
            submitBtn.disabled = true;

            try {
                // Send to Google Sheets
                const response = await fetch(GOOGLE_SCRIPT_URL, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                // Show success message
                showMessage('Cảm ơn bạn đã xác nhận! Chúng mình rất mong được gặp bạn! 💕', 'success');

                // Reset form
                rsvpForm.reset();

            } catch (error) {
                console.error('Error:', error);
                showMessage('Có lỗi xảy ra. Vui lòng thử lại sau!', 'error');
            } finally {
                // Re-enable form
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    function showMessage(message, type) {
        formMessage.textContent = message;
        formMessage.className = `form-message ${type}`;
        formMessage.style.display = 'block';

        // Hide message after 5 seconds
        setTimeout(() => {
            formMessage.style.display = 'none';
        }, 5000);
    }

    // Photo Carousel Functionality
    const mainImage = document.getElementById('mainImage');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const thumbnailsContainer = document.getElementById('thumbnailsContainer');
    const thumbnails = document.querySelectorAll('.carousel-thumb');

    let currentIndex = 0;

    if (mainImage && thumbnails.length > 0) {
        // Auto-slide functionality
        let autoSlideTimer;

        function startAutoSlide() {
            stopAutoSlide(); // Clear existing timer
            autoSlideTimer = setInterval(() => {
                currentIndex = (currentIndex + 1) % thumbnails.length;
                updateCarousel(true); // Pass true to indicate auto-slide
            }, 3000); // Change image every 3 seconds
        }

        function stopAutoSlide() {
            if (autoSlideTimer) {
                clearInterval(autoSlideTimer);
            }
        }

        function resetAutoSlide() {
            stopAutoSlide();
            startAutoSlide();
        }

        // Start auto-slide initially
        startAutoSlide();

        // Pause on hover (optional but recommended for UX)
        const carouselContainer = document.querySelector('.album-carousel');
        if (carouselContainer) {
            carouselContainer.addEventListener('mouseenter', stopAutoSlide);
            carouselContainer.addEventListener('mouseleave', startAutoSlide);
        }

        // Next button
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % thumbnails.length;
            updateCarousel();
            resetAutoSlide();
        });

        // Previous button
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
            updateCarousel();
            resetAutoSlide();
        });

        // Thumbnail click
        thumbnails.forEach((thumb, index) => {
            thumb.addEventListener('click', () => {
                currentIndex = index;
                updateCarousel();
                resetAutoSlide();
            });
        });

        // Update carousel display
        function updateCarousel(isAuto = false) { // Add flag to check if triggered by auto-slide
            // Only auto-scroll if user is looking at the section
            if (isAuto) {
                const rect = mainImage.getBoundingClientRect();
                const isVisible = (
                    rect.top >= -rect.height &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) + rect.height
                );

                // If auto-slide and not visible, do not update (wait for user to scroll back)
                // OR: Update image but DO NOT scroll thumbnails if it causes jumps
                if (!isVisible) return;
            }

            // Update main image: Add hidden class to trigger fade out + scale
            mainImage.classList.add('hidden');

            // Wait for transition (300ms matches CSS)
            setTimeout(() => {
                mainImage.src = thumbnails[currentIndex].src;
                // Remove hidden class to trigger fade in + scale back
                mainImage.onload = () => {
                    mainImage.classList.remove('hidden');
                };
                // Fallback in case onload is too slow or cached
                setTimeout(() => mainImage.classList.remove('hidden'), 50);
            }, 300);

            // Update active thumbnail
            thumbnails.forEach((thumb, index) => {
                if (index === currentIndex) {
                    thumb.classList.add('active');
                } else {
                    thumb.classList.remove('active');
                }
            });

            // Scroll thumbnail into view WITHOUT scrolling the whole page
            const activeThumb = thumbnails[currentIndex];
            const container = thumbnailsContainer;

            // Calculate position to center the thumb
            const thumbLeft = activeThumb.offsetLeft;
            const thumbWidth = activeThumb.offsetWidth;
            const containerWidth = container.offsetWidth;

            // Smoothly scroll the container horizontally
            container.scrollTo({
                left: thumbLeft - (containerWidth / 2) + (thumbWidth / 2),
                behavior: 'smooth'
            });
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                prevBtn.click();
            } else if (e.key === 'ArrowRight') {
                nextBtn.click();
            }
        });

        // Lightbox Functionality
        const lightboxModal = document.getElementById('lightboxModal');
        const lightboxImage = document.getElementById('lightboxImage');
        const closeLightbox = document.querySelector('.close-lightbox');

        if (lightboxModal && lightboxImage && closeLightbox) {
            // Open lightbox
            mainImage.addEventListener('click', () => {
                stopAutoSlide(); // Stop slide when viewing
                lightboxModal.style.display = 'flex';
                // Trigger reflow
                void lightboxModal.offsetWidth;
                lightboxModal.classList.add('show');
                lightboxImage.src = mainImage.src;
            });

            // Close lightbox function
            const closeBox = () => {
                lightboxModal.classList.remove('show');
                setTimeout(() => {
                    lightboxModal.style.display = 'none';
                    startAutoSlide(); // Resume slide
                }, 300);
            };

            // Close on 'x' click
            closeLightbox.addEventListener('click', closeBox);

            // Close on outside click
            lightboxModal.addEventListener('click', (e) => {
                if (e.target === lightboxModal) {
                    closeBox();
                }
            });

            // Close on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && lightboxModal.style.display === 'flex') {
                    closeBox();
                }
            });
        }
    }

    // Special observer for Thank You section animations
    const thankYouSection = document.querySelector('.thankyou-section');
    if (thankYouSection) {
        const thankYouObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    thankYouSection.classList.add('visible');
                    thankYouObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        thankYouObserver.observe(thankYouSection);
    }
});
