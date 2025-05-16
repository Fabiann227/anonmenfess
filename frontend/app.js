document.getElementById("menfessForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  console.log("[DEBUG] Form submitted");

  const msg = document.getElementById("message").value;
  const tags = document.getElementById("tags").value;
  const mediaInput = document.getElementById("media");
  const media = mediaInput ? mediaInput.files[0] : null;

  console.log("[DEBUG] Message:", msg);
  console.log("[DEBUG] Tags:", tags);
  console.log("[DEBUG] Media:", media ? media.name : "No media selected");

  if (!msg.trim()) {
    alert("Isi menfess tidak boleh kosong!");
    console.warn("[WARN] Menfess kosong");
    return;
  }

  const formData = new FormData();
  formData.append("message", msg);
  formData.append("tags", tags);
  if (media) formData.append("media", media);

  try {
    console.log("[DEBUG] Sending POST request to FastAPI...");
    const res = await fetch("/submit", {
      method: "POST",
      body: formData,
    });

    console.log("[DEBUG] Awaiting response from FastAPI...");
    const result = await res.json();
    console.log("[DEBUG] FastAPI response:", result);

    console.log("[DEBUG] Sending data to Telegram WebApp...");
    Telegram.WebApp.sendData(JSON.stringify(result));
    console.log("[DEBUG] Closing Telegram WebApp...");
    Telegram.WebApp.close();
  } catch (err) {
    alert("❌ Gagal mengirim menfess.");
    console.error("[ERROR] Submit failed:", err);
  }
});
