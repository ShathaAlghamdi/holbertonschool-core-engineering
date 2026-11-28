const socket = new WebSocket("ws://localhost:8000/ws");

const messages = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const username = document.getElementById("username");
const statusEl = document.getElementById("status");

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(text, type) {
  const li = document.createElement("li");
  li.className = "message " + type;

  const body = document.createElement("span");
  body.className = "text";
  body.textContent = text;

  const time = document.createElement("span");
  time.className = "time";
  time.textContent = timeNow();

  li.appendChild(body);
  li.appendChild(time);
  messages.appendChild(li);
  messages.scrollTop = messages.scrollHeight;
}

function setStatus(online) {
  statusEl.textContent = online ? "Connected" : "Disconnected";
  statusEl.className = "status " + (online ? "online" : "offline");
}

socket.onopen = () => {
  setStatus(true);
  addMessage("Connection established", "system");
};

socket.onmessage = (event) => {
  addMessage(event.data, "received");
};

socket.onclose = () => {
  setStatus(false);
  addMessage("Connection lost", "system");
};

socket.onerror = () => {
  addMessage("Connection error", "system");
};

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text || socket.readyState !== WebSocket.OPEN) {
    return;
  }
  const name = username.value.trim();
  const payload = name ? name + ": " + text : text;
  socket.send(payload);
  addMessage(payload, "sent");
  input.value = "";
  input.focus();
});
