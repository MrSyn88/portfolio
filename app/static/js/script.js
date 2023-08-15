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

// send email from contact me
function validateAndSubmit(event) {
    event.preventDefault();
    var name = document.getElementById("nameInput").value;
    var email = document.getElementById("emailInput").value;

    if (name.trim() === "" || email.trim() === "" || !isValidEmail(email)) {
        alert("Please enter a valid name and email address.");
        return false;
    }

    fetch('https://formsubmit.co/98e2200d283df1ce0a7053742feb6773', {
        method: 'POST',
        body: new FormData(document.getElementById('contactForm'))
    })
        .then(response => {
            if (response.ok) {
                alert('Message sent successfully\nI\'ll get back to you as soon as I can!');
                document.getElementById('contactForm').reset();
            } else {
                alert('An error occurred while sending the message.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the message.');
        });

    return false;
}

function isValidEmail(email) {
    var emailRegex = /^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
} 
