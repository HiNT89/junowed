/**
 * Scroll-Triggered Animation System
 * Uses Intersection Observer to trigger animations when elements scroll into view
 * Works with Animate.css and custom animations
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    // Intersection Observer options
    rootMargin: '0px 0px -100px 0px', // Trigger when element is about 100px from bottom
    threshold: 0,
    // Animation settings
    animationDelay: 0, // Base delay in ms
    staggerDelay: 100, // Delay between elements in same container (ms)
  };

  // Store observer instances
  const observers = new Map();

  /**
   * Initialize scroll trigger animations
   */
  function initScrollTriggers() {
    // Get all elements that should animate on scroll
    const elements = document.querySelectorAll('[data-animate-on-scroll]');
    
    if (elements.length === 0) {
      // Fallback: if no data-attribute, use .wow and animate__animated classes
      initWowScrollTriggers();
      return;
    }

    // Create observer for scroll-triggered animations
    const observer = new IntersectionObserver(handleIntersection, CONFIG);

    elements.forEach(element => {
      observer.observe(element);
    });
  }

  /**
   * Alternative initialization using WOW.js classes
   * Converts WOW.js elements to scroll-triggered animations
   */
  function initWowScrollTriggers() {
    const animatedElements = document.querySelectorAll('.wow.animate__animated');
    
    if (animatedElements.length === 0) return;

    // Observer for elements with wow class
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Trigger WOW.js animation
          entry.target.classList.add('animated');
          // Optional: unobserve after animation to save resources
          // observer.unobserve(entry.target);
        } else {
          // Reset animation when scrolling back
          entry.target.classList.remove('animated');
        }
      });
    }, CONFIG);

    animatedElements.forEach(element => {
      observer.observe(element);
    });
  }

  /**
   * Handle intersection changes - trigger animations
   */
  function handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        triggerAnimation(entry.target);
        // Optionally unobserve to prevent repeated triggers
        // observerInstance.unobserve(entry.target);
      } else {
        resetAnimation(entry.target);
      }
    });
  }

  /**
   * Trigger animation on element
   */
  function triggerAnimation(element) {
    if (element.classList.contains('animated') || element.classList.contains('animate__animated')) {
      return; // Already animating
    }

    // Get animation classes from data attribute or existing classes
    const animationClass = element.dataset.scrollAnimation || getExistingAnimationClass(element);
    
    if (!animationClass) return;

    // Add delay if specified
    const delay = element.dataset.scrollDelay || CONFIG.animationDelay;
    if (delay > 0) {
      element.style.setProperty('--animate-delay', delay + 'ms');
    }

    // Add animation classes
    element.classList.add('animated');
    element.classList.add('animate__animated');
    element.classList.add(animationClass);

    // Emit custom event
    element.dispatchEvent(new CustomEvent('scrollAnimationStart', { detail: { animation: animationClass } }));
  }

  /**
   * Reset animation on element (for when scrolling back)
   */
  function resetAnimation(element) {
    const animationClass = element.dataset.scrollAnimation || getExistingAnimationClass(element);
    
    if (!animationClass) return;

    element.classList.remove('animated');
    element.classList.remove(animationClass);

    // Keep animate__animated for potential re-trigger
    if (element.dataset.resetOnScroll !== 'false') {
      element.style.removeProperty('--animate-delay');
    }
  }

  /**
   * Get animation class from element's existing Animate.css classes
   */
  function getExistingAnimationClass(element) {
    const classList = element.classList;
    for (const className of classList) {
      if (className.startsWith('animate__') && className !== 'animate__animated' && className !== 'animated') {
        return className;
      }
    }
    return null;
  }

  /**
   * Add scroll trigger to individual elements
   * Usage: addScrollTrigger(element, 'animate__fadeInUp', delayMs)
   */
  window.addScrollTrigger = function(element, animationClass, delay = 0) {
    element.classList.add('wow', 'animate__animated', animationClass);
    if (delay > 0) {
      element.dataset.scrollDelay = delay;
    }
    
    const observer = new IntersectionObserver(handleIntersection, CONFIG);
    observer.observe(element);
  };

  /**
   * Reinitialize all scroll triggers (useful after dynamic content)
   */
  window.reinitScrollTriggers = function() {
    initScrollTriggers();
    initWowScrollTriggers();
  };

  /**
   * Manual animation trigger (if needed)
   */
  window.triggerScrollAnimation = function(element) {
    triggerAnimation(element);
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollTriggers);
  } else {
    initScrollTriggers();
  }

  // Re-initialize on page show (for when returning from other pages)
  window.addEventListener('pageshow', initScrollTriggers);

  // Optional: Update animations on resize for better accuracy
  let resizeTimeout;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(reinitScrollTriggers, 250);
  });

})();
