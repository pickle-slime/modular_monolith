let accessToken = localStorage.getItem("access_token");

// Add Authorization header to all AJAX requests
$(document).ajaxSend(function (event, xhr, settings) {
    if (accessToken) {
        xhr.setRequestHeader("Authorization", `Bearer ${accessToken}`);
    }
});

// Update token from New-Access-Token header
$(document).ajaxComplete(function (event, xhr, settings) {
    const newAccessToken = xhr.getResponseHeader("New-Access-Token");
    if (newAccessToken) {
        localStorage.setItem("access_token", newAccessToken);
    }
});

// Handle views that return TemplateResponse
$(function () {
    $.ajax({
        type: "HEAD",
        url: window.location.href,
        complete: function (xhr) {
            const newAccessToken = xhr.getResponseHeader("New-Access-Token");
            if (newAccessToken) {
                localStorage.setItem("access_token", newAccessToken);
            }
        },
    });
});

// Ensure CSRF token is added to all non-GET requests
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        const csrftoken = getCSRFToken();
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && csrftoken) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
});

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [key, value] = cookie.split("=");
        if (key === name) return value;
    }
    return null;
}
