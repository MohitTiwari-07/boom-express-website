
document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector(".site-header");
    const menuButton = document.querySelector(".menu-toggle");
    const navigation = document.querySelector(".primary-navigation");

    // Header scroll effect
    const updateHeader = () => {
        if (header) {
            header.classList.toggle("scrolled", window.scrollY > 40);
        }
    };

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    // Mobile navigation
    if (menuButton && navigation) {
        menuButton.addEventListener("click", () => {
            const isOpen = menuButton.getAttribute("aria-expanded") === "true";

            menuButton.setAttribute("aria-expanded", String(!isOpen));
            menuButton.setAttribute(
                "aria-label",
                isOpen ? "Open navigation" : "Close navigation"
            );

            navigation.classList.toggle("active", !isOpen);
            document.body.classList.toggle("menu-open", !isOpen);
        });

        navigation.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                menuButton.setAttribute("aria-expanded", "false");
                menuButton.setAttribute("aria-label", "Open navigation");
                navigation.classList.remove("active");
                document.body.classList.remove("menu-open");
            });
        });

        document.addEventListener("keydown", event => {
            if (event.key === "Escape") {
                menuButton.setAttribute("aria-expanded", "false");
                menuButton.setAttribute("aria-label", "Open navigation");
                navigation.classList.remove("active");
                document.body.classList.remove("menu-open");
            }
        });
    }

    // Scroll reveal animations
    const revealElements = document.querySelectorAll(
        ".reveal, .reveal-up, .reveal-left, .reveal-right"
    );

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -40px 0px"
            }
        );

        revealElements.forEach(element => observer.observe(element));
    } else {
        revealElements.forEach(element => {
            element.classList.add("is-visible");
        });
    }

    // Hero video: pause when the page is not visible
    const heroVideo = document.querySelector(".hero-video");

    if (heroVideo) {
        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                heroVideo.pause();
            } else if (!window.matchMedia(
                "(prefers-reduced-motion: reduce)"
            ).matches) {
                heroVideo.play().catch(() => {});
            }
        });
    }

    // Current year
    document.querySelectorAll("[data-current-year]").forEach(element => {
        element.textContent = new Date().getFullYear();
    });

    // Close mobile menu when resizing to desktop
    window.addEventListener("resize", () => {
        if (window.innerWidth > 900 && menuButton && navigation) {
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.setAttribute("aria-label", "Open navigation");
            navigation.classList.remove("active");
            document.body.classList.remove("menu-open");
        }
    });
});
