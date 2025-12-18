const API_URL =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8088/api/v1/poem"
    : "https://ai-poem-generator-fwdr.onrender.com/api/v1/poem";

// change to Render URL later

async function generatePoem() {
  const input = document.getElementById("inputText").value;
  const output = document.getElementById("output");
  output.textContent = "";

  if (!input.trim()) return;

  output.textContent = "✍️ The poet is thinking...\n";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input_text: input })
    });

    const data = await response.json();
    typeText(data.poem, output);

  } catch (err) {
    output.textContent = "Something went wrong.";
  }
}

function typeText(text, element, delay = 30) {
  element.textContent = "";
  let i = 0;

  const interval = setInterval(() => {
    element.textContent += text[i];
    i++;
    if (i >= text.length) clearInterval(interval);
  }, delay);
}
