(function () {
    function safeParseJson(text) {
        try {
            return JSON.parse(text);
        } catch (error) {
            return null;
        }
    }

    function appendBubble(container, role, content) {
        const isUser = role === "user";
        const wrapper = document.createElement("div");
        wrapper.className = isUser ? "flex justify-end" : "flex justify-start";

        const bubble = document.createElement("div");
        bubble.className =
            "max-w-[80%] rounded-2xl px-3 py-2 " +
            (isUser
                ? "bg-brand text-black"
                : "bg-white/10 text-white/90");
        bubble.textContent = content;

        wrapper.appendChild(bubble);
        container.appendChild(wrapper);
        container.scrollTop = container.scrollHeight;
    }

    function getMessageInput(form) {
        return form.querySelector("input[name='message']");
    }

    function getMessagesContainer() {
        return document.getElementById("ai-messages");
    }

    function isAiForm(target) {
        return target && target.closest && target.closest("[data-ai-form]");
    }

    function handleBeforeRequest(event) {
        const form = isAiForm(event.target);
        if (!form) return;

        const input = getMessageInput(form);
        const messages = getMessagesContainer();
        if (!input || !messages) return;

        const message = input.value.trim();
        if (!message) return;

        appendBubble(messages, "user", message);
    }

    document.addEventListener("htmx:beforeRequest", handleBeforeRequest);

    window.handleChatResponse = function handleChatResponse(event) {
        const form = event.detail?.target?.closest("[data-ai-form]");
        if (!form) return;

        const messages = getMessagesContainer();
        const input = getMessageInput(form);
        if (!messages) return;

        const xhr = event.detail?.xhr;
        const status = xhr?.status || 0;
        const responseText = xhr?.responseText || "";

        if (status === 429) {
            appendBubble(messages, "assistant", "Too many requests. Please wait and try again.");
            return;
        }

        const data = safeParseJson(responseText);
        if (status < 200 || status >= 300) {
            const errorText =
                data?.answer ||
                data?.error ||
                "Something went wrong. Please try again.";
            appendBubble(messages, "assistant", errorText);
            return;
        }

        const answer = data?.answer || "No response available.";
        appendBubble(messages, "assistant", answer);

        if (input) input.value = "";
    };

    document.addEventListener("htmx:afterRequest", (event) => {
        if (!isAiForm(event.target)) return;
        window.handleChatResponse(event);
    });

    document.addEventListener("DOMContentLoaded", () => {
        const toggle = document.getElementById("ai-toggle");
        const panel = document.getElementById("ai-panel");
        if (!toggle || !panel) return;

        toggle.addEventListener("click", () => {
            panel.classList.toggle("hidden");
            const isOpen = !panel.classList.contains("hidden");
            toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
        });
    });
})();
