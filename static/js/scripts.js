document.addEventListener("DOMContentLoaded", function () {
  if (typeof window.ImageResize !== "undefined") {
    Quill.register("modules/imageResize", window.ImageResize);
  } else {
    console.warn("⚠ Module imageResize introuvable");
  }

  if (typeof window.ImageUploader !== "undefined") {
    Quill.register("modules/imageUploader", window.ImageUploader);
  } else {
    console.warn("⚠ Module imageUploader introuvable");
  }

  const quill = new Quill("#editor", {
    theme: "snow",
    modules: {
      toolbar: "#toolbar",
      imageResize: { displaySize: true },
      imageUploader: {
        upload: file => Promise.resolve("path/to/image"),
      },
    },
  });



  // Bouton personnalisé d’insertion d’image
  const customImageBtn = document.getElementById("customImageBtn");
  if (customImageBtn) {
    customImageBtn.addEventListener("click", function () {
      const input = document.createElement("input");
      input.type = "file";
      input.accept = "image/*";

      input.onchange = () => {
        const file = input.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("image", file);

        fetch("/documents/upload_image/", {
          method: "POST",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          body: formData,
        })
          .then((response) => response.json())
          .then((result) => {
            if (result && result.url) {
              const range = quill.getSelection(true);
              quill.insertEmbed(range.index, "image", result.url);
            } else {
              alert("Erreur de réponse du serveur.");
            }
          })
          .catch(() => alert("Erreur réseau lors de l’envoi."));
      };

      input.click();
    });
  }

  
  // Sauvegarde du contenu HTML avant envoi
  const form = document.getElementById("templateForm");
  if (form) {
    form.addEventListener("submit", function () {
      const contentInput = document.getElementById("content");
      contentInput.value = quill.root.innerHTML;
    });
  }

  // Fonction CSRF pour Django
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
