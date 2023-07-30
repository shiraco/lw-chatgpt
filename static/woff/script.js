import { woffId } from "./params.js";

/**
 * Get profile
 */
const getProfile = () => {
  // Get profile
  woff
    .getProfile()
    .then((profile) => {
      // Success
      console.log(profile);

      // Set user info
      document.getElementById("domainIdField").textContent = profile.domainId;
      document.getElementById("userIdProfileField").textContent =
        profile.userId;
      document.getElementById("displayNameField").textContent =
        profile.displayName;
    })
    .catch((err) => {
      // Error
      console.log(err);
      window.alert(err);
    });
};

/**
 * Register event handlers for the buttons displayed in the app
 */
const registerButtonHandlers = () => {
  document
    .getElementById("sendMessageButton")
    .addEventListener("click", function () {
      let msg = document.getElementById("sendMessageText").value;

      // sendMessage call
      woff
        .sendMessage({ content: msg })
        .then(() => {
          // Success
          console.log("message sent: " + msg);
          window.alert("Message sent");
        })
        .catch((err) => {
          // Error
          console.log(err);
          window.alert(err);
        });
    });
};

// On load
window.addEventListener("load", () => {
  console.log(woffId);

  // Initialize WOFF
  woff
    .init({ woffId: woffId })
    .then(() => {
      // Success
      // Button handler
      registerButtonHandlers();
      // Get and show user profile
      getProfile();
    })
    .catch((err) => {
      // Error
      window.alert(err);
      console.error(err);
    });
});
