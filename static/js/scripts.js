document.addEventListener("DOMContentLoaded", function () {
  // Initialisation de Quill
  const quill = new Quill("#editor", {
    theme: "snow",
    placeholder: "Rédigez votre document ici...",
    modules: {
      toolbar: "#toolbar",
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

  // Gestion du glisser-déposer d’images
  const editorContainer = document.querySelector("#editor .ql-editor");
  if (editorContainer) {
    editorContainer.addEventListener("drop", function (e) {
      e.preventDefault();
      if (e.dataTransfer && e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        if (file.type.startsWith("image/")) {
          const reader = new FileReader();
          reader.onload = function (evt) {
            const range = quill.getSelection(true);
            quill.insertEmbed(range.index, "image", evt.target.result);
          };
          reader.readAsDataURL(file);
        }
      }
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
