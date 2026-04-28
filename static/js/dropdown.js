const dropdown = document.querySelector(".dropdown");
const btn = document.querySelector(".dropbtn");

if (dropdown && btn) {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        dropdown.classList.toggle("active");
    });

    window.addEventListener("click", () => {
        dropdown.classList.remove("active");
    });
}