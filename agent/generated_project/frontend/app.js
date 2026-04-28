
const API_URL = "http://127.0.0.1:8000";

const uploadInput = document.getElementById("upload");
const gallery = document.getElementById("gallery");

// Load images
window.onload = () => {
    loadImages();
    showSection('home');
};

// Navigation
function showSection(section) {
    document.querySelectorAll("section").forEach(sec => sec.classList.remove("active"));

    if (section === "home") {
        document.getElementById("home").classList.add("active");
    } else {
        document.getElementById("gallery-section").classList.add("active");
        loadImages();
    }
}

// MULTIPLE Upload
uploadInput.addEventListener("change", async () => {
    const files = Array.from(uploadInput.files);

    for (const file of files) {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(`${API_URL}/upload`, {
                method: "POST",
                body: formData
            });
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    }

    uploadInput.value = "";

    // IMPORTANT
    await loadImages();
    console.log("Gallery refreshed after upload");
    alert("Images uploaded successfully!");
});

// Load images
async function loadImages() {
    try {
        const res = await fetch(`${API_URL}/images?t=${Date.now()}`); // 🔥 cache busting
        const images = await res.json();

        gallery.innerHTML = "";

        images.forEach(img => {
            const card = document.createElement("div");
            card.className = "card";

            const image = document.createElement("img");

            // 🔥 SAFE CHECK
            if (img.content) {
                image.src = `data:image/jpeg;base64,${img.content}`;
            }

            const btn = document.createElement("button");
            btn.innerText = "Delete";
            btn.onclick = () => deleteImage(img.id);

            card.appendChild(image);
            card.appendChild(btn);

            gallery.appendChild(card);
        });

    } catch (err) {
        console.error("Load error:", err);
    }
}

// Delete
async function deleteImage(id) {
    await fetch(`http://127.0.0.1:8000/image/${id}`, {
        method: "DELETE"
    });

    loadImages(); // 🔥 refresh UI
}