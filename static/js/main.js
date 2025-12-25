// Scroll to section
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId)
  if (section) {
    section.scrollIntoView({ behavior: "smooth" })
  }
}

// Tab switching
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const tabName = e.currentTarget.dataset.tab

    // Remove active class from all tabs
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"))
    document.querySelectorAll(".tab-content").forEach((t) => t.classList.remove("active"))

    // Add active class to clicked tab
    e.currentTarget.classList.add("active")
    document.getElementById(tabName).classList.add("active")
  })
})

// Upload file handling
const uploadBox = document.getElementById("uploadBox")
const fileInput = document.getElementById("fileInput")
const uploadPreview = document.getElementById("uploadPreview")
const predictBtn = document.getElementById("predictBtn")

uploadBox.addEventListener("click", () => fileInput.click())

uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault()
  uploadBox.style.borderColor = "var(--primary)"
})

uploadBox.addEventListener("dragleave", () => {
  uploadBox.style.borderColor = "var(--border)"
})

uploadBox.addEventListener("drop", (e) => {
  e.preventDefault()
  uploadBox.style.borderColor = "var(--border)"

  const files = e.dataTransfer.files
  if (files.length > 0) {
    fileInput.files = files
    handleFileSelect()
  }
})

fileInput.addEventListener("change", handleFileSelect)

function handleFileSelect() {
  const file = fileInput.files[0]
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader()
    reader.onload = (e) => {
      document.getElementById("previewImage").src = e.target.result
      document.getElementById("resultImage").src = e.target.result
      uploadBox.style.display = "none"
      uploadPreview.style.display = "flex"
      predictBtn.style.display = "inline-flex"
    }
    reader.readAsDataURL(file)
  }
}

function resetUpload() {
  fileInput.value = ""
  uploadBox.style.display = "block"
  uploadPreview.style.display = "none"
  predictBtn.style.display = "none"
  document.getElementById("uploadResult").style.display = "none"
}

function predictImage() {
  const file = fileInput.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append("file", file)

  document.getElementById("uploadLoading").style.display = "flex"
  predictBtn.disabled = true

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("flowerName").textContent = data.prediction
        const confidence = data.confidence
        document.getElementById("confidenceFill").style.width = confidence + "%"
        document.getElementById("confidenceText").textContent = `Kepercayaan: ${confidence.toFixed(1)}%`
        document.getElementById("uploadResult").style.display = "block"
      } else {
        alert("Error: " + (data.error || "Unknown error"))
      }
    })
    .catch((error) => {
      console.error("Error:", error)
      alert("Error: " + error.message)
    })
    .finally(() => {
      document.getElementById("uploadLoading").style.display = "none"
      predictBtn.disabled = false
    })
}

// Camera functions
let stream = null

function startCamera() {
  navigator.mediaDevices
    .getUserMedia({
      video: { facingMode: "environment" },
    })
    .then((mediaStream) => {
      stream = mediaStream
      const video = document.getElementById("cameraStream")
      video.srcObject = stream

      document.getElementById("startCameraBtn").style.display = "none"
      document.getElementById("stopCameraBtn").style.display = "inline-flex"
      document.getElementById("captureBtn").style.display = "inline-flex"
    })
    .catch((error) => {
      alert("Error accessing camera: " + error.message)
    })
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop())
    document.getElementById("cameraStream").srcObject = null
  }

  document.getElementById("startCameraBtn").style.display = "inline-flex"
  document.getElementById("stopCameraBtn").style.display = "none"
  document.getElementById("captureBtn").style.display = "none"
}

function captureCamera() {
  const video = document.getElementById("cameraStream")
  const canvas = document.getElementById("cameraCanvas")
  const context = canvas.getContext("2d")

  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  context.drawImage(video, 0, 0)

  canvas.toBlob((blob) => {
    const formData = new FormData()
    formData.append("image", blob, "camera.jpg")

    document.getElementById("cameraLoading").style.display = "flex"
    document.getElementById("captureBtn").disabled = true

    fetch("/camera_predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.getElementById("cameraResultImage").src = canvas.toDataURL()
          document.getElementById("cameraFlowerName").textContent = data.prediction
          const confidence = data.confidence
          document.getElementById("cameraConfidenceFill").style.width = confidence + "%"
          document.getElementById("cameraConfidenceText").textContent = `Kepercayaan: ${confidence.toFixed(1)}%`
          document.getElementById("cameraResult").style.display = "block"
        } else {
          alert("Error: " + (data.error || "Unknown error"))
        }
      })
      .catch((error) => {
        console.error("Error:", error)
        alert("Error: " + error.message)
      })
      .finally(() => {
        document.getElementById("cameraLoading").style.display = "none"
        document.getElementById("captureBtn").disabled = false
      })
  }, "image/jpeg")
}

// Search function
function searchFlower() {
  const query = document.getElementById("searchInput").value.toLowerCase()
  if (!query) return

  // Dummy flower list untuk demo
  const flowers = [
    { name: "Pink Primrose", id: 1 },
    { name: "Hard-leaved Pocket Orchid", id: 2 },
    { name: "Canterbury Bells", id: 3 },
    { name: "Sweet Pea", id: 4 },
    { name: "English Marigold", id: 5 },
    { name: "Tiger Lily", id: 6 },
    { name: "Moon Orchid", id: 7 },
    { name: "Bird of Paradise", id: 8 },
    { name: "Sunflower", id: 54 },
    { name: "Rose", id: 74 },
  ]

  const results = flowers.filter((f) => f.name.toLowerCase().includes(query))
  const resultsDiv = document.getElementById("searchResults")

  if (results.length === 0) {
    resultsDiv.innerHTML =
      '<p style="grid-column: 1 / -1; text-align: center; color: var(--text-light);">Tidak ada hasil ditemukan</p>'
  } else {
    resultsDiv.innerHTML = results.map((f) => `<div class="search-result-item">${f.name}</div>`).join("")
  }
}

// Enter key for search
document.getElementById("searchInput")?.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    searchFlower()
  }
})
