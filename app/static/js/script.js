// menu icon nav toggle
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

// scroll reveal
ScrollReveal({
    distance: '80px',
    duration: 2000,
    delay: 200
});

ScrollReveal().reveal('.home-content, .heading', { origin: 'top' });
ScrollReveal().reveal('.home-img, .education-box, .projects-box, .hobbies-box, .timeline form, .contact form, .posts-box, #map', { origin: 'bottom' });
ScrollReveal().reveal('.home-content h1, .about-img', { origin: 'left' });
ScrollReveal().reveal('.home-content p, .about-content', { origin: 'right' });

// typed js
const typed = new Typed('.multiple-text', {
    strings: ['Systems Analyst', 'Production Engineer', 'Site Reliability Engineer'],
    typeSpeed: 50,
    backSpeed: 25,
    backDelay: 1000,
    loop: true
});
