const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");

function appendMessage(sender, text) {
  const div = document.createElement("div");
  div.className = `bubble ${sender}`;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// İlk mesaj
appendMessage("bot", "Hi! Ask me for a movie recommendation. 🎬");

form.onsubmit = async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  appendMessage("user", text);
  input.value = "";
  appendMessage("bot", "...");

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    chat.lastChild.innerText = data.response || "No response.";
  } catch {
    chat.lastChild.innerText = "❌ Network error.";
  }
};
