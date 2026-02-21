function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
}

document.body.addEventListener("htmx:configRequest", (event) => {
    const token = getCookie("csrftoken");
    if (token) {
        event.detail.headers["X-CSRFToken"] = token;
    }
});
