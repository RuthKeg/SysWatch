const toggleBtn = document.getElementById("theme-toggle-settings");
if (toggleBtn) {
    const current = localStorage.getItem("theme") || "light";
    if (current === "dark") document.body.classList.add("dark");
    toggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
    });
}
