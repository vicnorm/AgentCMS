const getMetaContent = (name) =>
    document.querySelector(`meta[name="${name}"]`)?.getAttribute("content") || "";

const stateUrl = getMetaContent("builder-state-url");
const saveUrl = getMetaContent("builder-save-url");
const csrfToken = getMetaContent("csrf-token");

function setTabValue(tabId, value) {
    const pre = document.querySelector(`#${tabId} pre`);
    if (pre) {
        pre.textContent = value || "";
        pre.style.display = (value || "").trim() ? "" : "none";
    }
}

async function loadBuilderState() {
    const response = await fetch(stateUrl, { credentials: "same-origin" });
    if (!response.ok) {
        throw new Error("Failed to load builder state");
    }
    const data = await response.json();

    const canvas = document.getElementById("canvas");
    if (canvas) {
        canvas.innerHTML = `<h2 id="canvas-heading">Canvas</h2>${data.html_content || ""}`;
    }

    setTabValue("tab1", data.html_content);
    setTabValue("tab2", data.css_content);
    setTabValue("tab3", data.js_content);
}

function collectState() {
    return {
        html_content: document.querySelector("#tab1 pre")?.textContent || "",
        css_content: document.querySelector("#tab2 pre")?.textContent || "",
        js_content: document.querySelector("#tab3 pre")?.textContent || "",
    };
}

async function saveBuilderState() {
    const payload = collectState();
    const response = await fetch(saveUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        throw new Error("Failed to save builder state");
    }

    window.alert("Builder content saved.");
}

document.addEventListener("DOMContentLoaded", async () => {
    const saveButton = document.getElementById("save-to-cms");
    if (saveButton) {
        saveButton.addEventListener("click", async () => {
            try {
                await saveBuilderState();
            } catch (error) {
                console.error(error);
                window.alert("Unable to save builder content.");
            }
        });
    }

    try {
        await loadBuilderState();
    } catch (error) {
        console.error(error);
    }
});
