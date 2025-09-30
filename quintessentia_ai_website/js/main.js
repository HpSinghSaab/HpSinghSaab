document.addEventListener('DOMContentLoaded', () => {
    // Set the copyright year dynamically
    const copyrightYearSpan = document.getElementById('copyright-year');
    if (copyrightYearSpan) {
        copyrightYearSpan.textContent = new Date().getFullYear();
    }

    // Intersection Observer for animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const elementsToAnimate = document.querySelectorAll('.fade-in-element');
    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });

    // Page transition handling
    const navLinks = document.querySelectorAll('header nav a, .cta-button');
    navLinks.forEach(link => {
        link.addEventListener('click', e => {
            const url = link.getAttribute('href');

            // Don't run animation for same-page links or external links
            if (url.startsWith('#') || (link.protocol !== window.location.protocol || link.hostname !== window.location.hostname)) {
                return;
            }

            e.preventDefault();

            document.body.classList.add('is-leaving');

            setTimeout(() => {
                window.location.href = url;
            }, 400);
        });
    });
});