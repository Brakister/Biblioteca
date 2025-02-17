// Adiciona animação ao scroll
document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll(".fadeIn");
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        },
        { threshold: 0.2 }
    );

    sections.forEach((section) => observer.observe(section));
});