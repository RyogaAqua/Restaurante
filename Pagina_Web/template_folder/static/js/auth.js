console.log("Testing if auth.js is loaded");

function checkAuthStatus() {
  console.log("Checking authentication status...");
  fetch("/auth/status", { method: "GET", credentials: "include" })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch auth status");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Auth status response:", data);
      const signInButton = document.querySelector(".signin-btn[href='signin.html']");
      const signOutButton = document.getElementById("signout-button");

      if (!signInButton || !signOutButton) {
        console.error("Sign In or Sign Out button not found on the page.");
        return;
      }

      if (data.isAuthenticated) {
        console.log("User is authenticated. Showing Sign Out button.");
        signInButton.style.display = "none"; // Ocultar Sign In
        signOutButton.style.display = "inline-block"; // Mostrar Sign Out
      } else {
        console.log("User is not authenticated. Showing Sign In button.");
        signInButton.style.display = "inline-block"; // Mostrar Sign In
        signOutButton.style.display = "none"; // Ocultar Sign Out
      }
    })
    .catch((error) => console.error("Error checking auth status:", error));
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("Auth script loaded and DOM fully loaded");
  checkAuthStatus();
});